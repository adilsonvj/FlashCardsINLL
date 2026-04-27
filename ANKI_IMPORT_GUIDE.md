# Anki Import Guide

This guide explains how to import the generated Luxembourgish flashcards into Anki.

There are two flashcard sets:

- `FLASHCARDS`: cards with Brazilian Portuguese translations.
- `FLASHCARDS_EN`: cards with US English translations.

The audio files needed by both sets are in:

```text
FLASHCARDS_MEDIA/
```

## 1. What to Share

To share both Portuguese and English versions, send:

```text
FLASHCARDS/
FLASHCARDS_EN/
FLASHCARDS_MEDIA/
ANKI_IMPORT_GUIDE.md
```

To share only the English version, send:

```text
FLASHCARDS_EN/
FLASHCARDS_MEDIA/
ANKI_IMPORT_GUIDE.md
```

To share only the Portuguese version, send:

```text
FLASHCARDS/
FLASHCARDS_MEDIA/
ANKI_IMPORT_GUIDE.md
```

## 2. Find Anki's Media Folder

Anki stores audio and image files in a profile folder named:

```text
collection.media
```

Typical locations:

Windows:

```text
%APPDATA%\Anki2\YOUR_ANKI_PROFILE\collection.media
```

macOS:

```text
/Users/YOUR_MAC_USER/Library/Application Support/Anki2/YOUR_ANKI_PROFILE/collection.media
```

Linux:

```text
/home/YOUR_LINUX_USER/.local/share/Anki2/YOUR_ANKI_PROFILE/collection.media
```

If you do not know the Anki profile name, open Anki and check:

```text
File > Switch Profile
```

## 3. Open `collection.media`

### Windows

1. Close Anki before copying media.
2. Open File Explorer.
3. Paste this into the address bar:

```text
%APPDATA%\Anki2
```

4. Open your Anki profile folder.
5. Open `collection.media`.

### macOS

1. Close Anki before copying media.
2. Open Finder.
3. Choose:

```text
Go > Go to Folder...
```

4. Paste:

```text
~/Library/Application Support/Anki2
```

5. Open your Anki profile folder.
6. Open `collection.media`.

### Linux

1. Close Anki before copying media.
2. Open your file manager.
3. Go to:

```text
~/.local/share/Anki2
```

4. Open your Anki profile folder.
5. Open `collection.media`.

## 4. Copy the Audio Files

Copy all `.mp3` files from:

```text
FLASHCARDS_MEDIA/
```

into:

```text
collection.media/
```

Important:

- Copy the MP3 files themselves.
- Do not copy the `FLASHCARDS_MEDIA` folder as a subfolder.
- Do not create subfolders inside `collection.media`.
- The MP3 files must sit directly inside `collection.media`.

Correct:

```text
collection.media/
  inll_efebb85a6dde_A1_KAPITEL_1_Audio_01_001.mp3
  inll_6ec08fc98d25_A1_KAPITEL_1_Audio_01_002.mp3
  inll_0002e7118f4b_A1_KAPITEL_2_Audio_39_001.mp3
```

Incorrect:

```text
collection.media/
  FLASHCARDS_MEDIA/
    inll_efebb85a6dde_A1_KAPITEL_1_Audio_01_001.mp3
```

The CSV files reference audio like this:

```text
[sound:inll_efebb85a6dde_A1_KAPITEL_1_Audio_01_001.mp3]
```

The filenames must match exactly.

If you imported an older version of these flashcards, delete those old notes before importing again. Older exports used filenames starting with `flashcards_`; the current export uses filenames starting with `inll_` plus a hash of the audio file. This prevents Anki from reusing stale media for a card with the same visible audio name.

## 5. Import the CSV Files

The flashcards are stored as `.csv` files, one file per level/chapter.

Examples:

```text
FLASHCARDS/A1/KAPITEL 1/A1_KAPITEL 1_flashcards.csv
FLASHCARDS_EN/A1/KAPITEL 1/A1_KAPITEL 1_flashcards.csv
```

Each CSV starts with:

```text
#separator:comma
#html:true
#columns:Front,Back
```

This tells Anki:

