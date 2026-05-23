# 🤖 AI Quiz Generator

> **Python with Generative AI Internship Mini Project**  
> Think Champ PV LTD

---

## 📖 Project Overview

The **AI Quiz Generator** is a Python-based terminal application that automatically asks quiz questions, accepts user answers, validates them, calculates scores, and displays results. It simulates a basic AI assistant interaction through the command line.

---

## ✨ Features

### Mandatory Features
- ✅ Welcome Message with colorful banner
- ✅ Minimum 5+ Quiz Questions (15 included!)
- ✅ User Answer Input via terminal
- ✅ Answer Validation (case-insensitive)
- ✅ Score Calculation
- ✅ Loop for Multiple Questions
- ✅ Final Result Display with grade
- ✅ Save Score in Text File with timestamp

### Optional / Bonus Features
- ⏱️ **Timer** – 15-second countdown per question using multithreading
- 🔤 **Multiple Choice Questions** – A/B/C/D options
- 📊 **Difficulty Levels** – Easy, Medium, Hard, or Mixed
- 🔀 **Random Questions** – Questions are shuffled each run
- 🎨 **Colored Output** – ANSI color codes (no external library required)

---

## 🚀 How to Run

### Prerequisites
- Python 3.6 or higher

### Steps
1. Clone or download this project folder.
2. Open a terminal/command prompt in the project directory.
3. Run the following command:
   ```bash
   python quiz.py
   ```
4. Follow the on-screen prompts to:
   - Choose a difficulty level
   - Answer the quiz questions
   - View your final score and grade

---

## 📁 Project Structure

```
AI_Quiz_Generator/
│
├── quiz.py           # Main Python application
├── questions.txt     # Quiz questions database
├── scores.txt        # Auto-generated score history (created after first run)
└── README.md         # Project documentation (this file)
```

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.x | Core programming language |
| Threading | Timer functionality |
| Random | Question shuffling |
| File I/O | Loading questions & saving scores |
| ANSI Codes | Colored terminal output |

---

## 📸 Sample Output

```
╔══════════════════════════════════════════════════╗
║                                                  ║
║        🤖  AI QUIZ GENERATOR  🤖                ║
║                                                  ║
║   Python with Generative AI Internship Project   ║
║              Think Champ PV LTD                  ║
║                                                  ║
╚══════════════════════════════════════════════════╝

📚 15 questions loaded successfully!

📊 Choose Difficulty Level:
   1) Easy
   2) Medium
   3) Hard
   4) All (Mixed)

──────────────────────────────────────────────────
Question 1/5  [Easy]  ⏱️  15 seconds
──────────────────────────────────────────────────

What is Python?

   A) A web browser
   B) A programming language
   C) An operating system
   D) A database

Your Answer (A/B/C/D): B
✅ Correct!

══════════════════════════════════════════════════
           📋 FINAL RESULTS 📋
══════════════════════════════════════════════════
   Total Questions  : 5
   Correct Answers  : 4
   Wrong Answers    : 1
   Percentage       : 80.0%
   Grade            : A (Great Job!)
══════════════════════════════════════════════════

💾 Score saved to 'scores.txt' successfully!
Thank you for playing AI Quiz Generator! 🎉
```

---

## 👤 Author

- **Name:** [Your Name]
- **Program:** Python with Generative AI Internship
- **Organization:** Think Champ PV LTD
- **Date:** May 2026

---

## 📄 License

This project is created as part of the Think Champ internship program.
