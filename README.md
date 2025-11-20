# Minesweeper AI Agent

This project implements an AI agent capable of playing and solving a modified version of the classic Minesweeper game. This was completed as a project for **UCI’s CS171: Introduction to Artificial Intelligence** course. The directions, shell framework, and world generation tools were provided as part of the course.

## Overview

The repository contains an AI agent that interacts with a Minesweeper environment provided by course staff. The agent receives percepts from the game, chooses actions, and attempts to safely uncover the entire board. The environment, game shell, and world generation tools were provided; I authored the AI logic inside the `MyAI` implementation.

### What I Built

* **`MyAI` implementation** (core solver logic)
* Additional helper functions inside the `MyAI` class
* All testing and evaluation performed during development

### What I Did Not Build

* **WorldGenerator** scripts (Python and Bash)
* **Shell framework**, including game engine, Makefile, and tournament scripts
* Provided sample worlds, manuals, and testing utilities

## Project Structure

```
Minesweeper_Student/
│
├── src/                 # Source code (MyAI implementation lives here)
├── bin/                 # Compiled program output
├── WorldGenerator/      # World generation utilities (provided)
├── Problems/            # Generated worlds (if created)
├── Makefile             # Build and submission tools
└── README.md            # This file
```

## How to Build

Navigate to the project’s root directory and run:

```bash
make
```

This compiles the full project and places the executable inside the `bin/` folder.

## How to Run

From the `bin/` directory:

### Run on a single random world

```bash
./Minesweeper
```

### Run using the Random or Manual AIs

```bash
./Minesweeper -r    # RandomAI
./Minesweeper -m    # ManualAI
```

### Run on a specific world file

```bash
./Minesweeper -f /path/to/world.txt
```

### Run on a folder of world files

```bash
./Minesweeper -f /path/to/folder/
```

### Debug / Verbose Options

```bash
./Minesweeper -d   # Debug mode (prints board after each move)
./Minesweeper -v   # Verbose mode (prints world filenames)
```

Multiple flags can be combined (e.g., `-fv`, `-rd`).

## World Generation

Although included in this repository, **the WorldGenerator scripts were not authored by me**.

Worlds can be generated with:

### Python script

```bash
python3 WorldGenerator.py numFiles baseName rows cols mines
```

### Bash scripts

```bash
./generateTournament
./generateSuperEasy
```

Generated worlds appear in the `Problems/` folder.

## Performance Summary

The AI was tested on all supported difficulties:

* **Beginner (8×8, 10 mines)**
* **Intermediate (16×16, 40 mines)**
* **Expert (16×30, 99 mines)**
* Additional small boards for minimal submission

Performance scales with board size, and tuning focused on safety-first inference rules, constraint logic, and systematic expansion strategies.
