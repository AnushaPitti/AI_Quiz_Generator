import os
import random
import time
import threading

# =============================================
#          AI QUIZ GENERATOR
#   Python with Generative AI Internship
#          Think Champ PV LTD
# =============================================

# ----- ANSI Color Codes (No external library needed) -----
class Color:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"


def print_banner():
    """Display a colorful welcome banner."""
    print(f"""
{Color.CYAN}{Color.BOLD}╔══════════════════════════════════════════════════╗
║                                                  ║
║        🤖  AI QUIZ GENERATOR  🤖                ║
║                                                  ║
║   Python with Generative AI Internship Project   ║
║              Think Champ PV LTD                  ║
║                                                  ║
╚══════════════════════════════════════════════════╝{Color.RESET}
""")


def load_questions(filename="questions.txt"):
    """
    Load questions from a text file.
    Format per line: difficulty|question|option_a|option_b|option_c|option_d|correct_option_letter
    Lines starting with '#' are treated as comments/headers.
    """
    questions = []
    if not os.path.exists(filename):
        print(f"{Color.RED}Error: '{filename}' not found! Please make sure it exists.{Color.RESET}")
        return questions

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("|")
            if len(parts) == 7:
                questions.append({
                    "difficulty": parts[0].strip().lower(),
                    "question":   parts[1].strip(),
                    "options": {
                        "A": parts[2].strip(),
                        "B": parts[3].strip(),
                        "C": parts[4].strip(),
                        "D": parts[5].strip(),
                    },
                    "answer": parts[6].strip().upper()
                })
    return questions


def choose_difficulty(questions):
    """Let the user select a difficulty level or play all."""
    available = sorted(set(q["difficulty"] for q in questions))
    print(f"{Color.YELLOW}{Color.BOLD}📊 Choose Difficulty Level:{Color.RESET}")
    print(f"   {Color.GREEN}1) Easy{Color.RESET}")
    print(f"   {Color.YELLOW}2) Medium{Color.RESET}")
    print(f"   {Color.RED}3) Hard{Color.RESET}")
    print(f"   {Color.CYAN}4) All (Mixed){Color.RESET}")
    print()

    while True:
        choice = input(f"{Color.BOLD}Enter your choice (1-4): {Color.RESET}").strip()
        if choice == "1":
            return [q for q in questions if q["difficulty"] == "easy"]
        elif choice == "2":
            return [q for q in questions if q["difficulty"] == "medium"]
        elif choice == "3":
            return [q for q in questions if q["difficulty"] == "hard"]
        elif choice == "4":
            return questions
        else:
            print(f"{Color.RED}Invalid choice. Please enter 1, 2, 3, or 4.{Color.RESET}")


def ask_question(q, index, total, timer_seconds=15):
    """
    Display a question with options and a countdown timer.
    Returns True if answered correctly, False otherwise.
    """
    answered = threading.Event()
    user_answer = [None]

    # Difficulty color
    diff_colors = {"easy": Color.GREEN, "medium": Color.YELLOW, "hard": Color.RED}
    diff_color = diff_colors.get(q["difficulty"], Color.WHITE)

    print(f"\n{Color.BOLD}{'─' * 50}{Color.RESET}")
    print(f"{Color.BOLD}{Color.BLUE}Question {index}/{total}{Color.RESET}  "
          f"[{diff_color}{q['difficulty'].capitalize()}{Color.RESET}]  "
          f"⏱️  {timer_seconds} seconds")
    print(f"{Color.BOLD}{'─' * 50}{Color.RESET}")
    print(f"\n{Color.WHITE}{Color.BOLD}{q['question']}{Color.RESET}\n")

    for key in ["A", "B", "C", "D"]:
        print(f"   {Color.CYAN}{key}){Color.RESET} {q['options'][key]}")

    print()

    # Timer logic
    def timer_func():
        time.sleep(timer_seconds)
        if not answered.is_set():
            print(f"\n{Color.RED}⏰ Time's up!{Color.RESET}")
            answered.set()

    timer_thread = threading.Thread(target=timer_func, daemon=True)
    timer_thread.start()

    # Get user input
    try:
        raw = input(f"{Color.BOLD}Your Answer (A/B/C/D): {Color.RESET}").strip().upper()
        answered.set()
        if raw in ["A", "B", "C", "D"]:
            user_answer[0] = raw
    except EOFError:
        answered.set()

    # Check answer
    correct = q["answer"]
    if user_answer[0] == correct:
        print(f"{Color.GREEN}✅ Correct!{Color.RESET}")
        return True
    else:
        if user_answer[0] is None:
            print(f"{Color.RED}❌ No valid answer given. "
                  f"The correct answer was: {correct}) {q['options'][correct]}{Color.RESET}")
        else:
            print(f"{Color.RED}❌ Wrong! The correct answer was: "
                  f"{correct}) {q['options'][correct]}{Color.RESET}")
        return False


