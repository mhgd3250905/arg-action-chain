import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import requests


ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parents[1]
DEFAULT_KEY_FILE = REPO_ROOT.parent / "阿里tts-apikey.txt"
API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"
MODEL = "qwen3-tts-instruct-flash"
VOICE = "Kai"
LANGUAGE_TYPE = "Chinese"
INSTRUCTIONS = "语速偏快，吐字清晰，节奏有推进感，像知识分享视频的男声旁白；不要拖腔，不要夸张表演。"
WIDTH = 1920
HEIGHT = 1080
CHROME_HEIGHT = 984
CAPTURE_CROP_HEIGHT = 889
FPS = 30


def run(cmd: list[str], *, cwd: Path | None = None) -> None:
    printable = " ".join(f'"{part}"' if " " in part else part for part in cmd)
    print(f"[run] {printable}")
    subprocess.run(cmd, cwd=str(cwd or ROOT), check=True)


def capture(cmd: list[str], *, cwd: Path | None = None) -> str:
    return subprocess.check_output(cmd, cwd=str(cwd or ROOT), text=True, encoding="utf-8").strip()


def find_executable(names: list[str], extra_paths: list[Path] | None = None) -> str:
    for name in names:
        found = shutil.which(name)
        if found:
            return found
    for path in extra_paths or []:
        if path.exists():
            return str(path)
    raise FileNotFoundError(f"找不到可执行文件: {', '.join(names)}")


def read_api_key(key_file: Path | None) -> str:
    value = os.getenv("DASHSCOPE_API_KEY", "").strip()
    if value:
        return value
    candidate = key_file or DEFAULT_KEY_FILE
    if candidate.exists():
        return candidate.read_text(encoding="utf-8").strip()
    raise RuntimeError("缺少 DASHSCOPE_API_KEY，也找不到阿里tts-apikey.txt")


def load_narration() -> list[dict[str, Any]]:
    data = json.loads((ROOT / "narration.json").read_text(encoding="utf-8"))
    if not isinstance(data, list) or not data:
        raise RuntimeError("narration.json 必须是非空数组")
    return data


def screenshot_slides(chrome: str, narration: list[dict[str, Any]], frames_dir: Path) -> list[Path]:
    frames_dir.mkdir(parents=True, exist_ok=True)
    html_url = (ROOT / "index.html").resolve().as_uri()
    frames: list[Path] = []
    for item in narration:
        slide = int(item["slide"])
        out = frames_dir / f"slide-{slide:02d}.png"
        url = f"{html_url}?slide={slide}&recording=1"
        run(
            [
                chrome,
                "--headless=new",
                "--disable-gpu",
                "--hide-scrollbars",
                f"--window-size={WIDTH},{CHROME_HEIGHT}",
                f"--screenshot={out}",
                url,
            ]
        )
        frames.append(out)
    return frames


def audio_url_from_response(payload: Any) -> str:
    try:
        url = payload["output"]["audio"]["url"]
        if isinstance(url, str) and url.startswith(("http://", "https://")):
            return url
    except (KeyError, TypeError):
        pass

    stack = [payload]
    while stack:
        node = stack.pop()
        if isinstance(node, dict):
            stack.extend(node.values())
        elif isinstance(node, list):
            stack.extend(node)
        elif isinstance(node, str) and node.startswith(("http://", "https://")):
            parsed = urlparse(node)
            if any(parsed.path.lower().endswith(ext) for ext in (".wav", ".mp3", ".m4a")):
                return node
    raise RuntimeError(f"响应里没有找到音频 URL: {json.dumps(payload, ensure_ascii=False)[:600]}")


def tts_payload(text: str, instructions_in_input: bool) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": MODEL,
        "input": {
            "text": text,
            "voice": VOICE,
            "language_type": LANGUAGE_TYPE,
        },
    }
    if instructions_in_input:
        payload["input"]["instructions"] = INSTRUCTIONS
        payload["input"]["optimize_instructions"] = True
    else:
        payload["parameters"] = {
            "instructions": INSTRUCTIONS,
            "optimize_instructions": True,
        }
    return payload


