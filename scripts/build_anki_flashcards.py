from __future__ import annotations

import argparse
import csv
import hashlib
import html
import os
import re
import shutil
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


CARD_CSS = (
    "font-family:Arial;"
    "font-size:24px;"
    "line-height:1.45;"
    "color:#111827;"
    "max-width:760px;"
    "margin:0 auto;"
    "padding:22px;"
)

TEXT_CSS = (
    "white-space:normal;"
    "padding:18px 20px;"
    "border:1px solid #e5e7eb;"
    "border-radius:10px;"
    "background:#ffffff;"
    "box-shadow:0 8px 24px #d1d5db;"
)

TRANSLATION_CSS = (
    "white-space:normal;"
    "margin-top:16px;"
    "padding:18px 20px;"
    "border-left:5px solid #2563eb;"
    "border-radius:10px;"
    "background:#f8fafc;"
)

AUDIO_CSS = (
    "display:flex;"
    "justify-content:center;"
    "align-items:center;"
    "min-height:150px;"
    "padding:22px;"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build Anki CSV flashcards and export referenced audio files."
    )
    parser.add_argument("--cuts-root", default="CUTS")
    parser.add_argument("--transcripts-root", default="TRANSCRIPTS")
    parser.add_argument("--translation-root", default="TRANSLATION")
    parser.add_argument("--flashcards-root", default="FLASHCARDS")
    parser.add_argument(
        "--export-media-root",
        default="FLASHCARDS_MEDIA",
        help="Local folder where the MP3 files referenced by the CSV files are exported.",
    )
    parser.add_argument(
        "--media-dir",
        default=os.environ.get("ANKI_MEDIA_DIR"),
        help=(
            "Optional Anki collection.media folder. If omitted, media is only exported "
            "to --export-media-root. You can also set ANKI_MEDIA_DIR."
        ),
    )
    return parser.parse_args()


def safe_media_name(relative_path: Path) -> str:
    raise RuntimeError("Use media_name_for_audio instead.")


def file_sha1_prefix(path: Path, length: int = 12) -> str:
    digest = hashlib.sha1()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()[:length]


def media_name_for_audio(audio_path: Path, relative_path: Path) -> str:
    stem = "__".join(relative_path.with_suffix("").parts)
    stem = re.sub(r"[^A-Za-z0-9]+", "_", stem).strip("_")
    return f"inll_{file_sha1_prefix(audio_path)}_{stem}.mp3"


def text_to_html(text: str) -> str:
    text = text.replace("\ufeff", "")
    lines = [line.strip() for line in text.replace("\r\n", "\n").split("\n")]
    cleaned: list[str] = []
    for line in lines:
        while line.startswith(("- -", "- –", "- —")):
            line = "- " + line[3:].strip()
        line = re.sub(r"^- \s*[-–—]\s*", "- ", line)
        if line:
            cleaned.append(line)
    lines = cleaned
    return "<br>".join(html.escape(line).replace(",", "&#44;") for line in lines)


def audio_html(media_name: str) -> str:
    return f"<div style='{CARD_CSS}'><div style='{AUDIO_CSS}'>[sound:{media_name}]</div></div>"


def text_html(text: str) -> str:
    return f"<div style='{CARD_CSS}'><div style='{TEXT_CSS}'>{text_to_html(text)}</div></div>"


def back_texts_html(transcript: str, translation: str) -> str:
    return (
        f"<div style='{CARD_CSS}'>"
        f"<div style='{TEXT_CSS}'>{text_to_html(transcript)}</div>"
        f"<div style='{TRANSLATION_CSS}'>{text_to_html(translation)}</div>"
        "</div>"
    )


def audio_translation_html(media_name: str, translation: str) -> str:
    return (
        f"<div style='{CARD_CSS}'>"
        f"<div style='{AUDIO_CSS}'>[sound:{media_name}]</div>"
        f"<div style='{TRANSLATION_CSS}'>{text_to_html(translation)}</div>"
        "</div>"
    )


def copy_media(audio_path: Path, media_dir: Path, media_name: str) -> None:
    media_dir.mkdir(parents=True, exist_ok=True)
    destination = media_dir / media_name
    if destination.exists() and destination.stat().st_size == audio_path.stat().st_size:
        return
    shutil.copy2(audio_path, destination)


