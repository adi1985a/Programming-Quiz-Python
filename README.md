<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Knowledge Testing Application</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            line-height: 1.5;
            color: #24292e;
            max-width: 896px;
            margin: 0 auto;
            padding: 16px;
            background-color: #ffffff;
        }
        h1, h2, h3 {
            margin-top: 24px;
            margin-bottom: 16px;
            font-weight: 600;
            line-height: 1.25;
        }
        h1 {
            font-size: 32px;
            padding-bottom: 0.3em;
            border-bottom: 1px solid #eaecef;
        }
        h2 {
            font-size: 24px;
            padding-bottom: 0.3em;
            border-bottom: 1px solid #eaecef;
        }
        h3 {
            font-size: 20px;
        }
        p {
            margin-top: 0;
            margin-bottom: 16px;
        }
        ul, ol {
            padding-left: 2em;
            margin-top: 0;
            margin-bottom: 16px;
        }
        li {
            margin-bottom: 8px;
        }
        code {
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
            font-size: 85%;
            background-color: #f6f8fa;
            padding: 0.2em 0.4em;
            border-radius: 6px;
        }
        pre {
            background-color: #f6f8fa;
            padding: 16px;
            border-radius: 6px;
            overflow: auto;
            margin-bottom: 16px;
        }
        pre code {
            background-color: transparent;
            padding: 0;
        }
        a {
            color: #0366d6;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        .highlight {
            margin-bottom: 16px;
        }
        .highlight pre {
            margin-bottom: 0;
            word-break: normal;
        }
        .markdown-body {
            box-sizing: border-box;
            min-width: 200px;
            max-width: 980px;
            margin: 0 auto;
            padding: 45px;
        }
        @media (max-width: 767px) {
            .markdown-body {
                padding: 15px;
            }
        }
    </style>
</head>
<body>
    <div class="markdown-body">
        <h1>Knowledge Testing Application</h1>
        <h2>Overview</h2>
        <p>This Python application is an interactive knowledge testing system designed to conduct quizzes in three formats: single-choice, multiple-choice, and open-ended questions. It uses a SQLite database to store questions and results, evaluates user answers, tracks scores, and visualizes learning progress with charts. The graphical user interface (GUI) is built using Tkinter.</p>
        
        <h2>Features</h2>
        <ul>
            <li><strong>Test Formats</strong>: Supports single-choice, multiple-choice, and open-ended questions.</li>
            <li><strong>Database</strong>: Stores questions and user results in a SQLite database.</li>
            <li><strong>Answer Evaluation</strong>: Automatically checks answers and awards points based on correctness.</li>
            <li><strong>Progress Tracking</strong>: Visualizes user performance over time using Matplotlib charts.</li>
            <li><strong>User Interface</strong>: Intuitive GUI created with Tkinter for easy navigation.</li>
        </ul>
        
        <h2>Requirements</h2>
        <ul>
            <li>Python 3.6+</li>
            <li>Libraries:
                <ul>
                    <li><code>tkinter</code> (usually included with Python)</li>
                    <li><code>sqlite3</code> (included with Python)</li>
                    <li><code>matplotlib</code></li>
                    <li><code>random</code></li>
                    <li><code>datetime</code></li>
                </ul>
            </li>
        </ul>
        <p>Install the required library using:</p>
        <div class="highlight">
            <pre><code class="language-bash">pip install matplotlib</code></pre>
        </div>
        
        <h2>Setup</h2>
        <ol>
            <li>Clone the repository:
                <div class="highlight">
                    <pre><code class="language-bash">git clone &lt;repository-url&gt;
cd &lt;repository-directory&gt;</code></pre>
                </div>
            </li>
            <li>Ensure all required libraries are installed (see Requirements).</li>
            <li>Run the application:
                <div class="highlight">
                    <pre><code class="language-bash">python main.py</code></pre>
                </div>
            </li>
        </ol>
        
        <h2>Usage</h2>
        <ol>
            <li>Launch the application to access the main menu.</li>
            <li>Select a test type (Single Choice, Multiple Choice, or Open Questions) from the "Tests" menu.</li>
            <li>Answer questions using the provided input fields or checkboxes.</li>
            <li>Click "Next Question" to proceed and receive feedback on your answer.</li>
            <li>View your progress by clicking "Show Progress" to display a chart of past results.</li>
        </ol>
        
        <h2>File Structure</h2>
        <ul>
            <li><code>main.py</code>: Main application script containing the core logic, GUI, and database interactions.</li>
            <li><code>database.py</code>: (Assumed) Contains functions for creating the database and inserting questions.</li>
            <li><code>README.md</code>: This file, providing project documentation.</li>
        </ul>
        
        <h2>Database</h2>
        <ul>
            <li>The application uses SQLite to manage a database with two main tables:
                <ul>
                    <li><code>questions</code>: Stores question data (text, type, correct answer, incorrect options).</li>
                    <li><code>results</code>: Stores test results (test type, points, date).</li>
                </ul>
            </li>
            <li>Questions are preloaded into the database upon startup, covering topics like networking, programming, and databases.</li>
        </ul>
        
        <h2>Contributing</h2>
        <p>Contributions are welcome! To contribute:</p>
        <ol>
            <li>Fork the repository.</li>
            <li>Create a new branch (<code>git checkout -b feature-branch</code>).</li>
            <li>Make your changes and commit (<code>git commit -m "Add feature"</code>).</li>
            <li>Push to the branch (<code>git push origin feature-branch</code>).</li>
            <li>Open a pull request.</li>
        </ol>
        
        <h2>License</h2>
        <p>This project is licensed under the MIT License. See the <a href="LICENSE">LICENSE</a> file for details.</p>
        
        <h2>Contact</h2>
        <p>For questions or feedback, please open an issue on GitHub or contact the repository owner.</p>
    </div>
</body>
</html>
