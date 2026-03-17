#!/usr/bin/env python3
"""Mint Robot 영상 description 업데이트 — 인하대 수업 내용 제거"""

from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

BASE_DIR = Path(__file__).parent
TOKEN_FILE = BASE_DIR / "youtube_token.json"
SCOPES = ["https://www.googleapis.com/auth/youtube"]

VIDEOS = [
    {
        "video_id": "-U82eI3eiQ0",
        "title": "[Week 03] 01. 민트 로봇 레퍼런스 이미지 설정",
        "description": "Blender 뷰포트에 레퍼런스 이미지를 배치하는 방법\n정면·측면·후면 이미지를 각 뷰에 정렬해 민트 로봇의 비율을 잡아봅니다.",
    },
    {
        "video_id": "FIY9RBLdYcA",
        "title": "[Week 03] 02. 민트 로봇 헤드 Mirror 모델링",
        "description": "Mirror Modifier를 사용해 민트 로봇 헤드를 대칭으로 모델링하는 과정\n한쪽만 만들고 대칭 복사로 효율적인 모델링 흐름을 익힙니다.",
    },
]

TAGS = ["Blender", "블렌더", "튜토리얼", "3D모델링", "민트로봇", "Mirror Modifier", "레퍼런스 이미지"]


def main():
    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if not creds.valid and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    youtube = build("youtube", "v3", credentials=creds)

    for v in VIDEOS:
        resp = youtube.videos().list(part="snippet", id=v["video_id"]).execute()
        if not resp["items"]:
            print(f"❌ 영상 없음: {v['video_id']}")
            continue

        snippet = resp["items"][0]["snippet"]
        snippet["title"] = v["title"]
        snippet["description"] = v["description"]
        snippet["tags"] = TAGS

        youtube.videos().update(
            part="snippet",
            body={"id": v["video_id"], "snippet": snippet}
        ).execute()
        print(f"✅ {v['title']}")

    print("\n완료!")


if __name__ == "__main__":
    main()
