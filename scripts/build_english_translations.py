from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

from openai import OpenAI

from transcribe_translate import normalize_dialogue


TRANSLATE_MODEL = "gpt-5-nano"
RETRY_TRANSLATE_MODEL = "gpt-4.1-mini"


ENGLISH_TRANSLATION_INSTRUCTIONS = """
You are a strict Luxembourgish-to-US-English translator.
Output constraints are mandatory:
Return only US English dialogue lines.
Keep exactly one translated line for each input line, and every line must start with "- ".
Translate all Luxembourgish words. Keep only personal names and place names unchanged.
Never write notes, brackets, explanations, uncertainty, titles, or timestamps.
Common meanings:
Moien = Hello
Gudde Moien = Good morning
Wéi heescht Dir? = What is your name?
Mäi Numm ass = My name is
An Dir? = And you?
An du? = And you?
Vu wou kommt Dir? = Where are you from?
Aus der Schwäiz = From Switzerland
Sidd Dir Schwäizer? = Are you Swiss?
Sidd Dir Fransous? = Are you French?
Ech kommen aus Frankräich = I come from France
Ech kommen aus = I come from
ech schwätzen = I speak
e bësse = a little
kee franzéisch = I do not speak French
Wéi eng Sprooch schwätz du? = What language do you speak?
zwou Sproochen = two languages
och = also
Nee = No
Fändelen = flags
zeechnen = draw
wann ech glift = please
""".strip()


RETRY_INSTRUCTIONS = """
Fix the US English translation.
You will receive the original Luxembourgish text and a previous translation attempt.
Return only the corrected US English translation.
Keep exactly one translated line for each original input line, every line starting with "- ".
Remove all notes, brackets, explanations, uncertainty, and untranslated Luxembourgish.
Keep only personal names and place names unchanged.
""".strip()


LUXEMBOURGISH_MARKERS = (
    "[",
    "]",
    "Note:",
    "Moien",
    "mäi ",
    "Mäi ",
    "Ech ",
    "ech ",
    "schwätz",
    "schwätzen",
    "lëtzebuergesch",
    "franzéisch",
    "Sprooch",
    "Sproochen",
    "Schwäiz",
    "Frankräich",
    "Fransous",
    "Sidd ",
    "Wéi ",
    "Vu wou",
    "Fändelen",
    "Nee, ech",
    "Lëtzebuerg",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Translate TRANSCRIPTS to US English while preserving the folder tree."
    )
    parser.add_argument("--transcripts-root", default="TRANSCRIPTS")
    parser.add_argument("--translation-root", default="TRANSLATION_EN")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--sleep", type=float, default=0.2)
    return parser.parse_args()


def needs_retry(text: str) -> bool:
    return any(marker in text for marker in LUXEMBOURGISH_MARKERS)


def translate_to_english(client: OpenAI, transcript: str) -> str:
    response = client.chat.completions.create(
        model=TRANSLATE_MODEL,
        reasoning_effort="minimal",
        messages=[
            {"role": "system", "content": ENGLISH_TRANSLATION_INSTRUCTIONS},
            {"role": "user", "content": transcript},
        ],
    )
    translation = normalize_dialogue(response.choices[0].message.content or "")

    if needs_retry(translation):
        retry = client.chat.completions.create(
            model=RETRY_TRANSLATE_MODEL,
            temperature=0,
            messages=[
                {"role": "system", "content": RETRY_INSTRUCTIONS},
                {
                    "role": "user",
                    "content": (
                        "Original Luxembourgish:\n"
                        f"{transcript}\n\n"
                        "Previous translation attempt:\n"
                        f"{translation}"
                    ),
                },
            ],
        )
        translation = normalize_dialogue(retry.choices[0].message.content or "")

    return translation


def main() -> int:
    args = parse_args()
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: set OPENAI_API_KEY before running.", file=sys.stderr)
        return 2

    transcripts_root = Path(args.transcripts_root).resolve()
    translation_root = Path(args.translation_root).resolve()
    if not transcripts_root.exists():
        print(f"Error: folder not found: {transcripts_root}", file=sys.stderr)
        return 2

    transcript_paths = sorted(transcripts_root.rglob("*.txt"))
    client = OpenAI(api_key=api_key)

    print(f"Transcripts: {transcripts_root}")
    print(f"English translations: {translation_root}")
    print(f"Files: {len(transcript_paths)}")

    for index, transcript_path in enumerate(transcript_paths, 1):
        relative_path = transcript_path.relative_to(transcripts_root)
        output_path = translation_root / relative_path
        print(f"[{index}/{len(transcript_paths)}] {relative_path}")

        if output_path.exists() and not args.overwrite:
            print(f"  existing -> {output_path}")
            continue

        transcript = transcript_path.read_text(encoding="utf-8")
        translation = translate_to_english(client, transcript)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(translation, encoding="utf-8")
        print(f"  translated -> {output_path}")
        time.sleep(args.sleep)

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
