#!/usr/bin/env python3
"""
Mint Robot 튜토리얼 영상 → YouTube 업로드
"""

import json
import time
from pathlib import Path

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

BASE_DIR = Path(__file__).parent
CLIENT_SECRET = BASE_DIR / "client_secret.json"
TOKEN_FILE = BASE_DIR / "youtube_token.json"
RESULT_FILE = BASE_DIR / "mint_robot_urls.json"

SCOPES = ["https://www.googleapis.com/auth/youtube"]

VIDEOS = [
    {
        "path": BASE_DIR / "Mint_robot/MR_Tutorial_videos/001.Mint_Robot_reference_setting.mov",
        "title": "[Week 03] 01. 민트 로봇 레퍼런스 이미지 설정",
        "description": "Blender 뷰포트에 레퍼런스 이미지를 배치하는 방법\n정면·측면·후면 이미지를 각 뷰에 정렬해 민트 로봇의 비율을 잡아봅니다.\n\nRPD 2026 Spring | 인하대학교 로봇프러덕트 디자인\nWeek 03: 기초 모델링 1 — Edit + Modifier",
    },
    {
        "path": BASE_DIR / "Mint_robot/MR_Tutorial_videos/002.Mint_Robot_head_mirror.mov",
        "title": "[Week 03] 02. 민트 로봇 헤드 Mirror 모델링",
        "description": "Mirror Modifier를 사용해 민트 로봇 헤드를 대칭으로 모델링하는 과정\n한쪽만 만들고 대칭 복사로 효율적인 모델링 흐름을 익힙니다.\n\nRPD 2026 Spring | 인하대학교 로봇프러덕트 디자인\nWeek 03: 기초 모델링 1 — Edit + Modifier",
    },
]

TAGS = ["Blender", "블렌더", "튜토리얼", "RPD", "인하대", "로봇제품디자인", "2026", "민트로봇", "3D모델링"]


def get_youtube_service():
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


def upload_video(youtube, video_info):
    body = {
        "snippet": {
            "title": video_info["title"],
            "description": video_info["description"],
            "tags": TAGS,
            "categoryId": "27",
        },
        "status": {
            "privacyStatus": "unlisted",
            "selfDeclaredMadeForKids": False,
        },
    }
    media = MediaFileUpload(str(video_info["path"]), mimetype="video/quicktime", resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            pct = int(status.progress() * 100)
            print(f"   ⬆️  {pct}%", end="\r")

    video_id = response["id"]
    print(f"   ✅ https://youtu.be/{video_id}          ")
    return video_id


def main():
    print("🔑 YouTube 인증 중...")
    youtube = get_youtube_service()

    results = []
    for i, v in enumerate(VIDEOS):
        if not v["path"].exists():
            print(f"❌ 파일 없음: {v['path']}")
            continue

        print(f"\n🎬 [{i+1}/{len(VIDEOS)}] {v['title']}")
        print(f"   📁 {v['path'].name}")

        video_id = upload_video(youtube, v)
        results.append({
            "title": v["title"],
            "file": v["path"].name,
            "video_id": video_id,
            "url": f"https://youtu.be/{video_id}",
        })

        if i < len(VIDEOS) - 1:
            time.sleep(2)

    # 결과 저장
    with open(RESULT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*50}")
    print("✅ 업로드 완료!")
    for r in results:
        print(f"  {r['title']}")
        print(f"  → {r['url']}")
    print(f"{'='*50}")
    print(f"📄 결과: {RESULT_FILE}")


if __name__ == "__main__":
    main()
