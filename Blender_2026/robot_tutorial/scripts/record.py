"""
record.py — ffmpeg로 Blender 창 자동 녹화 제어
사용법:
  start_recording("step_00_setup")   # 녹화 시작
  stop_recording()                   # 녹화 종료
"""
import subprocess
import os
import signal
import time

RECORDINGS_DIR = os.path.join(os.path.dirname(__file__), "..", "recordings")
_proc = None  # 현재 녹화 프로세스

def start_recording(step_name):
    global _proc
    os.makedirs(RECORDINGS_DIR, exist_ok=True)
    output = os.path.abspath(os.path.join(RECORDINGS_DIR, f"{step_name}.mp4"))

    # 기존 녹화 중이면 종료
    if _proc and _proc.poll() is None:
        stop_recording()

    # ffmpeg — macOS 화면 캡처 (Capture screen 0 = 메인 디스플레이)
    # Blender 창: 1512x921, 위치 0,0
    cmd = [
        "/opt/homebrew/bin/ffmpeg", "-y",
        "-f", "avfoundation",
        "-framerate", "30",
        "-i", "4",           # Capture screen 0
        "-vf", "crop=1512:921:0:0",   # Blender 창 크기에 맞게 크롭
        "-vcodec", "libx264",
        "-preset", "ultrafast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        output
    ]

    _proc = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(1.5)  # 녹화 안정화 대기
    print(f"🔴 녹화 시작: {step_name}.mp4")
    return output

def stop_recording():
    global _proc
    if _proc and _proc.poll() is None:
        _proc.send_signal(signal.SIGINT)  # ffmpeg 정상 종료 (q 입력 효과)
        _proc.wait(timeout=10)
        print("⏹️  녹화 종료 완료")
    _proc = None
