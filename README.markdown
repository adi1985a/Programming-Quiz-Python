# 🧠✅ PyQuiz Master: Tkinter Knowledge Testing System 📈
_A Python application for conducting interactive quizzes in single-choice, multiple-choice, and open-ended formats, featuring a Tkinter GUI, SQLite database storage, and Matplotlib progress visualization._

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) <!-- Assuming MIT if not specified -->
[![Python](https://img.shields.io/badge/Python-3.6%2B-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange.svg)]() <!-- Generic Tkinter badge -->
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57.svg?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Matplotlib](https://img.shields.io/badge/Charts-Matplotlib-89A7D2.svg?logo=matplotlib)](https://matplotlib.org/)

## 📋 Table of Contents
1.  [Overview](#-overview)
2.  [Key Features](#-key-features)
3.  [Screenshots (Conceptual)](#-screenshots-conceptual)
4.  [System Requirements & Dependencies](#-system-requirements--dependencies)
5.  [Database Schema & Content](#-database-schema--content)
6.  [Installation and Setup](#️-installation-and-setup)
7.  [Application Usage](#️-application-usage)
8.  [File Structure (Expected)](#-file-structure-expected)
9.  [Technical Notes](#-technical-notes)
10. [Contributing](#-contributing)
11. [License](#-license)
12. [Contact](#-contact)

## 📄 Overview

**PyQuiz Master**, developed by Adrian Lesniak, is an interactive knowledge testing system built with Python. It provides a versatile platform for conducting quizzes in three different formats: **single-choice**, **multiple-choice**, and **open-ended questions**. The application leverages an **SQLite** database to store a repository of questions and to track user test results over time. It features automatic answer evaluation, scorekeeping, and visualizes learning progress through charts generated with **Matplotlib**. The entire user experience is managed through an intuitive Graphical User Interface (GUI) created with Python's standard **Tkinter** library.

## ✨ Key Features

*   📝 **Multiple Test Formats**:
    *   **Single-Choice Questions**: Users select one correct answer from a list of options.
    *   **Multiple-Choice Questions**: Users can select one or more correct answers from a list.
    *   **Open-Ended Questions**: Users type their answers into a text field.
*   💾 **SQLite Database Integration**:
    *   **Questions Storage**: All quiz questions, options, and correct answers are stored in a persistent SQLite database.
    *   **Results Tracking**: User scores, test types, and dates of completion are saved to the database, allowing for historical performance analysis.
*   ✔️ **Automatic Answer Evaluation**:
    *   The application automatically checks user-submitted answers against the correct answers stored in the database.
    *   Awards points based on correctness for each question.
*   📈 **Learning Progress Visualization**:
    *   A "Show Progress" feature uses **Matplotlib** to generate and display charts (e.g., line charts, bar charts) that visualize user performance and scores over time.
*   🖥️ **Tkinter Graphical User Interface (GUI)**:
    *   An intuitive and easy-to-navigate GUI for taking tests and viewing results.
    *   Features include a menu bar, question display areas, input widgets (radio buttons, checkboxes, text entries), and feedback messages.
*   📚 **Preloaded Question Bank**: The database is pre-populated with questions covering topics like networking, programming (Python, C++), and databases upon first startup.

## 🖼️ Screenshots (Conceptual)

**Coming soon!**

_This section would ideally show screenshots of the PyQuiz Master application, including: the main menu, an example of a single-choice question, a multiple-choice question, an open-ended question, and the Matplotlib chart displaying user progress._

## ⚙️ System Requirements & Dependencies

### Software:
*   **Python**: Version 3.6 or higher.
*   **Libraries**:
    *   `tkinter`: For the graphical user interface. (Usually included with standard Python installations).
    *   `sqlite3`: For database interaction. (Included with standard Python installations).
    *   `matplotlib`: For generating progress charts.
    *   `random`: For shuffling question options.
    *   `datetime`: For timestamping test results.

### Installation of Dependencies:
*   `matplotlib` is the primary external library that needs to be installed using `pip`.

## 💾 Database Schema & Content

The application uses an SQLite database (e.g., `quiz_database.db`) with two main tables:

1.  **`questions` Table**:
    *   Stores the quiz questions and related data.
    *   **Example Schema**: `id INTEGER PRIMARY KEY, question_text TEXT, question_type TEXT, correct_answer TEXT, options TEXT`.
    *   `question_type` would be 'single', 'multiple', or 'open'.
    *   `correct_answer` and `options` would likely be stored as JSON strings or delimited text.
2.  **`results` Table**:
    *   Stores the history of completed tests.
    *   **Example Schema**: `id INTEGER PRIMARY KEY, test_type TEXT, points_scored INTEGER, total_points INTEGER, test_date TEXT`.

The database is initialized with a set of questions on topics like networking, programming, and databases, managed by a script like `database.py` (assumed).

## 🛠️ Installation and Setup

1.  **Clone the Repository**:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```
    *(Replace `<repository-url>` and `<repository-directory>` with your specific details).*

2.  **Set Up a Virtual Environment (Recommended)**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Required Libraries**:
    Activate your virtual environment and run:
    ```bash
    pip install matplotlib
    ```
    *(Tkinter and sqlite3 are usually part of the Python standard library, so they don't need to be installed separately via pip).*

4.  **Prepare Database (if needed)**:
    *   The application is designed to automatically create and populate the SQLite database on its first run via logic contained in `database.py` (assumed).
    *   Ensure you have write permissions in the project directory for the database file to be created.

5.  **Run the Application**:
    Open a terminal or command prompt in the project's root directory and execute:
    ```bash
    python main.py
    ```

## 💡 Application Usage

1.  Launch the application by running `python main.py` after completing the setup.
2.  **Main Window & Menu**:
    *   The main application window will appear with a menu bar at the top.
    *   The "Tests" menu will contain options to start a quiz:
        *   Single Choice Test
        *   Multiple Choice Test
        *   Open Questions Test
    *   There will also be an option to "Show Progress".
3.  **Taking a Test**:
    *   Select a test type from the "Tests" menu to begin.
    *   A question will be displayed.
    *   **For Single-Choice**: Select one answer using radio buttons.
    *   **For Multiple-Choice**: Select one or more answers using checkboxes.
    *   **For Open-Ended**: Type your answer into the text entry field.
    *   Click the "Next Question" (or similar) button to submit your answer.
    *   The application will provide immediate feedback (e.g., "Correct!" or "Incorrect.") and update your score.
    *   Continue until all questions in the test are answered.
4.  **Viewing Progress**:
    *   From the main menu, select the "Show Progress" option.
    *   A new window will appear displaying a **Matplotlib chart** that visualizes your past test scores, showing your learning progress over time.
5.  **Exiting**: Close the main window to exit the application.

## 🗂️ File Structure (Expected)

*   `main.py`: The main Python script that initializes the Tkinter application, sets up the GUI, handles user interactions, and orchestrates the test-taking and progress-viewing logic.
*   `database.py`: (Assumed) A separate Python module containing functions for all database-related operations:
    *   Creating the initial database and tables.
    *   Inserting the predefined set of questions.
    *   Fetching questions for a test.
    *   Saving test results.
    *   Retrieving historical results for charting.
*   `quiz_database.db`: (Generated on first run) The SQLite database file where all questions and results are stored.
*   `README.md`: This documentation file.

## 📝 Technical Notes

*   **GUI Framework**: The application's user interface is built entirely with **Tkinter**, Python's standard GUI toolkit, making it cross-platform without requiring extra GUI library installations.
*   **Database Management**: The use of `sqlite3` makes the database self-contained and file-based, requiring no separate database server setup. Logic for database creation and seeding is likely handled within `database.py`.
*   **Progress Charting**: The integration of **Matplotlib** allows for powerful and flexible data visualization, providing users with tangible feedback on their performance. The chart is typically embedded within a Tkinter window.
*   **Error Handling**: A robust implementation would include error handling for database operations (e.g., file permissions, SQL errors) and potentially invalid data formats if the database were to be manually edited.
*   **Modularity**: Separating database logic into a `database.py` module is a good practice for maintainability and separation of concerns.

## 🤝 Contributing

Contributions to **PyQuiz Master** are highly encouraged! If you have ideas for:

*   Adding new question types or test formats.
*   Expanding the question database with more topics.
*   Enhancing the progress visualization with different chart types or more detailed analytics.
*   Improving the Tkinter UI/UX with better layouts or custom widgets.
*   Implementing user accounts to track progress for multiple users.
*   Adding features like timed quizzes or hints.

1.  Fork the repository.
2.  Create a new branch for your feature (`git checkout -b feature/UserAccounts`).
3.  Make your changes to the Python scripts.
4.  Commit your changes (`git commit -m 'Feature: Implement multi-user support'`).
5.  Push to the branch (`git push origin feature/UserAccounts`).
6.  Open a Pull Request.

Please ensure your code is well-commented, follows Python best practices (e.g., PEP 8), and includes type hints where appropriate.

## 📃 License

This project is licensed under the **MIT License**.
(If you have a `LICENSE` file in your repository, refer to it: `See the LICENSE file for details.`)

## 📧 Contact

Project concept by **Adrian Lesniak**.
For questions, feedback, or issues, please open an issue on the GitHub repository or contact the repository owner.

---
🎓 _Test your knowledge and track your learning progress with this interactive quiz application!_
