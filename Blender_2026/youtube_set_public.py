#!/usr/bin/env python3
"""업로드된 YouTube 영상 공개 설정 변경 (unlisted → public)"""

import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

BASE_DIR = Path(__file__).parent
TOKEN_FILE = BASE_DIR / "youtube_token.json"
URLS_FILE = BASE_DIR / "youtube_urls.json"

SCOPES = ["https://www.googleapis.com/auth/youtube"]

def main():
    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())

    youtube = build("youtube", "v3", credentials=creds)

    with open(URLS_FILE, "r") as f:
        data = json.load(f)

    # 재생목록도 public으로
    playlist_id = data["playlist_id"]
    pl = youtube.playlists().list(part="snippet,status", id=playlist_id).execute()
    if pl["items"]:
        item = pl["items"][0]
        item["status"]["privacyStatus"] = "public"
        youtube.playlists().update(
            part="snippet,status",
            body=item
        ).execute()
        print(f"📋 재생목록 → public: {playlist_id}")

    # 각 영상 public으로
    for num, info in data["videos"].items():
        if "video_id" not in info:
            print(f"   ⏭️  {num}번 클립 스킵 (미업로드)")
            continue

        video_id = info["video_id"]
        youtube.videos().update(
            part="status",
            body={
                "id": video_id,
                "status": {
                    "privacyStatus": "public",
                    "selfDeclaredMadeForKids": False,
                    "embeddable": True,
                }
            }
        ).execute()
        print(f"   ✅ {num}번 → public + embed 허용: https://youtu.be/{video_id}")

    print("\n✅ 전체 공개 설정 완료!")

if __name__ == "__main__":
    main()
