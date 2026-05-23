"""AI Quiz Generator

Terminal-based quiz app built for the Python with Generative AI
internship at Think Champ PV LTD.

Features
--------
- Loads MCQ questions from questions.txt
- Difficulty selection (easy / medium / hard / all)
- Shuffles questions each run
- 15-second visible countdown timer per question
- Score, percentage, and letter grade
- Saves every result to scores.txt with a timestamp
- Option to play again at a different difficulty without restarting
"""

import os
import random
import time
import threading
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List

# ---- settings ----
QUESTIONS_FILE = "questions.txt"
SCORES_FILE    = "scores.txt"
TIME_LIMIT     = 15          # seconds per question

# ---- terminal colours (ANSI) ----
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BLUE   = "\033[94m"
BOLD   = "\033[1m"
RESET  = "\033[0m"


@dataclass
class Question:
    difficulty: str
    text: str
    options: Dict[str, str]
    answer: str                # A, B, C or D


# ---------- loading questions ----------

def load_questions(filepath: str = QUESTIONS_FILE) -> List[Question]:
    """Read questions from a pipe-delimited text file."""
    if not os.path.exists(filepath):
        print(f"{RED}Error: {filepath} not found.{RESET}")
        return []

    questions: List[Question] = []
    with open(filepath, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) != 7:
                continue
            diff, text, opt_a, opt_b, opt_c, opt_d, correct = parts
            if correct.upper() not in ("A", "B", "C", "D"):
                continue
            questions.append(
                Question(
                    difficulty=diff.lower(),
                    text=text,
                    options={"A": opt_a, "B": opt_b, "C": opt_c, "D": opt_d},
                    answer=correct.upper(),
                )
            )
    return questions


# ---------- difficulty selection ----------

def pick_difficulty() -> str:
    """Let the user choose a difficulty level."""
    print("\nSelect difficulty:")
    print("  1) Easy")
    print("  2) Medium")
    print("  3) Hard")
    print("  4) All (mixed)")
    choices = {"1": "easy", "2": "medium", "3": "hard", "4": "all"}
    while True:
        sel = input("Enter 1-4: ").strip()
        if sel in choices:
            return choices[sel]
        print(f"{YELLOW}Invalid choice. Type 1, 2, 3 or 4.{RESET}")


def filter_questions(questions: List[Question], level: str) -> List[Question]:
    if level == "all":
        return list(questions)
    return [q for q in questions if q.difficulty == level]


# ---------- timer ----------

def countdown_timer(seconds: int, stop_event: threading.Event) -> None:
    """Background thread that prints a warning when time runs out."""
    remaining = seconds
    while remaining > 0 and not stop_event.is_set():
        time.sleep(1)
        remaining -= 1
        # show warning at 5 seconds remaining
        if remaining == 5 and not stop_event.is_set():
            print(f"\n{YELLOW}>>> 5 seconds remaining! <<<{RESET}")
    if not stop_event.is_set():
        print(f"\n{RED}>>> Time's up! ({seconds}s) <<<{RESET}")


# ---------- asking a single question ----------

def ask_question(q: Question, number: int, total: int) -> bool:
    """Display one question with timer, collect answer, return True if correct."""
    # difficulty tag colour
    tag_colour = {"easy": GREEN, "medium": YELLOW, "hard": RED}.get(
        q.difficulty, BLUE
    )

    print(f"\n{'-' * 50}")
    print(f"Question {number}/{total}  "
          f"[{tag_colour}{q.difficulty.capitalize()}{RESET}]  "
          f"{CYAN}Timer: {TIME_LIMIT}s{RESET}")
    print(f"{'-' * 50}")
    print(f"\n{BOLD}{q.text}{RESET}\n")
    for letter in ("A", "B", "C", "D"):
        print(f"  {letter}) {q.options[letter]}")

    # start background timer
    stop_event = threading.Event()
    timer_thread = threading.Thread(
        target=countdown_timer,
        args=(TIME_LIMIT, stop_event),
        daemon=True
    )

    print(f"\n{CYAN}You have {TIME_LIMIT} seconds to answer...{RESET}")

    start_time = time.time()
    timer_thread.start()

    # get user input
    try:
        user_input = input("\nYour answer (A/B/C/D): ").strip().upper()
    except EOFError:
        user_input = ""

    elapsed = time.time() - start_time
    stop_event.set()  # stop the background timer

    # show time taken
    print(f"{BLUE}(Answered in {elapsed:.1f}s){RESET}")

    # check time limit
    if elapsed > TIME_LIMIT:
        print(f"{RED}Too slow! Time limit was {TIME_LIMIT}s.{RESET}")
        print(f"{YELLOW}Correct answer: {q.answer}) {q.options[q.answer]}{RESET}")
        return False

    # validate input
    if user_input not in ("A", "B", "C", "D"):
        print(f"{YELLOW}Invalid input. Answer must be A, B, C or D.{RESET}")
        print(f"{YELLOW}Correct answer: {q.answer}) {q.options[q.answer]}{RESET}")
        return False

    # check correctness
    if user_input == q.answer:
        print(f"{GREEN}Correct!{RESET}")
        return True

    print(f"{RED}Wrong.{RESET}")
    print(f"{YELLOW}Correct answer: {q.answer}) {q.options[q.answer]}{RESET}")
    return False


# ---------- grading ----------

def letter_grade(percent: float) -> str:
    if percent >= 90:
        return "A+"
    if percent >= 80:
        return "A"
    if percent >= 70:
        return "B"
    if percent >= 60:
        return "C"
    if percent >= 50:
        return "D"
    return "F"


# ---------- saving results ----------

def save_score(score: int, total: int, percent: float, grade: str) -> None:
    """Append the result to scores.txt."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"{timestamp} | Score: {score}/{total} | {percent:.1f}% | Grade: {grade}\n"
    with open(SCORES_FILE, "a", encoding="utf-8") as fh:
        fh.write(entry)


# ---------- main loop ----------

def main() -> None:
    # welcome message
    print("=" * 50)
    print("       AI Quiz Generator".center(50))
    print("     Internship Mini Project".center(50))
    print("=" * 50)

    questions = load_questions()
    if not questions:
        print(f"{RED}No questions loaded. Make sure {QUESTIONS_FILE} exists.{RESET}")
        return

    print(f"\n{CYAN}Loaded {len(questions)} questions.{RESET}")
    print(f"{CYAN}Time limit: {TIME_LIMIT} seconds per question.{RESET}")

    # game loop (allows replaying at a different difficulty)
    while True:
        level = pick_difficulty()
        selected = filter_questions(questions, level)

        if not selected:
            print(f"{YELLOW}No questions found for that level. Try another.{RESET}")
            continue

        random.shuffle(selected)
        total = len(selected)
        score = 0

        print(f"\n{CYAN}Starting {total} questions. Good luck!{RESET}")

        for i, q in enumerate(selected, start=1):
            if ask_question(q, i, total):
                score += 1

        # results
        percent = (score / total) * 100
        grade = letter_grade(percent)

        print("\n" + "=" * 50)
        print(f"  Score      : {score}/{total}")
        print(f"  Percentage : {percent:.1f}%")
        print(f"  Grade      : {grade}")
        print("=" * 50)

        save_score(score, total, percent, grade)
        print(f"{GREEN}Result saved to {SCORES_FILE}{RESET}")

        # ask to continue
        again = input("\nTry another difficulty? (y/n): ").strip().lower()
        if again != "y":
            print(f"\n{CYAN}Thanks for playing! Goodbye.{RESET}")
            break


if __name__ == "__main__":
    main()
