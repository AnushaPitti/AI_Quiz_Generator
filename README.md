# AI Quiz Generator

> Internship Mini Project | Python with Generative AI | Think Champ PV LTD

## Overview

A terminal-based Python quiz application that asks multiple-choice questions,
validates answers, tracks scores, and saves results to a file.

## Features

- 15 questions across three difficulty levels (Easy, Medium, Hard)
- Multiple-choice format (A / B / C / D)
- Random question order each run
- 15-second visible countdown timer per question
- Warning at 5 seconds remaining
- Shows time taken per answer
- Score calculation with percentage and letter grade
- Results saved to scores.txt with timestamps
- Option to replay at a different difficulty without restarting
- Coloured terminal output

## How to Run

1. Make sure Python 3.6+ is installed.
2. Open a terminal in the project folder.
3. Run:

```
python quiz.py
```

4. Choose a difficulty and answer the questions.

## Project Structure

```
AI_Quiz_Generator/
    quiz.py          Main application
    questions.txt    Question bank
    scores.txt       Score history (created on first run)
    README.md        This file
```

## Technologies

- Python 3
- File I/O (question loading and score saving)
- random (question shuffling)
- time (answer timer)
- threading (background countdown)
- dataclasses (question model)
- ANSI escape codes (coloured output)

## Sample Output

```
==================================================
            AI Quiz Generator
          Internship Mini Project
==================================================

Loaded 15 questions.
Time limit: 15 seconds per question.

Select difficulty:
  1) Easy
  2) Medium
  3) Hard
  4) All (mixed)
Enter 1-4: 1

--------------------------------------------------
Question 1/5  [Easy]  Timer: 15s
--------------------------------------------------

What is Python?

  A) A web browser
  B) A programming language
  C) An operating system
  D) A database

You have 15 seconds to answer...

Your answer (A/B/C/D): B
(Answered in 3.2s)
Correct!

==================================================
  Score      : 4/5
  Percentage : 80.0%
  Grade      : A
==================================================
Result saved to scores.txt

Try another difficulty? (y/n): n
Thanks for playing! Goodbye.
```

## Author

- **Name:** Pitti Anusha
- **Program:** Python with Generative AI Internship
- **Organization:** Think Champ PV LTD
- **Date:** May 2026
