# Luxembourgish Anki Flashcards

This repository contains Luxembourgish audio flashcards for Anki.

There are two versions:

- `FLASHCARDS/`: cards with Brazilian Portuguese translations.
- `FLASHCARDS_EN/`: cards with US English translations.

Both versions use the same audio files:

```text
FLASHCARDS_MEDIA/
```

Each audio file creates two cards:

1. Audio on the front; Luxembourgish transcript and translation on the back.
2. Luxembourgish transcript on the front; audio and translation on the back.

## 1. Download and Install Anki

1. Go to the official Anki website:

```text
https://apps.ankiweb.net/
```

2. Download Anki for your computer.
3. Install and open Anki.
4. Create a profile if Anki asks you to.

You do not need an AnkiWeb account to import these cards. An AnkiWeb account is only needed if you want to sync between your computer and phone.

## 2. Download This Repository

On GitHub, click:

```text
Code > Download ZIP
```

Then unzip the `.zip` file on your computer.

After unzipping, you should see these folders:

```text
FLASHCARDS/
FLASHCARDS_EN/
FLASHCARDS_MEDIA/
```

Important: the audio files are stored with Git LFS. If you download with `Download ZIP`, GitHub should include the real audio files. If you clone with Git, install Git LFS and run:

```powershell
git lfs pull
```

## 3. Choose Which Version to Import

For cards with Brazilian Portuguese translations, use:

```text
FLASHCARDS/
```

For cards with US English translations, use:

```text
FLASHCARDS_EN/
```

For either version, you also need:

```text
FLASHCARDS_MEDIA/
```

This folder contains the audio used by the cards.

## 4. Find Anki's Media Folder

Anki stores audio and image files in a folder named:

```text
collection.media
```

Common locations:

Windows:

```text
%APPDATA%\Anki2\PROFILE_NAME\collection.media
```

macOS:

```text
/Users/YOUR_USER/Library/Application Support/Anki2/PROFILE_NAME/collection.media
```

Linux:

```text
/home/YOUR_USER/.local/share/Anki2/PROFILE_NAME/collection.media
```

If you do not know your profile name, open Anki and go to:

```text
File > Switch Profile
```

On a new Anki installation, the profile is usually called `User 1`.

## 5. Open `collection.media`

### Windows

1. Close Anki.
2. Open File Explorer.
3. Click the address bar.
4. Paste:

```text
%APPDATA%\Anki2
```

5. Press Enter.
6. Open your profile folder, for example `User 1`.
7. Open `collection.media`.

### macOS

1. Close Anki.
2. Open Finder.
3. In the top menu, click:

```text
Go > Go to Folder...
```

4. Paste:

```text
~/Library/Application Support/Anki2
```

5. Press Enter.
6. Open your profile folder, for example `User 1`.
7. Open `collection.media`.

### Linux

1. Close Anki.
2. Open your file manager.
3. Go to:

```text
~/.local/share/Anki2
```

4. Open your profile folder, for example `User 1`.
5. Open `collection.media`.

## 6. Copy the Audio Files

Open this repository folder:

```text
FLASHCARDS_MEDIA/
```

Copy all `.mp3` files from that folder into Anki's media folder:

```text
collection.media/
```

Correct:

```text
collection.media/
  inll_efebb85a6dde_A1_KAPITEL_1_Audio_01_001.mp3
  inll_6ec08fc98d25_A1_KAPITEL_1_Audio_01_002.mp3
```

Wrong:

```text
collection.media/
  FLASHCARDS_MEDIA/
    inll_efebb85a6dde_A1_KAPITEL_1_Audio_01_001.mp3
```

The `.mp3` files must be directly inside `collection.media`, not inside a subfolder.

## 7. Create Decks in Anki

Open Anki and create the decks before importing the files.

A recommended structure is:

```text
Luxembourgish::A1::Kapitel 1
Luxembourgish::A1::Kapitel 2
Luxembourgish::A2::Kapitel 1
Luxembourgish::B1::Kapitel 1
```

For the English translation version, you can use:

```text
Luxembourgish EN::A1::Kapitel 1
Luxembourgish EN::A2::Kapitel 1
Luxembourgish EN::B1::Kapitel 1
```