def synthesize_one(api_key: str, text: str, out_path: Path, force: bool) -> Path:
    if out_path.exists() and not force:
        print(f"[skip] 已存在音频 {out_path.name}")
        return out_path

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    last_error: Exception | None = None
    for attempt in range(1, 4):
        try:
            response = requests.post(API_URL, headers=headers, json=tts_payload(text, True), timeout=240)
            if response.status_code == 400 and "instructions" in response.text:
                response = requests.post(API_URL, headers=headers, json=tts_payload(text, False), timeout=240)
            if response.status_code != 200:
                raise RuntimeError(f"TTS 请求失败: HTTP {response.status_code} {response.text[:600]}")

            payload = response.json()
            audio_url = audio_url_from_response(payload)
            audio = requests.get(audio_url, timeout=240)
            audio.raise_for_status()
            out_path.write_bytes(audio.content)
            print(f"[tts] {out_path.name} {len(audio.content)} bytes")
            time.sleep(0.25)
            return out_path
        except Exception as exc:
            last_error = exc
            if attempt == 3:
                break
            wait = attempt * 2
            print(f"[retry] {out_path.name} 第 {attempt} 次失败，{wait}s 后重试: {exc}")
            time.sleep(wait)
    raise RuntimeError(f"{out_path.name} 合成失败: {last_error}")


def synthesize_audio(
    api_key: str,
    narration: list[dict[str, Any]],
    audio_dir: Path,
    force: bool,
) -> list[Path]:
    audio_dir.mkdir(parents=True, exist_ok=True)
    files: list[Path] = []
    for item in narration:
        slide = int(item["slide"])
        out = audio_dir / f"slide-{slide:02d}.wav"
        files.append(synthesize_one(api_key, item["text"], out, force))
    return files


def duration_seconds(ffprobe: str, audio: Path) -> float:
    value = capture(
        [
            ffprobe,
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(audio),
        ]
    )
    return max(float(value), 1.2)


def make_clip(ffmpeg: str, ffprobe: str, frame: Path, audio: Path, out: Path) -> None:
    duration = duration_seconds(ffprobe, audio)
    frames = max(int(duration * FPS), FPS)
    vf = (
        f"crop={WIDTH}:{CAPTURE_CROP_HEIGHT}:0:0,"
        f"scale={WIDTH}:{HEIGHT},"
        f"zoompan=z='min(zoom+0.00028,1.032)':d={frames}:s={WIDTH}x{HEIGHT}:fps={FPS},"
        "format=yuv420p"
    )
    run(
        [
            ffmpeg,
            "-y",
            "-loop",
            "1",
            "-i",
            str(frame),
            "-i",
            str(audio),
            "-t",
            f"{duration:.3f}",
            "-vf",
            vf,
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "18",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            str(out),
        ]
    )


def concat_clips(ffmpeg: str, clips: list[Path], output: Path) -> None:
    concat_file = output.parent / "concat.txt"
    concat_file.write_text(
        "\n".join(f"file '{clip.as_posix()}'" for clip in clips) + "\n",
        encoding="utf-8",
    )
    run(
        [
            ffmpeg,
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-c",
            "copy",
            str(output),
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Render ARG 行动链路动态 HTML 为带旁白 MP4")
    parser.add_argument("--skip-tts", action="store_true", help="复用 build/audio 里已有音频")
    parser.add_argument("--force-tts", action="store_true", help="重新生成所有 TTS 音频")
    parser.add_argument("--key-file", type=Path, default=DEFAULT_KEY_FILE)
    parser.add_argument("--output", type=Path, default=ROOT / "arg-action-chain-intro.mp4")
    args = parser.parse_args()

    chrome = find_executable(
        ["chrome", "chrome.exe", "msedge", "msedge.exe"],
        [
            Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
            Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
        ],
    )
    ffmpeg = find_executable(["ffmpeg", "ffmpeg.exe"], [Path(r"D:\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe")])
    ffprobe = find_executable(["ffprobe", "ffprobe.exe"], [Path(r"D:\ffmpeg-master-latest-win64-gpl\bin\ffprobe.exe")])

    build = ROOT / "build"
    frames_dir = build / "frames"
    audio_dir = build / "audio"
    clips_dir = build / "clips"
    clips_dir.mkdir(parents=True, exist_ok=True)

    narration = load_narration()
    frames = screenshot_slides(chrome, narration, frames_dir)

    if args.skip_tts:
        audio = [audio_dir / f"slide-{int(item['slide']):02d}.wav" for item in narration]
        missing = [item for item in audio if not item.exists()]
        if missing:
            raise RuntimeError(f"--skip-tts 但缺少音频: {missing}")
    else:
        api_key = read_api_key(args.key_file)
        audio = synthesize_audio(api_key, narration, audio_dir, args.force_tts)

    clips: list[Path] = []
    for frame, wav in zip(frames, audio):
        out = clips_dir / f"{frame.stem}.mp4"
        make_clip(ffmpeg, ffprobe, frame, wav, out)
        clips.append(out)

    concat_clips(ffmpeg, clips, args.output)
    print(f"[done] {args.output}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"[error] {exc}", file=sys.stderr)
        raise
