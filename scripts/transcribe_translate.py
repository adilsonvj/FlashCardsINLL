from __future__ import annotations

import argparse
import os
import re
import sys
import time
from pathlib import Path

from openai import OpenAI


TRANSCRIBE_MODEL = "gpt-4o-transcribe"
FORMAT_MODEL = "gpt-4.1-mini"
TRANSLATE_MODEL = "gpt-5-nano"
RETRY_TRANSLATE_MODEL = "gpt-4.1-mini"


TRANSCRIPTION_PROMPT = """
The audio is a Luxembourgish language-learning recording (A1, A2, or B1), often with short dialogues.
Transcribe in Luxembourgish (Letzebuergesch / Lëtzebuergesch), not German, French, or English.
Common phrases may include: Wéi heescht Dir? Mäi Numm ass..., Vu wou kommt Dir?,
Aus der Schwäiz, vu Basel. Sidd Dir Schwäizer? Sidd Dir Fransous?
Ech kommen aus Frankräich, vu Nancy.
Return only the transcript.
""".strip()


FORMAT_INSTRUCTIONS = """
Format this Luxembourgish language-learning transcript as dialogue.
Split every question, answer, and short follow-up such as "an Dir?" into its own natural spoken turn.
Every output line must start with "- ".
Preserve the Luxembourgish wording and accents. You may fix only obvious speech-recognition spelling
for common A1 phrases, such as Wé/Wéi heescht Dir, Mäi Numm ass, Vu wou kommt Dir,
Sidd Dir Schwäizer, Sidd Dir Fransous, Ech kommen aus Frankräich.
Do not translate. Do not add notes, explanations, speaker names, or timestamps.
""".strip()


TRANSLATION_INSTRUCTIONS = """
You are a strict Luxembourgish-to-Brazilian-Portuguese translator.
Output constraints are mandatory:
Return only Brazilian Portuguese dialogue lines.
Keep exactly one translated line for each input line, and every line must start with "- ".
Translate all Luxembourgish words. Keep only personal names and place names unchanged.
Never write notes, brackets, explanations, uncertainty, titles, or timestamps.
Glossary:
Moien = Olá
Gudde Moien = Bom dia
Wéi heescht Dir? = Qual é o seu nome?
Mäi Numm ass = Meu nome é
An Dir? = E você?
An du? = E você?
Vu wou kommt Dir? = De onde você vem?
Aus der Schwäiz = Da Suíça
Sidd Dir Schwäizer? = Você é suíço?
Sidd Dir Fransous? = Você é francês?
Ech kommen aus Frankräich = Eu venho da França
Ech kommen aus = Eu venho de
ech schwätzen = eu falo
e bësse = um pouco
kee franzéisch = não falo francês
Wéi eng Sprooch schwätz du? = Que língua você fala?
zwou Sproochen = duas línguas
och = também
Nee = Não
Fändelen = bandeiras
zeechnen = desenhar
wann ech glift = por favor
""".strip()


