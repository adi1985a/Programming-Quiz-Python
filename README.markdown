# 🎓📝 Programming Quiz Pro: Interactive IT Knowledge System 🧠
_A Python desktop application using Tkinter for interactive IT/programming quizzes with single-choice, multiple-choice, and open-ended questions, user accounts, achievements, learning mode, and a modern GUI._

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.6%2B-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange.svg)]()
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57.svg?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Matplotlib](https://img.shields.io/badge/Visualization-Matplotlib-informational.svg?logo=matplotlib)](https://matplotlib.org/)

## 📋 Table of Contents
1.  [Overview](#-overview)
2.  [Key Features](#-key-features)
3.  [Screenshots (Conceptual)](#-screenshots-conceptual)
4.  [System Requirements & Dependencies](#-system-requirements--dependencies)
5.  [Database Schema](#-database-schema)
6.  [Core Modules](#-core-modules)
7.  [Installation and Setup](#️-installation-and-setup)
8.  [Application Usage](#️-application-usage)
9.  [File Structure](#-file-structure)
10. [Technical Notes](#-technical-notes)
11. [Contributing](#-contributing)
12. [License](#-license)
13. [Contact](#-contact)

## 📄 Overview

**Programming Quiz Pro** is a modern Python application for interactive IT and programming quizzes. Developed by Adrian Lesniak, it supports single-choice, multiple-choice, and open-ended questions, user registration and login, achievements, ranking, learning mode, and a beautiful, responsive GUI. All user progress, results, and questions are stored in an **SQLite database**. The app features a real-time message/info window, no pop-up dialogs, and supports import/export of questions and multiple color themes.

<br>
<p align="center">
  <img src="screenshots/1.gif" width="90%">
</p>
<br>

## ✨ Key Features

*   👤 **User Accounts**: Registration, login, user-specific results, achievements, and ranking.
*   🏆 **Achievements & Ranking**: Earn badges for quiz mastery, streaks, high scores, and see your position in the global ranking.
*   🤔 **Diverse Test Formats**: Single-choice, multiple-choice, and open-ended questions.
*   📚 **Learning Mode**: Practice questions with hints, error tracking, and the ability to retry questions.
*   💬 **Integrated Info Window**: All feedback, hints, errors, and results are shown in a scrollable info window at the bottom of the main window (no pop-up dialogs).
*   💾 **SQLite Database**: Stores users, questions, results, achievements, and supports import/export of questions (JSON).
*   🎨 **Modern Tkinter GUI**: Responsive, color themes (light/dark), large info window, clear navigation, and accessibility.
*   📈 **Progress Visualization**: View your progress and statistics with Matplotlib charts.
*   🗃️ **Database Preloading**: Rich set of IT/programming questions preloaded on first run.
*   🔄 **Import/Export Questions**: Easily manage your own question sets.

## 🖼️ Screenshots (Conceptual)

_Screenshots of: login/registration, main menu, quiz types, learning mode, achievements, ranking, and info window._

<p align="center">
  <img src="screenshots/1.jpg" width="300"/>
  <img src="screenshots/2.jpg" width="300"/>
  <img src="screenshots/3.jpg" width="300"/>
  <img src="screenshots/4.jpg" width="300"/>
  <img src="screenshots/5.jpg" width="300"/>
  <img src="screenshots/6.jpg" width="300"/>
</p>

## ⚙️ System Requirements & Dependencies

*   **Python Version**: Python 3.6 or higher.
*   **Operating System**: Windows, Linux, or macOS (Tkinter and SQLite included with Python).
*   **Standard Python Libraries**: `tkinter`, `sqlite3`, `random`, `datetime`, `os`, `json`.
*   **External Libraries**: `matplotlib` (for charts).

## 💾 Database Schema

The application uses an SQLite database with the following tables:

- **users**: id, username, email, password (hashed)
- **questions**: id, question, type, correct_answer, incorrect_options, hint
- **results**: id, user_id, type, points, date
- **achievements**: id, user_id, name, description, date

## 🧩 Core Modules

*   `main.py`: Main application logic, GUI orchestration, user session, navigation.
*   `gui.py`: All Tkinter GUI screens, info window, quiz/learning mode logic.
*   `user.py`: User management, registration, login, stats, ranking, achievements.
*   `quiz.py`: Quiz logic, answer checking, lifelines, progress.
*   `database.py`: Database creation, schema, question/result/achievement management.
*   `logger.py`: Error logging.

## 🛠️ Installation and Setup

1.  **Clone or Download the Repository**:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```
2.  **Set Up a Virtual Environment (Recommended)**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install Required Libraries**:
    ```bash
    pip install matplotlib
    ```
4.  **Run the Application**:
    ```bash
    python main.py
    ```

## 💡 Application Usage

1.  **Register or log in** to your account.
2.  Use the **main menu** to start a quiz, enter learning mode, view your records, achievements, statistics, or ranking.
3.  In **quiz mode**, answer questions, use lifelines (50/50, hint, skip), and watch the timer. All feedback appears in the info window at the bottom.
4.  In **learning mode**, practice questions with hints and see your mistakes. Info window shows all feedback.
5.  Use **Import/Export** to manage your own question sets.
6.  **Switch between light and dark themes** for your comfort.
7.  All your results and achievements are saved to your account.

## 🗂️ File Structure

*   `main.py`
*   `gui.py`
*   `user.py`
*   `quiz.py`
*   `database.py`
*   `logger.py`
*   `knowledge_tests.db`
*   `README.markdown`
*   `screenshots/`

## 📝 Technical Notes

*   **No pop-up dialogs**: All feedback, errors, and hints are shown in the info window.
*   **User accounts**: Each user has their own results, achievements, and stats.
*   **Learning mode**: Practice with hints, error tracking, and retry.
*   **Achievements**: Earn badges for quiz mastery, streaks, high scores, and more.
*   **Ranking**: See your position among all users.
*   **Import/Export**: Manage your own question sets (JSON).
*   **Modern GUI**: Large, scrollable info window, color themes, accessibility.

## 🤝 Contributing

Contributions are welcome! Please fork the repository, create a branch, and submit a pull request. See the original instructions for details.

## 📃 License

This project is licensed under the **MIT License**.

## 📧 Contact

Application concept by **Adrian Lesniak**.
For questions, feedback, or issues, please open an issue on the GitHub repository or contact the repository owner.

---
📚 _Test your IT knowledge and track your learning journey!_
