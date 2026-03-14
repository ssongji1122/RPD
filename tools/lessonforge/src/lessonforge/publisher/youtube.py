"""YouTube upload via YouTube Data API v3.

Uploads videos with metadata (title, description, tags, privacy).
Requires OAuth2 credentials from Google Cloud Console.

Setup:
    1. Create a project at https://console.cloud.google.com
    2. Enable YouTube Data API v3
    3. Create OAuth 2.0 credentials (Desktop app)
    4. Download client_secrets.json to tools/lessonforge/
    5. First run will open browser for authorization
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Optional

from .metadata import VideoMetadata


# OAuth2 scopes needed for YouTube upload
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE = "youtube"
YOUTUBE_API_VERSION = "v3"


def find_credentials(search_dirs: Optional[list[Path]] = None) -> Optional[Path]:
    """Find client_secrets.json for YouTube API authentication."""
    if search_dirs is None:
        search_dirs = [
            Path.cwd(),
            Path(__file__).parent.parent.parent.parent,  # tools/lessonforge/
            Path.home() / ".config" / "lessonforge",
        ]

    for d in search_dirs:
        candidate = d / "client_secrets.json"
        if candidate.exists():
            return candidate

    return None


def authenticate(client_secrets_path: Path, token_path: Optional[Path] = None):
    """Authenticate with YouTube API using OAuth2.

    Returns an authorized YouTube API service object.
    First run opens a browser for user authorization.
    Subsequent runs use the cached token.
    """
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
    except ImportError:
        raise ImportError(
            "YouTube upload requires:\n"
            "  pip install google-api-python-client google-auth-oauthlib"
        )

    if token_path is None:
        token_path = client_secrets_path.parent / "youtube_token.json"

    credentials = None

    # Try to load cached credentials
    if token_path.exists():
        credentials = Credentials.from_authorized_user_file(
            str(token_path), [YOUTUBE_UPLOAD_SCOPE]
        )

    # Refresh or get new credentials
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(client_secrets_path), [YOUTUBE_UPLOAD_SCOPE]
            )
            credentials = flow.run_local_server(port=0)

        # Cache credentials
        token_path.write_text(credentials.to_json())

    return build(YOUTUBE_API_SERVICE, YOUTUBE_API_VERSION, credentials=credentials)


def upload_video(
    video_path: Path,
    metadata: VideoMetadata,
    *,
    client_secrets: Optional[Path] = None,
    youtube_service=None,
    thumbnail_path: Optional[Path] = None,
) -> dict:
    """Upload a video to YouTube with metadata.

    Args:
        video_path: Path to the MP4 video file.
        metadata: Video metadata (title, description, tags, etc.).
        client_secrets: Path to client_secrets.json.
        youtube_service: Pre-authenticated YouTube service (optional).
        thumbnail_path: Custom thumbnail image (optional).

    Returns:
        Dict with video ID and URL.
    """
    try:
        from googleapiclient.http import MediaFileUpload
    except ImportError:
        raise ImportError(
            "YouTube upload requires:\n"
            "  pip install google-api-python-client google-auth-oauthlib"
        )

    if not video_path.exists():
        raise FileNotFoundError(f"Video not found: {video_path}")

    # Authenticate if needed
    if youtube_service is None:
        if client_secrets is None:
            client_secrets = find_credentials()
            if client_secrets is None:
                raise FileNotFoundError(
                    "client_secrets.json not found. See docstring for setup instructions."
                )
        youtube_service = authenticate(client_secrets)

    # Build request body
    body = {
        "snippet": {
            "title": metadata.title,
            "description": metadata.description,
            "tags": metadata.tags,
            "categoryId": metadata.category_id,
            "defaultLanguage": metadata.language,
            "defaultAudioLanguage": metadata.language,
        },
        "status": {
            "privacyStatus": metadata.privacy_status,
            "selfDeclaredMadeForKids": False,
        },
    }

    # Create media upload
    media = MediaFileUpload(
        str(video_path),
        mimetype="video/mp4",
        resumable=True,
        chunksize=10 * 1024 * 1024,  # 10MB chunks
    )

    # Execute upload with retry
    request = youtube_service.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media,
    )

    response = _resumable_upload(request)

    video_id = response.get("id", "")
    result = {
        "video_id": video_id,
        "url": f"https://youtu.be/{video_id}",
        "title": metadata.title,
        "privacy": metadata.privacy_status,
    }

    # Set thumbnail if provided
    if thumbnail_path and thumbnail_path.exists() and video_id:
        try:
            youtube_service.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(str(thumbnail_path), mimetype="image/png"),
            ).execute()
            result["thumbnail"] = str(thumbnail_path)
        except Exception:
            pass  # Thumbnail upload is optional

    # Add to playlist if specified
    if metadata.playlist_name and video_id:
        try:
            playlist_id = _find_or_create_playlist(
                youtube_service, metadata.playlist_name
            )
            if playlist_id:
                youtube_service.playlistItems().insert(
                    part="snippet",
                    body={
                        "snippet": {
                            "playlistId": playlist_id,
                            "resourceId": {
                                "kind": "youtube#video",
                                "videoId": video_id,
                            },
                        },
                    },
                ).execute()
                result["playlist_id"] = playlist_id
        except Exception:
            pass  # Playlist is optional

    return result


def _resumable_upload(request, max_retries: int = 3) -> dict:
    """Execute a resumable upload with exponential backoff retry."""
    response = None
    retry = 0

    while response is None:
        try:
            status, response = request.next_chunk()
            if status:
                progress = int(status.progress() * 100)
                if progress % 25 == 0:
                    print(f"  Upload: {progress}%")
        except Exception as e:
            if retry >= max_retries:
                raise RuntimeError(f"Upload failed after {max_retries} retries: {e}")
            retry += 1
            wait = 2 ** retry
            print(f"  Retry {retry}/{max_retries} in {wait}s...")
            time.sleep(wait)

    return response


def _find_or_create_playlist(youtube_service, playlist_name: str) -> Optional[str]:
    """Find an existing playlist by name, or create a new one."""
    # Search existing playlists
    playlists = youtube_service.playlists().list(
        part="snippet",
        mine=True,
        maxResults=50,
    ).execute()

    for item in playlists.get("items", []):
        if item["snippet"]["title"] == playlist_name:
            return item["id"]

    # Create new playlist
    result = youtube_service.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": playlist_name,
                "description": f"인하대학교 로봇프러덕트 디자인 강의 영상",
            },
            "status": {
                "privacyStatus": "unlisted",
            },
        },
    ).execute()

    return result.get("id")
