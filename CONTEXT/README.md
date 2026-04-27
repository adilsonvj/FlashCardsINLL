# Project Context

This project turns short Luxembourgish audio files into Anki-ready flashcards.

The source audio files live in:

```text
CUTS/
  A1/
    KAPITEL 1/
    KAPITEL 2/
  A2/
  B1/
```

The generated text folders mirror the same structure:

```text
TRANSCRIPTS/
TRANSLATION/
TRANSLATION_EN/
```

For every `.mp3` in `CUTS`, there should be:

- one `.txt` in `TRANSCRIPTS` with the Luxembourgish transcript;
- one `.txt` in `TRANSLATION` with the Brazilian Portuguese translation;
- one `.txt` in `TRANSLATION_EN` with the US English translation.

All text files should use dialogue-style formatting:

```text
- First line.
- Second line.
```

No notes, comments, titles, timestamps, labels, or model explanations should appear inside the final transcript or translation files.

## Scripts

### Transcription and Portuguese Translation

```text
scripts/transcribe_translate.py
```

This script:

1. Transcribes audio with `gpt-4o-transcribe`.
2. Formats the transcript into dialogue lines with `gpt-4.1-mini`.
3. Translates to Brazilian Portuguese with `gpt-5-nano`.
4. Retries translation cleanup with `gpt-4.1-mini` if obvious untranslated text or notes appear.

Run it like this:

```powershell
$env:OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
python scripts\transcribe_translate.py CUTS
Remove-Item Env:OPENAI_API_KEY
```

To regenerate one folder:

```powershell
$env:OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
python scripts\transcribe_translate.py "CUTS\A1\KAPITEL 1" --overwrite
Remove-Item Env:OPENAI_API_KEY
```

Important: API keys must only be passed through environment variables. Do not commit, paste, or store real keys in project files.

### English Translation

```text
scripts/build_english_translations.py
```

This script reads `TRANSCRIPTS` and creates `TRANSLATION_EN`.

Run it like this:

```powershell
$env:OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
python scripts\build_english_translations.py
Remove-Item Env:OPENAI_API_KEY
```

### Anki Flashcards

```text
scripts/build_anki_flashcards.py
```

This script creates Anki CSV files and exports the referenced MP3 files.

Portuguese version:

```powershell
python scripts\build_anki_flashcards.py
```

English version:

```powershell
python scripts\build_anki_flashcards.py --translation-root TRANSLATION_EN --flashcards-root FLASHCARDS_EN
```

By default, media files are exported to:

```text
FLASHCARDS_MEDIA/
```

If you want the script to also copy media directly into a local Anki profile, pass the media folder explicitly:

```powershell
python scripts\build_anki_flashcards.py --media-dir "PATH\TO\collection.media"
```

or set:

```powershell
$env:ANKI_MEDIA_DIR="PATH\TO\collection.media"
python scripts\build_anki_flashcards.py
Remove-Item Env:ANKI_MEDIA_DIR
```

No personal Anki profile path is stored in the script.

## Current Generated Outputs

The full source tree has been processed.

Validated counts:

```text
CUTS:           1350 .mp3 files
TRANSCRIPTS:    1350 .txt files
TRANSLATION:    1350 .txt files
TRANSLATION_EN: 1350 .txt files
```

Portuguese flashcards:

```text
FLASHCARDS: 20 .csv files
Cards: 2700
```

English flashcards:

```text
FLASHCARDS_EN: 20 .csv files
Cards: 2700
```

Shared media:

```text
FLASHCARDS_MEDIA: 1350 .mp3 files
```

Import manifests:

```text
MANIFESTS/FLASHCARDS:    one manifest CSV per Portuguese level/chapter
MANIFESTS/FLASHCARDS_EN: one manifest CSV per English level/chapter
```

## Flashcard Format

Each audio generates two cards:

1. Front: audio. Back: Luxembourgish transcript plus translation.
2. Front: Luxembourgish transcript. Back: audio plus translation.

The CSV files include:

```text
#separator:comma
#html:true
#columns:Front,Back
```