- the file uses comma separation;
- HTML should be enabled;
- the fields are `Front` and `Back`.

### Import Steps

1. Open Anki.
2. Create or choose a deck.
3. Go to:

```text
File > Import
```

4. Select a `.csv` file, for example:

```text
FLASHCARDS_EN/A1/KAPITEL 1/A1_KAPITEL 1_flashcards.csv
```

5. In the import screen:

- Choose the correct deck.
- Use a note type with two fields, such as `Basic`.
- Map `Front` to `Front`.
- Map `Back` to `Back`.
- Make sure HTML is enabled.
- Make sure the separator is comma.

6. Import.
7. Repeat for the other chapter CSV files.

Suggested deck organization:

```text
Luxembourgish::A1::Kapitel 1
Luxembourgish::A1::Kapitel 2
Luxembourgish::A2::Kapitel 1
Luxembourgish::B1::Kapitel 1
```

For the English set:

```text
Luxembourgish EN::A1::Kapitel 1
Luxembourgish EN::A2::Kapitel 1
Luxembourgish EN::B1::Kapitel 1
```

## 6. Check That Audio Works

After importing:

1. Open Anki's browser.
2. Click one imported note.
3. Confirm that a field contains something like:

```text
[sound:flashcards_A1_KAPITEL_1_Audio_01_001.mp3]
```

4. Preview the card.
5. Play the audio.

If audio does not play:

1. Check that the referenced `.mp3` file exists in `collection.media`.
2. Check that the filename is exactly the same.
3. In Anki, run:

```text
Tools > Check Media
```

Anki will report media references that are missing.

If you are replacing a previous import, also let Anki remove unused media after you confirm the new cards work. The old unused files should be the ones starting with `flashcards_`; the current files start with `inll_`.

## 7. Recommended Anki Settings

These cards are for language learning with audio. The goal is frequent exposure without creating an overwhelming review load.

### Enable FSRS

Open deck options:

```text
Deck Options > FSRS
```

Enable FSRS.

Recommended starting desired retention:

```text
0.90
```

This is a good balance between remembering well and keeping daily reviews manageable. If you want stronger retention, try `0.92` or `0.93`, but expect more reviews. Avoid starting very high, such as `0.97`, because the workload can become heavy quickly.

### New Cards Per Day

Start modestly:

```text
New cards/day: 20 to 40
```

If you study every day and have enough time:

```text
New cards/day: 50 to 80
```

Do not add hundreds of new cards in one day unless you are ready for the review backlog.

### Maximum Reviews Per Day

Use a high enough limit that reviews are not blocked:

```text
Maximum reviews/day: 9999
```

If you prefer a cap, use something like:

```text
Maximum reviews/day: 300 to 500
```

Try to finish due reviews before adding many new cards.

### Learning Steps

A simple setup:

```text
Learning steps: 10m
Relearning steps: 10m
```

When using FSRS, avoid learning or relearning steps longer than one day.

### Bury Siblings

Each audio produces two related cards. To avoid seeing both immediately:

```text
Bury new siblings: On
Bury review siblings: On
```

### How to Review These Cards

For audio-front cards:

1. Listen first without reading.
2. Try to understand the meaning.
3. Show the back.
4. Read the Luxembourgish transcript.
5. Read the translation.
6. Repeat the sentence aloud if possible.

For transcript-front cards:

1. Read the Luxembourgish.
2. Try to recall the meaning.
3. Show the back.
4. Listen to the audio.
5. Compare with the translation.

### Button Use

Use the buttons honestly:

- `Again`: you did not understand or missed the main meaning.
- `Hard`: you understood, but with serious effort.
- `Good`: you understood well enough.
- `Easy`: it was immediate and obvious.

Do not press `Hard` when you actually forgot. Use `Again` instead.

### After a Few Weeks

After you have some review history:

```text
Deck Options > FSRS > Optimize
```

Anki can then tune FSRS parameters to your actual memory and study habits.

## 8. Official Anki References

- Media: https://docs.ankiweb.net/media.html
- Importing text files and media: https://docs.ankiweb.net/importing/text-files.html
- Deck options and FSRS: https://docs.ankiweb.net/deck-options
