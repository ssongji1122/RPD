#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

sys.path.insert(0, str(Path(__file__).parent))

from grading_db import (  # noqa: E402
    _load_grading_ids,
    detect_submission,
    load_student_roster,
    parse_student_weeks,
    query_grades,
)
from notion_api import _get_page_blocks, get_notion_token  # noqa: E402
from runtime_paths import ROOT  # noqa: E402


SEMESTER_START = date(2026, 3, 4)
TOTAL_WEEKS = 15
SEMESTER_END = SEMESTER_START + timedelta(weeks=TOTAL_WEEKS)
DEFAULT_OUT = ROOT / "web" / "public" / "admin" / "dashboard.enc.json"
RISK_MISSING_COUNT = 2
RISK_CONSECUTIVE_MISSING = 2
KDF_ITERATIONS = 310_000
SALT_BYTES = 16
IV_BYTES = 12


def current_week_num(today: date | None = None) -> int:
    today = today or date.today()
    delta = (today - SEMESTER_START).days
    week = delta // 7 + 1
    return max(1, min(week, TOTAL_WEEKS))


def is_semester_active(today: date | None = None) -> bool:
    today = today or date.today()
    return SEMESTER_START <= today <= SEMESTER_END


def load_dashboard_grading_ids() -> dict[str, str]:
    raw = os.environ.get("GRADING_DB_IDS")
    if raw:
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError("GRADING_DB_IDS는 JSON 문자열이어야 합니다.") from exc
        if not isinstance(data, dict):
            raise ValueError("GRADING_DB_IDS는 JSON 객체여야 합니다.")
        return {str(k): str(v) for k, v in data.items() if v}
    return _load_grading_ids()


def normalize_grade_name(name: str) -> str:
    return name.split(" (", 1)[0].strip()


def load_grade_map(db_id: str | None, token: str) -> dict[tuple[str, str], dict[str, Any]]:
    if not db_id:
        print("[경고] grades_db_id가 없어 성적 필드는 null로 기록합니다.", file=sys.stderr)
        return {}

    try:
        rows = query_grades(db_id=db_id, token=token)
    except Exception as exc:
        print(f"[경고] 성적 DB를 읽지 못해 성적 필드는 null로 기록합니다: {exc}", file=sys.stderr)
        return {}

    grade_map: dict[tuple[str, str], dict[str, Any]] = {}
    for row in rows:
        class_num = str(row.get("class_num", "")).replace("반", "")
        student_id = str(row.get("student_id", "")).strip()
        student_name = normalize_grade_name(str(row.get("student_name", "")))
        if student_id:
            grade_map[(class_num, student_id)] = row
        if student_name:
            grade_map[(class_num, student_name)] = row
    return grade_map


def grade_value(row: dict[str, Any] | None, key: str) -> int | float | None:
    if row is None:
        return None
    return row.get(key)


def count_consecutive_missing(weeks: dict[str, bool], current_week: int) -> int:
    count = 0
    for week in range(current_week, 0, -1):
        if weeks.get(f"{week:02d}", False):
            break
        count += 1
    return count