In Anki, `::` creates subdecks. For example:

```text
Luxembourgish::A1::Kapitel 1
```

creates `Kapitel 1` inside `A1`, inside `Luxembourgish`.

## 8. Import the CSV Files

Each chapter has one `.csv` file.

Examples:

```text
FLASHCARDS/A1/KAPITEL 1/A1_KAPITEL 1_flashcards.csv
FLASHCARDS_EN/A1/KAPITEL 1/A1_KAPITEL 1_flashcards.csv
```

To import one chapter:

1. Open Anki.
2. Click the deck where that chapter should go.
3. Go to:

```text
File > Import
```

4. Choose the chapter `.csv` file.
5. In the import screen, check:

```text
Type / Note Type: Basic
Deck: the correct chapter deck
Field 1: Front
Field 2: Back
Separator: comma
Allow HTML in fields: enabled
```

6. Click Import.
7. Repeat this for every chapter you want to import.

The CSV files already start with:

```text
#separator:comma
#html:true
#columns:Front,Back
```

These lines help Anki read the file correctly.

## 9. Check That Audio Works

After importing the first chapter:

1. Open Anki's card browser.
2. Click one imported card.
3. Preview the card.
4. Press the audio/play button.

If the audio does not play:

1. Check that the `.mp3` files were copied into `collection.media`.
2. Check that they are not inside a subfolder.
3. In Anki, run:

```text
Tools > Check Media
```

Anki will report missing media files.

If you imported an older version of this deck, delete the old notes before importing again. Older media files started with `flashcards_`; the current files start with `inll_` and include an audio hash to keep every card synchronized with the correct file.

## 10. Recommended Anki Settings

These settings are a good starting point for language learning with audio.

Open the deck options:

```text
Click the gear next to the deck > Options
```

Recommended settings:

```text
FSRS: enabled
Desired retention: 0.90
New cards/day: 20 to 40
Maximum reviews/day: 9999
Learning steps: 10m
Relearning steps: 10m
Bury new siblings: enabled
Bury review siblings: enabled
```

Why these settings:

- `FSRS` is Anki's modern scheduler and usually works better than the older scheduler.
- `0.90` desired retention is a good balance between remembering well and avoiding too many reviews.
- `20 to 40` new cards per day is enough to make progress without creating a huge review backlog.
- `9999` maximum reviews/day prevents Anki from hiding due review cards.
- `Bury siblings` is useful because each audio creates two related cards, and it is usually better not to see both on the same day.

After a few weeks of study, run:

```text
Deck Options > FSRS > Optimize
```

This lets Anki tune the schedule based on your real review history.

## 11. How to Study These Cards

For cards with audio on the front:

1. Listen before reading anything.
2. Try to understand the meaning.
3. Show the back.
4. Read the Luxembourgish transcript.
5. Read the translation.
6. Repeat the sentence out loud.

For cards with Luxembourgish on the front:

1. Read the Luxembourgish.
2. Try to remember the meaning.
3. Show the back.
4. Listen to the audio.
5. Compare it with the translation.

Use Anki's answer buttons honestly:

- `Again`: you did not understand it or forgot it.
- `Hard`: you understood it, but with serious effort.
- `Good`: you understood it well enough.
- `Easy`: it was immediate.

Do not press `Hard` when you completely forgot the card. In that case, use `Again`.

## 12. Folder Reference

```text
FLASHCARDS/        CSV files with Brazilian Portuguese cards
FLASHCARDS_EN/     CSV files with US English cards
FLASHCARDS_MEDIA/  MP3 files used by both versions
TRANSCRIPTS/       Luxembourgish transcripts
TRANSLATION/       Brazilian Portuguese translations
TRANSLATION_EN/    US English translations
MANIFESTS/         Files used to audit audio, transcript, and translation mapping
scripts/           Scripts used to generate the project
```

## 13. Official Anki Documentation

- Download Anki: https://apps.ankiweb.net/
- Importing: https://docs.ankiweb.net/importing/intro.html
- Importing text files and media: https://docs.ankiweb.net/importing/text-files.html
- Anki files and `collection.media`: https://docs.ankiweb.net/files.html
- Deck options and FSRS: https://docs.ankiweb.net/deck-options