def write_chapter_csv(
    chapter_dir: Path,
    cuts_root: Path,
    transcripts_root: Path,
    translation_root: Path,
    flashcards_root: Path,
    manifest_root: Path,
    export_media_root: Path,
    media_dir: Path | None,
) -> int:
    audio_paths = sorted(chapter_dir.glob("*.mp3"))
    if not audio_paths:
        return 0

    relative_chapter = chapter_dir.relative_to(cuts_root)
    output_dir = flashcards_root / relative_chapter
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{'_'.join(relative_chapter.parts)}_flashcards.csv"
    rows: list[list[str]] = []
    manifest_rows: list[list[str]] = []

    for audio_path in audio_paths:
        relative_audio = audio_path.relative_to(cuts_root)
        transcript_path = transcripts_root / relative_audio.with_suffix(".txt")
        translation_path = translation_root / relative_audio.with_suffix(".txt")

        if not transcript_path.exists():
            raise FileNotFoundError(f"Missing transcript: {transcript_path}")
        if not translation_path.exists():
            raise FileNotFoundError(f"Missing translation: {translation_path}")

        media_name = media_name_for_audio(audio_path, relative_audio)
        copy_media(audio_path, export_media_root, media_name)
        if media_dir is not None:
            copy_media(audio_path, media_dir, media_name)

        transcript = transcript_path.read_text(encoding="utf-8").strip()
        translation = translation_path.read_text(encoding="utf-8").strip()

        rows.append([audio_html(media_name), back_texts_html(transcript, translation)])
        rows.append([text_html(transcript), audio_translation_html(media_name, translation)])
        manifest_rows.append(
            [
                str(relative_chapter),
                str(relative_audio),
                media_name,
                str(transcript_path.relative_to(transcripts_root)),
                str(translation_path.relative_to(translation_root)),
                "2",
            ]
        )

    with output_path.open("w", encoding="utf-8", newline="") as file:
        file.write("#separator:comma\n")
        file.write("#html:true\n")
        file.write("#columns:Front,Back\n")
        writer = csv.writer(file)
        writer.writerows(rows)
    manifest_dir = manifest_root / relative_chapter
    manifest_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = manifest_dir / f"{'_'.join(relative_chapter.parts)}_manifest.csv"
    with manifest_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "chapter",
                "source_audio",
                "anki_media_file",
                "transcript_file",
                "translation_file",
                "cards_generated",
            ]
        )
        writer.writerows(manifest_rows)
    return len(audio_paths) * 2


def main() -> int:
    args = parse_args()
    cuts_root = (PROJECT_ROOT / args.cuts_root).resolve()
    transcripts_root = (PROJECT_ROOT / args.transcripts_root).resolve()
    translation_root = (PROJECT_ROOT / args.translation_root).resolve()
    flashcards_root = (PROJECT_ROOT / args.flashcards_root).resolve()
    manifest_root = (PROJECT_ROOT / "MANIFESTS" / Path(args.flashcards_root).name).resolve()
    export_media_root = (PROJECT_ROOT / args.export_media_root).resolve()
    media_dir = Path(args.media_dir).resolve() if args.media_dir else None

    if not cuts_root.exists():
        raise FileNotFoundError(cuts_root)
    if not transcripts_root.exists():
        raise FileNotFoundError(transcripts_root)
    if not translation_root.exists():
        raise FileNotFoundError(translation_root)

    total_notes = 0
    chapter_count = 0
    for chapter_dir in sorted(path for path in cuts_root.rglob("*") if path.is_dir()):
        notes = write_chapter_csv(
            chapter_dir,
            cuts_root,
            transcripts_root,
            translation_root,
            flashcards_root,
            manifest_root,
            export_media_root,
            media_dir,
        )
        if notes:
            chapter_count += 1
            total_notes += notes
            print(f"{chapter_dir.relative_to(cuts_root)}: {notes} cards")

    print(f"Chapters: {chapter_count}")
    print(f"Cards: {total_notes}")
    print(f"FLASHCARDS: {flashcards_root}")
    print(f"Manifests: {manifest_root}")
    print(f"Exported media: {export_media_root}")
    if media_dir is not None:
        print(f"Anki media: {media_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
