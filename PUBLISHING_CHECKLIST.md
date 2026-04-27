# Publishing Checklist

Use this checklist before pushing the project to a public or shared GitHub repository.

## Secret Safety

- Do not commit real OpenAI API keys.
- Do not commit `.env` files.
- Do not commit local Anki profile folders or databases.
- Use environment variables for API keys:

```powershell
$env:OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
python scripts\transcribe_translate.py CUTS
Remove-Item Env:OPENAI_API_KEY
```

The project scripts and Markdown files should only contain placeholders such as `YOUR_OPENAI_API_KEY`.

## Personal Information Safety

Before publishing, search for personal usernames, local paths, and profile names:

```powershell
Get-ChildItem -Recurse -File -Include *.py,*.md,*.csv,*.txt,*.json,*.yml,*.yaml,*.toml,*.ini,*.ps1,*.bat,*.cmd |
  Select-String -Pattern 'C:\\Users\\|AppData\\Roaming\\Anki2|OPENAI_API_KEY\\s*=\\s*.+' -CaseSensitive:$false
```

Expected result: no matches containing real secrets or personal paths.

For API keys, also run a dedicated secret scanner such as GitHub secret scanning or `gitleaks` before pushing.

## Audio and Copyright Safety

This repository contains audio files. Audio is usually the highest-risk part of publishing.

Before pushing to a public repository, confirm that you have the right to redistribute the audio files in:

```text
CUTS/
FLASHCARDS_MEDIA/
```

If you do not have redistribution rights, do not publish those folders.

In that case, uncomment these lines in `.gitignore` before committing:

```gitignore
CUTS/
FLASHCARDS_MEDIA/
```

You can still publish:

```text
scripts/
CONTEXT/
ANKI_IMPORT_GUIDE.md
PUBLISHING_CHECKLIST.md
TRANSCRIPTS/
TRANSLATION/
TRANSLATION_EN/
FLASHCARDS/
FLASHCARDS_EN/
```

However, the Anki audio will not work for other people unless they receive the matching MP3 files separately.

## Repository Size

The generated project is large because it contains both original audio and exported Anki audio media.

Current approximate size:

```text
CUTS:             about 498 MB
FLASHCARDS_MEDIA: about 498 MB
Total project:    about 1 GB
```

GitHub blocks individual files over 100 MB. The current files were checked and no file over 90 MB was found, but the total repository is still large.

If the repository feels too heavy, consider publishing only:

```text
FLASHCARDS/
FLASHCARDS_EN/
FLASHCARDS_MEDIA/
ANKI_IMPORT_GUIDE.md
```

and omitting:

```text
CUTS/
```

because `FLASHCARDS_MEDIA` already contains the audio files required by the Anki CSVs.

## Final Local Checks

Run these before commit:

```powershell
@'
from pathlib import Path
for path in [
    Path("scripts/transcribe_translate.py"),
    Path("scripts/build_english_translations.py"),
    Path("scripts/build_anki_flashcards.py"),
]:
    compile(path.read_text(encoding="utf-8"), str(path), "exec")
    print("ok", path)
'@ | python -B -
```

Check card CSV structure:

```powershell
@'
from pathlib import Path
import csv

for root in ["FLASHCARDS", "FLASHCARDS_EN"]:
    rows = 0
    bad = 0
    empty = 0
    for path in Path(root).rglob("*.csv"):
        with path.open(encoding="utf-8", newline="") as f:
            for row in csv.reader(line for line in f if not line.startswith("#")):
                rows += 1
                if len(row) != 2:
                    bad += 1
                elif not row[1].strip():
                    empty += 1
    print(root, "cards:", rows, "bad rows:", bad, "empty backs:", empty)
'@ | python -B -
```

Expected:

```text
FLASHCARDS cards: 2700 bad rows: 0 empty backs: 0
FLASHCARDS_EN cards: 2700 bad rows: 0 empty backs: 0
```