def display_result(score, total):
    """Display the final result with grade."""
    percentage = (score / total) * 100 if total > 0 else 0

    if percentage >= 90:
        grade, grade_color = "A+ (Excellent!)", Color.GREEN
    elif percentage >= 80:
        grade, grade_color = "A (Great Job!)", Color.GREEN
    elif percentage >= 70:
        grade, grade_color = "B (Good!)", Color.CYAN
    elif percentage >= 60:
        grade, grade_color = "C (Average)", Color.YELLOW
    elif percentage >= 50:
        grade, grade_color = "D (Needs Improvement)", Color.YELLOW
    else:
        grade, grade_color = "F (Try Again!)", Color.RED

    print(f"\n\n{Color.BOLD}{'═' * 50}{Color.RESET}")
    print(f"{Color.BOLD}{Color.MAGENTA}           📋 FINAL RESULTS 📋{Color.RESET}")
    print(f"{Color.BOLD}{'═' * 50}{Color.RESET}")
    print(f"   Total Questions  : {total}")
    print(f"   Correct Answers  : {Color.GREEN}{score}{Color.RESET}")
    print(f"   Wrong Answers    : {Color.RED}{total - score}{Color.RESET}")
    print(f"   Percentage       : {Color.BOLD}{percentage:.1f}%{Color.RESET}")
    print(f"   Grade            : {grade_color}{Color.BOLD}{grade}{Color.RESET}")
    print(f"{Color.BOLD}{'═' * 50}{Color.RESET}\n")

    return percentage, grade


def save_score(score, total, percentage, grade, filename="scores.txt"):
    """Save the quiz result to a text file with a timestamp."""
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"{'=' * 40}\n")
        f.write(f"Date & Time    : {timestamp}\n")
        f.write(f"Score          : {score}/{total}\n")
        f.write(f"Percentage     : {percentage:.1f}%\n")
        f.write(f"Grade          : {grade}\n")
        f.write(f"{'=' * 40}\n\n")

    print(f"{Color.GREEN}💾 Score saved to '{filename}' successfully!{Color.RESET}")


def main():
    """Main function to run the AI Quiz Generator."""
    print_banner()

    # Load questions
    questions = load_questions("questions.txt")
    if not questions:
        print(f"{Color.RED}No questions loaded. Exiting.{Color.RESET}")
        return

    print(f"{Color.CYAN}📚 {len(questions)} questions loaded successfully!{Color.RESET}\n")

    # Choose difficulty
    selected = choose_difficulty(questions)
    if not selected:
        print(f"{Color.RED}No questions available for that difficulty. Exiting.{Color.RESET}")
        return

    # Shuffle for randomness
    random.shuffle(selected)

    total = len(selected)
    score = 0

    print(f"\n{Color.BOLD}{Color.CYAN}🎯 Starting Quiz with {total} questions... Good luck!{Color.RESET}")
    print(f"{Color.YELLOW}(You have 15 seconds per question){Color.RESET}")

    # Ask each question
    for i, q in enumerate(selected, 1):
        if ask_question(q, i, total, timer_seconds=15):
            score += 1

    # Display and save results
    percentage, grade = display_result(score, total)
    save_score(score, total, percentage, grade)

    print(f"{Color.CYAN}{Color.BOLD}Thank you for playing AI Quiz Generator! 🎉{Color.RESET}\n")


if __name__ == "__main__":
    main()
