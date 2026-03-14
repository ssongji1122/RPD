#!/usr/bin/env python3
"""
Week 02 Blender 클립 → YouTube 자동 업로드
사용법: python3 youtube_upload.py
"""

import os
import json
import time
from pathlib import Path

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# ──────────────────────────────────────────
# 설정
# ──────────────────────────────────────────
BASE_DIR = Path(__file__).parent
CLIPS_DIR = BASE_DIR / "week_02" / "notion"
CLIENT_SECRET = BASE_DIR / "client_secret.json"
TOKEN_FILE = BASE_DIR / "youtube_token.json"
RESULT_FILE = BASE_DIR / "youtube_urls.json"

SCOPES = ["https://www.googleapis.com/auth/youtube"]

# 클립 번호 → (YouTube 제목, 설명)
CLIP_META = {
    1:  ("Blender 다운로드",            "Blender 공식 사이트에서 다운로드하는 방법"),
    2:  ("Blender 설치하기",            "Blender 설치 과정 안내"),
    3:  ("Blender 첫 실행",             "Blender를 처음 열었을 때 보이는 화면 설명"),
    4:  ("인터페이스 소개",              "Blender UI의 4가지 주요 영역 소개"),
    5:  ("인터페이스 심화",              "뷰포트 Header, N 패널, 네비게이션 기즈모 등"),
    6:  ("도구상자 (Toolbox)",           "T 패널의 도구 팔레트와 주요 도구 소개"),
    7:  ("오브젝트 추가 (Add Object)",   "Shift+A로 Primitive 오브젝트 추가하기"),
    8:  ("오브젝트 편집 (Object Edit)",  "Object Mode에서 G·R·S 기본 Transform"),
    9:  ("Tab 키로 모드 전환",           "Object Mode ↔ Edit Mode 전환 방법"),
    10: ("Extrude & Inset",             "E 키로 면 돌출, I 키로 면 안쪽 생성"),
    11: ("Bevel 도구",                  "Ctrl+B로 모서리를 부드럽게 처리하는 방법"),
    12: ("Loop Cut 기초",               "Ctrl+R로 Edge Loop 추가하기"),
    13: ("Loop Cut 활용",               "Loop Cut 개수 조절과 위치 조정"),
    14: ("Knife 도구",                  "K 키로 자유롭게 메시 분할하기"),
}

PLAYLIST_TITLE = "RPD 2026 Week 02 | Blender 기초"
PLAYLIST_DESC = "인하대학교 로봇제품디자인 2026 Spring - Week 02 Blender 인터페이스 및 기초 조작"

# ──────────────────────────────────────────


def get_youtube_service():
    """OAuth2 인증 → YouTube API 서비스 반환"""
    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

    return build("youtube", "v3", credentials=creds)


def create_playlist(youtube):
    """재생목록 생성"""
    body = {
        "snippet": {
            "title": PLAYLIST_TITLE,
            "description": PLAYLIST_DESC,
        },
        "status": {"privacyStatus": "unlisted"},
    }
    resp = youtube.playlists().insert(part="snippet,status", body=body).execute()
    playlist_id = resp["id"]
    print(f"📋 재생목록 생성: {PLAYLIST_TITLE} ({playlist_id})")
    return playlist_id


def add_to_playlist(youtube, playlist_id, video_id):
    """영상을 재생목록에 추가"""
    body = {
        "snippet": {
            "playlistId": playlist_id,
            "resourceId": {"kind": "youtube#video", "videoId": video_id},
        }
    }
    youtube.playlistItems().insert(part="snippet", body=body).execute()


def upload_video(youtube, filepath, title, description):
    """단일 영상 업로드 → video_id 반환"""
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": ["Blender", "튜토리얼", "RPD", "인하대", "로봇제품디자인", "2026"],
            "categoryId": "27",  # Education
        },
        "status": {
            "privacyStatus": "unlisted",
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(str(filepath), mimetype="video/mp4", resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            pct = int(status.progress() * 100)
            print(f"   ⬆️  {pct}%", end="\r")

    video_id = response["id"]
    print(f"   ✅ https://youtu.be/{video_id}")
    return video_id


def find_clips():
    """세그먼트 폴더에서 클립 파일 찾기 → [(clip_num, path)] 정렬"""
    clips = []
    for mp4 in CLIPS_DIR.rglob("*.mp4"):
        stem = mp4.stem
        try:
            num = int(stem.split("_", 1)[0])
            clips.append((num, mp4))
        except ValueError:
            continue
    return sorted(clips, key=lambda x: x[0])


def main():
    if not CLIENT_SECRET.exists():
        print(f"❌ client_secret.json 없음: {CLIENT_SECRET}")
        print("   Google Cloud Console에서 다운로드 후 위 경로에 넣어주세요.")
        return

    clips = find_clips()
    if not clips:
        print(f"❌ 클립 없음: {CLIPS_DIR}")
        return

    print(f"📂 {len(clips)}개 클립 발견\n")
    for num, path in clips:
        meta = CLIP_META.get(num, (path.stem, ""))
        print(f"   {num:02d}. {meta[0]}  ← {path.name}")

    print(f"\n🔑 YouTube 인증 중...")
    youtube = get_youtube_service()

    # 재생목록 생성
    playlist_id = create_playlist(youtube)

    # 업로드
    results = {}
    for i, (num, path) in enumerate(clips):
        title_text, desc_text = CLIP_META.get(num, (path.stem, ""))
        full_title = f"[Week 02] {num:02d}. {title_text}"
        full_desc = f"{desc_text}\n\nRPD 2026 Spring | 인하대학교 로봇제품디자인\nWeek 02: Blender 인터페이스 및 기초"

        print(f"\n🎬 [{i+1}/{len(clips)}] {full_title}")
        print(f"   📁 {path.name}")

        video_id = upload_video(youtube, path, full_title, full_desc)
        add_to_playlist(youtube, playlist_id, video_id)

        results[num] = {
            "video_id": video_id,
            "url": f"https://youtu.be/{video_id}",
            "title": full_title,
            "file": path.name,
        }

        # API 할당량 보호 (초당 요청 제한)
        if i < len(clips) - 1:
            time.sleep(2)

    # 결과 저장
    output = {
        "playlist_id": playlist_id,
        "playlist_url": f"https://youtube.com/playlist?list={playlist_id}",
        "videos": results,
    }
    with open(RESULT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*50}")
    print(f"✅ 전체 완료!")
    print(f"📋 재생목록: https://youtube.com/playlist?list={playlist_id}")
    print(f"📄 결과 파일: {RESULT_FILE}")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
