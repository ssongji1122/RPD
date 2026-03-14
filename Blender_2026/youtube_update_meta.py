#!/usr/bin/env python3
"""YouTube 영상 메타데이터 업데이트 (제목/설명/태그)"""

import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

BASE_DIR = Path(__file__).parent
TOKEN_FILE = BASE_DIR / "youtube_token.json"
URLS_FILE = BASE_DIR / "youtube_urls.json"

SCOPES = ["https://www.googleapis.com/auth/youtube"]

# 클립별 메타데이터: (제목, 설명)
CLIP_META = {
    1:  ("[Week 02] 01. Blender 다운로드",
         "Blender 공식 사이트(blender.org)에서 최신 버전을 다운로드하는 방법을 안내합니다."),
    2:  ("[Week 02] 02. Blender 설치하기",
         "다운로드한 Blender 설치 파일을 실행하여 설치하는 과정을 보여줍니다."),
    3:  ("[Week 02] 03. Blender 첫 실행",
         "Blender를 처음 열었을 때 나타나는 Splash Screen과 기본 씬 구성을 살펴봅니다."),
    4:  ("[Week 02] 04. 인터페이스 소개",
         "Blender UI의 4가지 주요 영역(3D Viewport, Outliner, Properties, Timeline)을 소개합니다."),
    5:  ("[Week 02] 05. 인터페이스 심화",
         "뷰포트 Header의 Transform Orientation, Pivot Point, Snap 설정과 N 패널, 네비게이션 기즈모를 다룹니다."),
    6:  ("[Week 02] 06. 도구상자 (Toolbox)",
         "T 키로 여는 Tool Shelf의 도구 팔레트와 Move, Rotate, Scale 등 주요 도구를 소개합니다."),
    7:  ("[Week 02] 07. 오브젝트 추가 (Add Object)",
         "Shift+A로 Cube, Sphere, Cylinder 등 Primitive 오브젝트를 추가하는 방법을 보여줍니다."),
    8:  ("[Week 02] 08. 오브젝트 편집 (Object Edit)",
         "Object Mode에서 G(이동), R(회전), S(스케일) 기본 Transform 조작법을 다룹니다."),
    9:  ("[Week 02] 09. Tab 키로 모드 전환",
         "Tab 키를 사용하여 Object Mode와 Edit Mode를 전환하는 방법과 각 모드의 차이를 설명합니다."),
    10: ("[Week 02] 10. Extrude & Inset",
         "E 키로 면을 돌출(Extrude)하고, I 키로 면 안쪽에 새 면을 생성(Inset)하는 방법을 다룹니다."),
    11: ("[Week 02] 11. Bevel 도구",
         "Ctrl+B로 모서리를 부드럽게 깎는 Bevel 도구의 사용법과 Segment 조절 방법을 보여줍니다."),
    12: ("[Week 02] 12. Loop Cut 기초",
         "Ctrl+R로 메시에 Edge Loop을 추가하는 Loop Cut 도구의 기본 사용법을 다룹니다."),
    13: ("[Week 02] 13. Loop Cut 활용",
         "Loop Cut의 개수 조절(스크롤 휠)과 위치 조정, 실전 활용 방법을 보여줍니다."),
}

TAGS = ["Blender", "블렌더", "튜토리얼", "3D 모델링", "Blender 기초", "Blender 입문"]


def main():
    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())

    youtube = build("youtube", "v3", credentials=creds)

    with open(URLS_FILE, "r") as f:
        data = json.load(f)

    for num_str, info in data["videos"].items():
        num = int(num_str)
        if "video_id" not in info:
            print(f"   ⏭️  {num}번 스킵 (미업로드)")
            continue
        if num not in CLIP_META:
            continue

        video_id = info["video_id"]
        title, description = CLIP_META[num]

        # 기존 snippet 가져오기 (categoryId 유지 필요)
        resp = youtube.videos().list(part="snippet", id=video_id).execute()
        if not resp["items"]:
            print(f"   ❌ {num}번 영상 찾을 수 없음: {video_id}")
            continue

        snippet = resp["items"][0]["snippet"]
        snippet["title"] = title
        snippet["description"] = description
        snippet["tags"] = TAGS

        youtube.videos().update(
            part="snippet",
            body={"id": video_id, "snippet": snippet}
        ).execute()
        print(f"   ✅ {num:02d}. {title}")

    print("\n✅ 메타데이터 업데이트 완료!")


if __name__ == "__main__":
    main()