RETRY_TRANSLATION_INSTRUCTIONS = """
Fix the Brazilian Portuguese translation.
You will receive the original Luxembourgish text and a previous translation attempt.
Return only the corrected Brazilian Portuguese translation.
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
)

COMMENT_MARKERS = (
    "Note:",
    "Nota:",
    "Observação:",
    "Observacao:",
    "Explanation:",
    "Comentário:",
    "Comentario:",
    "Transcrição:",
    "Transcricao:",
    "Transcript:",
    "Tradução:",
    "Traducao:",
    "Translation:",
    "Title:",
    "Titel:",
    "Título:",
    "Titulo:",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Transcribe audio from CUTS and translate it while preserving the folder tree."
    )
    parser.add_argument(
        "source",
        nargs="?",
        default="CUTS",
        help="Source folder inside CUTS, for example: 'CUTS/A1/KAPITEL 1'.",
    )
    parser.add_argument("--cuts-root", default="CUTS")
    parser.add_argument("--transcripts-root", default="TRANSCRIPTS")
    parser.add_argument("--translation-root", default="TRANSLATION")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--sleep", type=float, default=0.2)
    return parser.parse_args()


def normalize_dialogue(text: str) -> str:
    text = text.replace("\ufeff", "")
    lines = [line.strip() for line in text.replace("\r\n", "\n").split("\n")]
    lines = [line for line in lines if line]
    if not lines:
        return ""

    normalized: list[str] = []
    for line in lines:
        if any(marker.lower() in line.lower() for marker in COMMENT_MARKERS):
            continue
        line = re.sub(r"\s*\[[^\]]*\]", "", line).strip()
        line = re.sub(
            r"\s*\((?:note|nota|observa(?:ç|c)ão|explanation|coment[aá]rio)[^)]*\)",
            "",
            line,
            flags=re.IGNORECASE,
        ).strip()
        if not line:
            continue
        if line.startswith(("-", "–", "—")):
            line = line[1:].strip()
            while line.startswith(("-", "–", "—")):
                line = line[1:].strip()
            if not line:
                continue
            normalized.append("- " + line)
        elif line:
            normalized.append("- " + line)
        else:
            continue
    return "\n".join(normalized).strip() + "\n"


def fix_common_portuguese_typos(text: str) -> str:
    replacements = {
        "suiço": "suíço",
        "Suiço": "Suíço",
        "voce": "você",
        "Voce": "Você",
        "eu falo nenhum francês": "eu não falo francês",
        "Eu falo nenhum francês": "Eu não falo francês",
        "Fransous": "francês",
        "Lëtzebuerg": "Luxemburgo",
    }
    for wrong, right in replacements.items():
        text = text.replace(wrong, right)
    return text


def translation_needs_retry(text: str) -> bool:
    return any(marker in text for marker in LUXEMBOURGISH_MARKERS)


def output_path(
    audio_path: Path, source_root: Path, destination_root: Path, suffix: str = ".txt"
) -> Path:
    return destination_root / audio_path.relative_to(source_root).with_suffix(suffix)


def transcribe_audio(client: OpenAI, audio_path: Path) -> str:
    with audio_path.open("rb") as audio_file:
        result = client.audio.transcriptions.create(
            model=TRANSCRIBE_MODEL,
            file=audio_file,
            prompt=TRANSCRIPTION_PROMPT,
            response_format="text",
        )
    return str(result).strip()


def format_transcript(client: OpenAI, transcript: str) -> str:
    response = client.chat.completions.create(
        model=FORMAT_MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": FORMAT_INSTRUCTIONS},
            {"role": "user", "content": transcript},
        ],
    )
    return normalize_dialogue(response.choices[0].message.content or "")


def translate_text(client: OpenAI, transcript: str) -> str:
    response = client.chat.completions.create(
        model=TRANSLATE_MODEL,
        reasoning_effort="minimal",
        messages=[
            {"role": "system", "content": TRANSLATION_INSTRUCTIONS},
            {"role": "user", "content": transcript},
        ],
    )
    translation = normalize_dialogue(response.choices[0].message.content or "")
    translation = fix_common_portuguese_typos(translation)
    if translation_needs_retry(translation):
        retry = client.chat.completions.create(
            model=RETRY_TRANSLATE_MODEL,
            temperature=0,
            messages=[
                {"role": "system", "content": RETRY_TRANSLATION_INSTRUCTIONS},
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
    return fix_common_portuguese_typos(translation)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    args = parse_args()
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: set OPENAI_API_KEY before running.", file=sys.stderr)
        return 2

    source_root = Path(args.cuts_root).resolve()
    source = Path(args.source).resolve()
    transcripts_root = Path(args.transcripts_root).resolve()
    translation_root = Path(args.translation_root).resolve()

    if not source.exists():
        print(f"Error: source folder not found: {source}", file=sys.stderr)
        return 2
    if not source.is_relative_to(source_root):
        print(f"Error: source must be inside {source_root}", file=sys.stderr)
        return 2

    audio_paths = sorted(source.rglob("*.mp3"))
    if args.limit is not None:
        audio_paths = audio_paths[: args.limit]
    if not audio_paths:
        print(f"No MP3 files found in {source}")
        return 0

    client = OpenAI(api_key=api_key)

    print(f"Source: {source}")
    print(f"Audio files found: {len(audio_paths)}")
    print(f"Transcripts: {transcripts_root}")
    print(f"Translations: {translation_root}")

    for index, audio_path in enumerate(audio_paths, start=1):
        transcript_path = output_path(audio_path, source_root, transcripts_root)
        translation_path = output_path(audio_path, source_root, translation_root)

        print(f"[{index}/{len(audio_paths)}] {audio_path.relative_to(source_root)}")

        if args.overwrite or not transcript_path.exists():
            raw_transcript = transcribe_audio(client, audio_path)
            transcript = format_transcript(client, raw_transcript)
            write_text(transcript_path, transcript)
            print(f"  transcribed -> {transcript_path}")
            time.sleep(args.sleep)
        else:
            transcript = transcript_path.read_text(encoding="utf-8")
            print(f"  existing transcript -> {transcript_path}")

        if args.overwrite or not translation_path.exists():
            translation = translate_text(client, transcript)
            write_text(translation_path, translation)
            print(f"  translated -> {translation_path}")
            time.sleep(args.sleep)
        else:
            print(f"  existing translation -> {translation_path}")

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