The CSVs are generated so each card row has exactly one comma separator. Commas inside card text are encoded as `&#44;` to avoid import problems in Anki.

Media filenames start with `inll_` and include a hash of the source MP3 content. This keeps regenerated decks synchronized with the correct audio and avoids stale Anki media from older imports. Older exports used filenames starting with `flashcards_`; those should be removed from Anki after the new cards are confirmed.

## Useful Validation Commands

Count source and generated files:

```powershell
(Get-ChildItem -LiteralPath 'CUTS' -Recurse -File -Filter *.mp3).Count
(Get-ChildItem -LiteralPath 'TRANSCRIPTS' -Recurse -File -Filter *.txt).Count
(Get-ChildItem -LiteralPath 'TRANSLATION' -Recurse -File -Filter *.txt).Count
(Get-ChildItem -LiteralPath 'TRANSLATION_EN' -Recurse -File -Filter *.txt).Count
```

Check for transcript or translation lines that do not start with `- `:

```powershell
$badT = Get-ChildItem -LiteralPath 'TRANSCRIPTS' -Recurse -File -Filter *.txt | Where-Object { (Get-Content -LiteralPath $_.FullName -Encoding UTF8 | Where-Object { $_.Trim() -and -not $_.Trim().StartsWith('- ') }).Count -gt 0 }
$badP = Get-ChildItem -LiteralPath 'TRANSLATION' -Recurse -File -Filter *.txt | Where-Object { (Get-Content -LiteralPath $_.FullName -Encoding UTF8 | Where-Object { $_.Trim() -and -not $_.Trim().StartsWith('- ') }).Count -gt 0 }
$badE = Get-ChildItem -LiteralPath 'TRANSLATION_EN' -Recurse -File -Filter *.txt | Where-Object { (Get-Content -LiteralPath $_.FullName -Encoding UTF8 | Where-Object { $_.Trim() -and -not $_.Trim().StartsWith('- ') }).Count -gt 0 }
"Transcript files with non-dialogue lines: " + $badT.Count
"Portuguese translation files with non-dialogue lines: " + $badP.Count
"English translation files with non-dialogue lines: " + $badE.Count
```

Check Anki CSV structure:

```powershell
@'
from pathlib import Path
import csv

for root in ["FLASHCARDS", "FLASHCARDS_EN"]:
    rows = 0
    bad = []
    empty_back = []
    for path in Path(root).rglob("*.csv"):
        with path.open(encoding="utf-8", newline="") as f:
            for line_no, row in enumerate(csv.reader(line for line in f if not line.startswith("#")), 1):
                rows += 1
                if len(row) != 2:
                    bad.append((str(path), line_no, len(row)))
                elif not row[1].strip():
                    empty_back.append((str(path), line_no))
    print(root, "cards:", rows, "bad rows:", len(bad), "empty backs:", len(empty_back))
'@ | python -
```

Check media synchronization against the generated manifests:

```powershell
@'
from pathlib import Path
import csv

errors = []
rows = 0
for manifest in Path("MANIFESTS").rglob("*_manifest.csv"):
    deck_root = manifest.parts[1]
    translation_root = "TRANSLATION_EN" if deck_root == "FLASHCARDS_EN" else "TRANSLATION"
    with manifest.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            rows += 1
            checks = {
                "source_audio": Path("CUTS") / row["source_audio"],
                "anki_media_file": Path("FLASHCARDS_MEDIA") / row["anki_media_file"],
                "transcript_file": Path("TRANSCRIPTS") / row["transcript_file"],
                "translation_file": Path(translation_root) / row["translation_file"],
            }
            for key, path in checks.items():
                if not path.exists():
                    errors.append((str(manifest), key, str(path)))

print("manifest rows:", rows)
print("missing references:", len(errors))
'@ | python -
```

## Safety Notes

- No real API key should be stored in this repository.
- No personal Anki profile path should be stored in this repository.
- Use `FLASHCARDS_MEDIA` for sharing media safely.
- Anyone importing the cards should copy the files from `FLASHCARDS_MEDIA` into their own Anki `collection.media` folder.