def build_dashboard_payload(token: str) -> dict[str, Any]:
    roster = load_student_roster()
    if not roster:
        raise RuntimeError("학생 명단을 불러올 수 없습니다.")

    ids = load_dashboard_grading_ids()
    grades = load_grade_map(ids.get("grades_db_id"), token)
    current_week = current_week_num()

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    risk_students: list[dict[str, Any]] = []
    scan_errors: list[dict[str, Any]] = []

    sorted_roster = sorted(
        roster,
        key=lambda item: (str(item.get("class_num", "")), str(item.get("student_id", "")), str(item.get("name", ""))),
    )

    for student in sorted_roster:
        class_num = str(student["class_num"])
        try:
            blocks = _get_page_blocks(student["page_id"], token=token)
            parsed_weeks = parse_student_weeks(blocks)
            weeks = {
                f"{week:02d}": detect_submission(parsed_weeks.get(f"{week:02d}", []), token=token)
                for week in range(1, TOTAL_WEEKS + 1)
            }
        except Exception as exc:
            # 페이지가 삭제·아카이브됐거나 일시 오류인 학생은 표시만 하고 집계를 계속한다.
            print(f"[경고] {class_num}반 {student['name']} 페이지 스캔 실패: {exc}", file=sys.stderr)
            scan_errors.append({
                "class_num": class_num,
                "name": student["name"],
                "student_id": student["student_id"],
            })
            grade_row = grades.get((class_num, student["student_id"])) or grades.get((class_num, student["name"]))
            grouped[class_num].append({
                "name": student["name"],
                "student_id": student["student_id"],
                "scan_error": True,
                "weeks": {},
                "submitted_count": None,
                "missing_count": None,
                "consecutive_missing": None,
                "missing_weeks": [],
                "attendance": grade_value(grade_row, "attendance"),
                "midterm": grade_value(grade_row, "midterm"),
                "final": grade_value(grade_row, "final"),
                "submissions_db_count": grade_value(grade_row, "submissions"),
            })
            continue

        current_week_keys = [f"{week:02d}" for week in range(1, current_week + 1)]
        missing_weeks = [week for week in current_week_keys if not weeks.get(week, False)]
        submitted_count = sum(1 for week in current_week_keys if weeks.get(week, False))
        missing_count = len(missing_weeks)
        consecutive_missing = count_consecutive_missing(weeks, current_week)

        grade_row = grades.get((class_num, student["student_id"])) or grades.get((class_num, student["name"]))
        student_payload = {
            "name": student["name"],
            "student_id": student["student_id"],
            "weeks": weeks,
            "submitted_count": submitted_count,
            "missing_count": missing_count,
            "consecutive_missing": consecutive_missing,
            "missing_weeks": missing_weeks,
            "attendance": grade_value(grade_row, "attendance"),
            "midterm": grade_value(grade_row, "midterm"),
            "final": grade_value(grade_row, "final"),
            "submissions_db_count": grade_value(grade_row, "submissions"),
        }
        grouped[class_num].append(student_payload)

        if missing_count >= RISK_MISSING_COUNT or consecutive_missing >= RISK_CONSECUTIVE_MISSING:
            reason = (
                f"{consecutive_missing}주 연속 미제출"
                if consecutive_missing >= RISK_CONSECUTIVE_MISSING
                else f"누적 {missing_count}회 미제출"
            )
            risk_students.append({
                "class_num": class_num,
                "name": student["name"],
                "student_id": student["student_id"],
                "missing_count": missing_count,
                "consecutive_missing": consecutive_missing,
                "missing_weeks": missing_weeks,
                "reason": reason,
            })

    if scan_errors and len(scan_errors) == len(sorted_roster):
        raise RuntimeError("모든 학생 페이지 스캔에 실패했습니다. 토큰·권한을 확인하세요.")

    class_titles = {
        str(student["class_num"]): student.get("class_title") or f"{student['class_num']}반 (DET3012-001)"
        for student in roster
    }
    classes = [
        {
            "class_num": class_num,
            "title": class_titles.get(class_num, f"{class_num}반 (DET3012-001)"),
            "students": grouped[class_num],
        }
        for class_num in sorted(grouped.keys())
    ]

    risk_students.sort(
        key=lambda item: (
            -int(item["consecutive_missing"]),
            -int(item["missing_count"]),
            str(item["class_num"]),
            str(item["student_id"]),
        )
    )

    return {
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "semester": {
            "start": SEMESTER_START.isoformat(),
            "total_weeks": TOTAL_WEEKS,
        },
        "current_week": current_week,
        "classes": classes,
        "risk_students": risk_students,
        "scan_errors": scan_errors,
    }


def derive_key(passphrase: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=SHA256(),
        length=32,
        salt=salt,
        iterations=KDF_ITERATIONS,
    )
    return kdf.derive(passphrase.encode("utf-8"))


def encrypt_payload(payload: dict[str, Any], passphrase: str) -> tuple[dict[str, Any], bytes]:
    plaintext = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    salt = os.urandom(SALT_BYTES)
    iv = os.urandom(IV_BYTES)
    key = derive_key(passphrase, salt)
    ciphertext = AESGCM(key).encrypt(iv, plaintext, None)

    decrypted = AESGCM(key).decrypt(iv, ciphertext, None)
    if decrypted != plaintext:
        raise RuntimeError("암호화 self-test에 실패했습니다.")

    encrypted = {
        "v": 1,
        "kdf": "PBKDF2-SHA256",
        "iterations": KDF_ITERATIONS,
        "salt": base64.b64encode(salt).decode("ascii"),
        "iv": base64.b64encode(iv).decode("ascii"),
        "ciphertext": base64.b64encode(ciphertext).decode("ascii"),
    }
    return encrypted, plaintext


def ensure_plain_path_allowed(path: Path) -> None:
    resolved = path.expanduser().resolve()
    try:
        resolved.relative_to(ROOT)
    except ValueError:
        return
    raise ValueError("--plain 경로는 repo 밖이어야 합니다.")


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="RPD 강사 대시보드 집계 JSON을 암호화해 저장")
    parser.add_argument("--force", action="store_true", help="학기 기간 밖에도 실행")
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="암호화 JSON 출력 경로")
    parser.add_argument("--plain", help="디버그용 평문 JSON 출력 경로. repo 밖 경로만 허용")
    args = parser.parse_args()

    if not args.force and not is_semester_active():
        print("학기 기간 밖이라 대시보드 집계를 건너뜁니다. 강제 실행은 --force를 사용하세요.")
        return 3

    token = get_notion_token()
    if not token:
        print("ERROR: NOTION_TOKEN이 설정되지 않았습니다.", file=sys.stderr)
        return 1

    passphrase = os.environ.get("DASHBOARD_PASSPHRASE")
    if not passphrase:
        print("ERROR: DASHBOARD_PASSPHRASE가 설정되지 않았습니다.", file=sys.stderr)
        return 1

    try:
        payload = build_dashboard_payload(token)
        encrypted, plaintext = encrypt_payload(payload, passphrase)
        out_path = Path(args.out).expanduser().resolve()
        write_json(out_path, encrypted)

        if args.plain:
            plain_path = Path(args.plain)
            ensure_plain_path_allowed(plain_path)
            plain_path = plain_path.expanduser().resolve()
            plain_path.parent.mkdir(parents=True, exist_ok=True)
            plain_path.write_bytes(plaintext + b"\n")

    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    total_students = sum(len(item["students"]) for item in payload["classes"])
    print(f"대시보드 집계 완료: {len(payload['classes'])}개 반, {total_students}명")
    print(f"암호화 파일: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
