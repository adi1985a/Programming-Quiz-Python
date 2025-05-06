# Knowledge Testing Application

## Overview
This Python application is an interactive knowledge testing system designed to conduct quizzes in three formats: single-choice, multiple-choice, and open-ended questions. It uses a SQLite database to store questions and results, evaluates user answers, tracks scores, and visualizes learning progress with charts. The graphical user interface (GUI) is built using Tkinter.

## Features
- **Test Formats**: Supports single-choice, multiple-choice, and open-ended questions.
- **Database**: Stores questions and user results in a SQLite database.
- **Answer Evaluation**: Automatically checks answers and awards points based on correctness.
- **Progress Tracking**: Visualizes user performance over time using Matplotlib charts.
- **User Interface**: Intuitive GUI created with Tkinter for easy navigation.

## Requirements
- Python 3.6+
- Libraries:
  - `tkinter` (usually included with Python)
  - `sqlite3` (included with Python)
  - `matplotlib`
  - `random`
  - `datetime`

Install the required library using:
```bash
pip install matplotlib
```

## Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
2. Ensure all required libraries are installed (see Requirements).
3. Run the application:
   ```bash
   python main.py
   ```

## Usage
1. Launch the application to access the main menu.
2. Select a test type (Single Choice, Multiple Choice, or Open Questions) from the "Tests" menu.
3. Answer questions using the provided input fields or checkboxes.
4. Click "Next Question" to proceed and receive feedback on your answer.
5. View your progress by clicking "Show Progress" to display a chart of past results.

## File Structure
- `main.py`: Main application script containing the core logic, GUI, and database interactions.
- `database.py`: (Assumed) Contains functions for creating the database and inserting questions.
- `README.md`: This file, providing project documentation.

## Database
- The application uses SQLite to manage a database with two main tables:
  - `questions`: Stores question data (text, type, correct answer, incorrect options).
  - `results`: Stores test results (test type, points, date).
- Questions are preloaded into the database upon startup, covering topics like networking, programming, and databases.

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For questions or feedback, please open an issue on GitHub or contact the repository owner.