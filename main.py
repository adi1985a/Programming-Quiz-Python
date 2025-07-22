"""
Programming Quiz Application
Author: Adrian Lesniak

Description:
This is a cross-platform quiz application for IT knowledge testing. It allows users to solve single choice, multiple choice, and open questions. The program saves results, shows progress, and provides a user-friendly, colorful graphical interface. All options are available from the menu. After each action, you can return to the main menu by pressing a button.

Menu options:
- Single Choice: Start a quiz with single-answer questions.
- Multiple Choice: Start a quiz with multiple-answer questions.
- Open Questions: Start a quiz with open-ended questions.
- Show Progress: Display your learning progress in a chart.

All interface elements, questions, and messages are in English. The application features error logging, file saving/loading, and is designed for clarity and ease of use.
"""
import tkinter as tk
from tkinter import messagebox
import sqlite3
import random
import matplotlib.pyplot as plt
from datetime import datetime
from database import create_database, insert_question  # Import database functions
from tkinter import ttk
from tkinter import Checkbutton, IntVar
import logging
from logger import log_error
import json
import os
import tkinter as tk
from gui import LoginScreen, RegisterScreen, MainMenuScreen, QuizScreen, ResultsScreen, AchievementsScreen, LearningModeScreen
from user import User
from quiz import Quiz

# Configure logging
logging.basicConfig(
    filename='log.txt',
    level=logging.ERROR,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Global variables
questions = []
current_question = 0
points = 0
current_test_type = None
question_label = None
answer_entry = None
next_button = None
submit_button = None
checkbox_vars = []
checkbox_frame = None

# Establish database connection
try:
    conn = create_database()
    if conn is None:
        raise Exception("Failed to connect to the database.")
except Exception as e:
    log_error(str(e))
    messagebox.showerror("Critical Error", "Database connection failed. See log.txt for details.")
    exit()

def migrate_results_table():
    conn = create_database()
    c = conn.cursor()
    # Sprawdź czy kolumna user_id istnieje
    c.execute("PRAGMA table_info(results)")
    columns = [row[1] for row in c.fetchall()]
    if 'user_id' not in columns:
        # Stwórz nową tabelę
        c.execute('''CREATE TABLE IF NOT EXISTS results_new (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            points INTEGER NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )''')
        # Przenieś stare dane (bez user_id, przypisz user_id=1 lub NULL)
        try:
            c.execute("SELECT id, type, points, date FROM results")
            for row in c.fetchall():
                c.execute("INSERT INTO results_new (id, user_id, type, points, date) VALUES (?, ?, ?, ?, ?)", (row[0], 1, row[1], row[2], row[3]))
        except Exception:
            pass
        c.execute("DROP TABLE results")
        c.execute("ALTER TABLE results_new RENAME TO results")
        conn.commit()
    conn.close()

# Wywołaj migrację na starcie
migrate_results_table()

# Function to generate single-choice test
def generate_single_choice(question, correct, incorrect):
    options = incorrect.split(",") + [correct]
    random.shuffle(options)
    return options

# Function to check the answer
def check_answer(type, user_answer, correct_answer):
    if type == "multiple":
        correct_answers = set(correct_answer.split(","))
        selected_answers = set()
        options = questions[current_question][4].split(",")
        for i, var in enumerate(checkbox_vars):
            if var.get() == 1:
                selected_answers.add(options[i])
        return selected_answers == correct_answers
    elif type == "single":
        # For single choice, exact match is required
        return user_answer.strip().lower() == correct_answer.strip().lower()
    elif type == "open":
        # For open questions, check if key words are present
        user_answer = user_answer.lower()
        correct_answer = correct_answer.lower()
        # Check for at least 3 key words from the correct answer
        key_words = [word for word in correct_answer.split() if len(word) > 3][:5]
        matches = sum(1 for word in key_words if word in user_answer)
        return matches >= 2  # At least 2 key words must match

# Function to start the test
def start_test(type):
    global current_question, questions, points, current_test_type, next_button
    current_question = 0
    points = 0
    current_test_type = type
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM questions WHERE type=?", (type,))
        questions = c.fetchall()
    except Exception as e:
        log_error(f"Database error in start_test: {e}")
        messagebox.showerror("Database Error", "Could not load questions. See log.txt for details.")
        return
    if not questions:
        messagebox.showinfo("Error", "No questions available for this test type!")
        return
    random.shuffle(questions)
    next_button.config(state=tk.NORMAL)
    show_question()

def show_question():
    global current_question, question_label, answer_entry, questions, next_button, checkbox_frame, checkbox_vars
    if current_question < len(questions):
        question_data = questions[current_question]
        question_label.config(text=f"Question {current_question + 1}/{len(questions)}:\n\n{question_data[1]}")
        
        # Clear previous answer widgets
        if checkbox_frame:
            checkbox_frame.destroy()
        answer_entry.delete(0, tk.END)
        
        if question_data[2] == "multiple":
            # Show checkboxes for multiple choice
            answer_entry.pack_forget()
            answer_label.pack_forget()
            checkbox_frame = tk.Frame(answer_frame)
            checkbox_frame.pack(pady=10)
            checkbox_vars.clear()
            
            options = question_data[4].split(",")
            for option in options:
                var = IntVar()
                checkbox_vars.append(var)
                Checkbutton(checkbox_frame, text=option, variable=var).pack(anchor='w')
        else:
            # Show text entry for other types
            answer_entry.pack(side=tk.LEFT, padx=5)
            answer_label.pack(side=tk.LEFT, padx=5)
            answer_entry.config(state=tk.NORMAL)
        
        next_button.config(state=tk.NORMAL)
    else:
        question_label.config(text=f"Test completed!\nYour score: {points}/{len(questions)}")
        if checkbox_frame:
            checkbox_frame.destroy()
        answer_entry.config(state=tk.DISABLED)
        next_button.config(state=tk.DISABLED)
        save_result(current_test_type, points)
        show_return_to_menu()

# Add missing next_question function

def next_question():
    global current_question, points
    if current_question < len(questions):
        if questions[current_question][2] == "multiple":
            if any(var.get() for var in checkbox_vars):
                correct_answer = questions[current_question][3]
                if check_answer("multiple", None, correct_answer):
                    points += 1
                    messagebox.showinfo("Correct!", "Your answer is correct!")
                else:
                    messagebox.showinfo("Incorrect", f"Correct answers were: {correct_answer}")
                current_question += 1
                show_question()
            else:
                messagebox.showwarning("Warning", "Please select at least one answer.")
        else:
            user_answer = answer_entry.get().strip()
            if user_answer:  # Only check if answer is not empty
                correct_answer = questions[current_question][3]
                if check_answer(current_test_type, user_answer, correct_answer):
                    points += 1
                    messagebox.showinfo("Correct!", "Your answer is correct!")
                else:
                    messagebox.showinfo("Incorrect", f"Correct answer was: {correct_answer}")
                current_question += 1
                show_question()
            else:
                messagebox.showwarning("Warning", "Please enter an answer before continuing.")

# Add return to menu button
def show_return_to_menu():
    def return_to_menu():
        question_label.config(text="Select a test type to begin")
        answer_entry.config(state=tk.NORMAL)
        answer_entry.delete(0, tk.END)
        next_button.config(state=tk.DISABLED)
        if hasattr(show_return_to_menu, 'btn') and show_return_to_menu.btn:
            show_return_to_menu.btn.destroy()
    show_return_to_menu.btn = tk.Button(main_frame, text="Return to Menu", bg="#b3e6cc", fg="#003300", font=("Arial", 11, "bold"), command=return_to_menu)
    show_return_to_menu.btn.pack(pady=10)

# Function to save the result
def save_result(type, points):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        c = conn.cursor()
        c.execute("INSERT INTO results (type, points, date) VALUES (?, ?, ?)", (type, points, date))
        conn.commit()
    except Exception as e:
        log_error(f"Database error in save_result: {e}")

# Function to show progress
def show_progress():
    try:
        c = conn.cursor()
        c.execute("SELECT date, points FROM results")
        data = c.fetchall()
        dates = [row[0] for row in data]
        points = [row[1] for row in data]
        plt.plot(dates, points, marker='o')
        plt.title("Learning Progress")
        plt.xlabel("Date")
        plt.ylabel("Points")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        log_error(f"Database or plot error in show_progress: {e}")
        messagebox.showerror("Error", "Could not display progress. See log.txt for details.")
    show_return_to_menu()

# Save results to JSON file
def save_results_to_file():
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM results")
        results = c.fetchall()
        with open("results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        messagebox.showinfo("Export", "Results exported to results.json")
    except Exception as e:
        log_error(f"Error exporting results: {e}")
        messagebox.showerror("Export Error", "Could not export results. See log.txt for details.")

# Load results from JSON file
def load_results_from_file():
    try:
        if not os.path.exists("results.json"):
            messagebox.showwarning("Import", "results.json not found.")
            return
        with open("results.json", "r", encoding="utf-8") as f:
            results = json.load(f)
        c = conn.cursor()
        for row in results:
            c.execute("INSERT INTO results (id, type, points, date) VALUES (?, ?, ?, ?)", row)
        conn.commit()
        messagebox.showinfo("Import", "Results imported from results.json")
    except Exception as e:
        log_error(f"Error importing results: {e}")
        messagebox.showerror("Import Error", "Could not import results. See log.txt for details.")

# Before inserting questions, clear existing ones
if conn is not None:
    c = conn.cursor()
    c.execute("DELETE FROM questions")  # Clear existing questions
    
    # Add single choice questions (20+)
    insert_question(conn, "Which routing protocol uses the Dijkstra algorithm?", "single", "OSPF", 
                   "RIP,BGP,EIGRP")
    
    insert_question(conn, "Which type of memory is faster?", "single", "SRAM", 
                   "DRAM,ROM,EPROM")
    
    insert_question(conn, "Which layer of the OSI model is responsible for routing?", "single", "Network Layer", 
                   "Transport Layer,Data Link Layer,Physical Layer")
    
    insert_question(conn, "Which database model uses JSON to store data?", "single", "Document", 
                   "Relational,Graph,Hierarchical")
                   
    insert_question(conn, "Which programming language is compiled?", "single", "C++", 
                   "Python,JavaScript,PHP")
                   
    insert_question(conn, "Which sorting algorithm has a time complexity of O(n log n)?", "single", "QuickSort", 
                   "BubbleSort,SelectionSort,InsertionSort")
                   
    insert_question(conn, "Which type of network has the largest range?", "single", "WAN", 
                   "LAN,MAN,PAN")
                   
    insert_question(conn, "Which protocol operates at the application layer?", "single", "HTTP", 
                   "TCP,IP,UDP")
                   
    insert_question(conn, "Which encryption method is symmetric?", "single", "AES", 
                   "RSA,DSA,ECC")
                   
    insert_question(conn, "Which file system is native to Linux?", "single", "ext4", 
                   "NTFS,FAT32,HFS+")
                   
    insert_question(conn, "Which port is default for HTTPS?", "single", "443", 
                   "80,21,22")
                   
    insert_question(conn, "Which virtualization technology is bare-metal?", "single", "VMware ESXi", 
                   "VirtualBox,QEMU,Wine")
                   
    insert_question(conn, "Which design pattern is creational?", "single", "Singleton", 
                   "Observer,Iterator,Decorator")
                   
    insert_question(conn, "Which data structure operates on a LIFO principle?", "single", "Stack", 
                   "Queue,List,Tree")
                   
    insert_question(conn, "Which protocol is stateless?", "single", "HTTP", 
                   "FTP,SSH,Telnet")
                   
    insert_question(conn, "Which HTTP method is used to delete resources?", "single", "DELETE", 
                   "GET,POST,PUT")
                   
    insert_question(conn, "Which format is used for data serialization?", "single", "JSON", 
                   "HTML,CSS,SQL")
                   
    insert_question(conn, "Which technique is used for load balancing?", "single", "Round Robin", 
                   "FIFO,LIFO,Priority Queue")
                   
    insert_question(conn, "Which protocol ensures data confidentiality?", "single", "SSH", 
                   "HTTP,FTP,SMTP")
                   
    insert_question(conn, "Which network topology is the most reliable?", "single", "Mesh", 
                   "Star,Bus,Ring")

    # Add multiple choice questions (20+)
    insert_question(conn, "Which routing protocols are link-state protocols?", 
                   "multiple", "OSPF,IS-IS", 
                   "OSPF,RIP,BGP,IS-IS")
    
    insert_question(conn, "Which of the following are RAM types?", 
                   "multiple", "DRAM,SRAM", 
                   "DRAM,SRAM,ROM,EPROM")
    
    insert_question(conn, "Which layers of the OSI model are related to communication?", 
                   "multiple", "Application Layer,Presentation Layer,Session Layer", 
                   "Application Layer,Presentation Layer,Session Layer,Transport Layer")
                   
    insert_question(conn, "Which programming languages are object-oriented?", 
                   "multiple", "Java,C++,Python", 
                   "Java,C++,Python,Assembly")
                   
    insert_question(conn, "Which operating systems are based on UNIX?", 
                   "multiple", "Linux,macOS,FreeBSD", 
                   "Linux,macOS,FreeBSD,Windows")
                   
    insert_question(conn, "Which protocols operate at the transport layer?", 
                   "multiple", "TCP,UDP", 
                   "TCP,UDP,IP,HTTP")
                   
    insert_question(conn, "Which HTTP methods are idempotent?", 
                   "multiple", "GET,PUT,DELETE", 
                   "GET,PUT,DELETE,POST")
                   
    insert_question(conn, "Which algorithms are used in asymmetric cryptography?", 
                   "multiple", "RSA,ECC,DSA", 
                   "RSA,ECC,DSA,AES")
                   
    insert_question(conn, "Which design patterns are structural?", 
                   "multiple", "Adapter,Bridge,Composite", 
                   "Adapter,Bridge,Composite,Singleton")
                   
    insert_question(conn, "Which technologies are related to containerization?", 
                   "multiple", "Docker,Kubernetes,Podman", 
                   "Docker,Kubernetes,Podman,VMware")
                   
    insert_question(conn, "Which protocols are used in email?", 
                   "multiple", "SMTP,POP3,IMAP", 
                   "SMTP,POP3,IMAP,FTP")
                   
    insert_question(conn, "Which file systems support UNIX permissions?", 
                   "multiple", "ext4,XFS,ZFS", 
                   "ext4,XFS,ZFS,FAT32")
                   
    insert_question(conn, "Which languages are used in machine learning?", 
                   "multiple", "Python,R,Julia", 
                   "Python,R,Julia,HTML")
                   
    insert_question(conn, "Which databases are NoSQL?", 
                   "multiple", "MongoDB,Cassandra,Redis", 
                   "MongoDB,Cassandra,Redis,PostgreSQL")
                   
    insert_question(conn, "Which protocols are related to security?", 
                   "multiple", "SSL,TLS,IPSec", 
                   "SSL,TLS,IPSec,FTP")
                   
    insert_question(conn, "Which technologies are used in Big Data?", 
                   "multiple", "Hadoop,Spark,HBase", 
                   "Hadoop,Spark,HBase,MySQL")
                   
    insert_question(conn, "Which elements are part of microservices architecture?", 
                   "multiple", "API Gateway,Service Registry,Load Balancer", 
                   "API Gateway,Service Registry,Load Balancer,Monolith")
                   
    insert_question(conn, "Which protocols are used in IoT?", 
                   "multiple", "MQTT,CoAP,AMQP", 
                   "MQTT,CoAP,AMQP,SQL")
                   
    insert_question(conn, "Which tools are used for CI/CD?", 
                   "multiple", "Jenkins,GitLab CI,Travis CI", 
                   "Jenkins,GitLab CI,Travis CI,Notepad")
                   
    insert_question(conn, "Which languages are compiled to native code?", 
                   "multiple", "C,C++,Rust", 
                   "C,C++,Rust,Python")

    # Clear and add new multiple choice questions
    if conn is not None:
        c = conn.cursor()
        c.execute("DELETE FROM questions WHERE type='multiple'")  
        
        # Add new multiple choice questions based on the content
        insert_question(conn, "Which of the following are object-oriented programming features?", 
                    "multiple", "Encapsulation,Inheritance,Polymorphism", 
                    "Encapsulation,Inheritance,Polymorphism,Sequentiality")
        
        insert_question(conn, "Which parameter passing methods are used in programming?", 
                    "multiple", "By value,By reference,By pointer", 
                    "By value,By reference,By pointer,By name")
        
        insert_question(conn, "Which characteristics characterize the OSI model?", 
                    "multiple", "Physical Layer,Data Link Layer,Network Layer", 
                    "Physical Layer,Data Link Layer,Network Layer,Abstraction Layer")
        
        insert_question(conn, "Which elements are part of ACID principles in databases?", 
                    "multiple", "Atomicity,Consistency,Isolation,Durability", 
                    "Atomicity,Consistency,Isolation,Durability,Flexibility")
        
        insert_question(conn, "Which color models are commonly used?", 
                    "multiple", "RGB,CMYK,HSV,LAB", 
                    "RGB,CMYK,HSV,LAB,YUV")
        
        insert_question(conn, "Which characteristics characterize embedded systems?", 
                    "multiple", "Low power consumption,Optimization,Real-time,Miniaturization", 
                    "Low power consumption,Optimization,Real-time,Miniaturization,Univerality")
        
        insert_question(conn, "Which methods are used to ensure network security?", 
                    "multiple", "Firewall,Encryption,VPN,IDS/IPS", 
                    "Firewall,Encryption,VPN,IDS/IPS,Compression")
        
        insert_question(conn, "What are the fundamental concepts of cryptography?", 
                    "multiple", "Symmetric encryption,Asymmetric encryption,Hash functions,Digital signature", 
                    "Symmetric encryption,Asymmetric encryption,Hash functions,Digital signature,Compression")
        
        insert_question(conn, "Which factors affect database performance?", 
                    "multiple", "Indexing,Query optimization,Fast SSD disks,Buffering", 
                    "Indexing,Query optimization,Fast SSD disks,Buffering,Fragmentation")
        
        insert_question(conn, "What are the main characteristics of interpersonal communication?", 
                    "multiple", "Two-way communication,Verbal signals,Non-verbal signals,Context", 
                    "Two-way communication,Verbal signals,Non-verbal signals,Context,One-way communication")

    # Now add open questions
    # Electrical engineering and electronics
    insert_question(conn, "Provide and discuss Thevenin's theorem.", "open", "Allows the simplification of a complex electrical circuit into a simple equivalent circuit, consisting of a voltage source and a resistor. Thevenin's theorem states that any linear electrical circuit, viewed from two terminals, can be replaced by an equivalent circuit, consisting of an ideal voltage source Thevenin (Vth) and a Thevenin resistor (Rth) connected in series. Vth - is the open-circuit voltage between the terminals, Rth - is the resistance viewed between these terminals, when all independent voltage sources are shorted, and independent current sources are open.")
    insert_question(conn, "Characterize the principle of a half-wave rectifier.", "open", "A simple rectifier circuit that conducts current only in one half of the input voltage cycle. A half-wave rectifier uses a diode that conducts current only when the anode has a higher potential than the cathode. As a result, only one half of the sinusoidal input voltage passes through the diode, creating a rectified, but pulsating voltage. This is the simplest, but least effective type of rectifier.")
    insert_question(conn, "Explain the principles of operation of semiconductor memory types RAM", "open", "RAM is volatile memory, in which data is temporarily stored and lost after power off. RAM (Random Access Memory) operates on the principle of fast data access and uses memory cells based on transistors and capacitors (DRAM) or flip-flops (SRAM). It is used to store active processes and program data. DRAM uses a capacitor and requires refreshing, SRAM does not require refreshing and is faster, but more expensive - but for an oral exam, the current form is sufficient.")

    # Basic programming
    insert_question(conn, "Characterize procedural and object-oriented programming paradigms.", "open", "Procedural programming relies on dividing code into functions and control blocks, while object-oriented programming organizes code into classes and objects. Procedural programming - uses constructs such as loops, conditional statements, and functions to organize code in a readable and logical way. Object-oriented programming - introduces the concept of objects, which combine data and methods operating on that data, enabling encapsulation, inheritance, and polymorphism.")
    insert_question(conn, "Discuss parameter passing methods.", "open", "Parameters can be passed by value (copying data) or by reference (referring to the original). By value - creates a copy of the parameter value, so changes do not affect the original data. By reference - the original value is passed, so changes made inside the function affect the calling variable. By pointer (e.g., in C++) - the memory address is passed, which gives greater control over the data, but requires caution.")

    # Algorithms and data structures
    insert_question(conn, "Explain concepts: time complexity of an algorithm (worst-case and average).", "open", "Time complexity determines how many operations an algorithm performs depending on the size of the data. Worst-case analysis evaluates the worst possible scenario, while average analysis evaluates the average time. Worst-case complexity (worst case) - determines the maximum number of operations an algorithm can perform. Denoted as O(n) or other asymptotic notations. Average complexity - determines the expected number of operations, based on average input cases.")
    insert_question(conn, "Provide a definition of an algorithm and its methods of recording.", "open", "An algorithm is a finite set of instructions leading to the solution of a specific problem. Algorithms can be recorded in several ways: Step-by-step description - a verbal description of actions. Flowchart - a graphical representation of the algorithm using blocks and arrows. Pseudocode - a recording that resembles programming code, but is independent of a specific language. Programming language - implementation of the algorithm in a selected language.")

    # Databases
    insert_question(conn, "Provide a definition and significance of keys in relational databases.", "open", "Keys in databases serve to uniquely identify records and ensure data integrity. Primary Key - a unique identifier in a table. Foreign Key - a reference to the primary key in another table, ensuring relationship consistency. Candidate Key - a potential primary key, satisfying uniqueness conditions. Composite Key - consisting of more than one column.")
    insert_question(conn, "Provide a description of the SQL query language.", "open", "SQL is a language for managing data in relational databases. SQL (Structured Query Language) allows: Retrieving data (SELECT) Modifying data (INSERT, UPDATE, DELETE) Defining table structure (CREATE TABLE, ALTER TABLE) Managing permissions (GRANT, REVOKE) Handling transactions (COMMIT, ROLLBACK)")
    insert_question(conn, "Explain the process of normalizing a relational database.", "open", "Normalization is the process of organizing data in a database to eliminate redundancy and ensure consistency. Normalization consists of several levels (normal forms), e.g.: 1NF - elimination of repeating data groups. 2NF - elimination of functional dependencies from the primary key. 3NF - elimination of intermediate dependencies between columns. BCNF - extension of 3NF to further reduce dependencies.")
    insert_question(conn, "Explain the concept of a transaction.", "open", "A transaction is a set of operations on a database, which must be executed in their entirety or not at all. Transactions in databases satisfy the ACID principles: Atomicity (Atomization) - a transaction is indivisible. Consistency (Consistency) - a transaction does not violate database rules. Isolation (Isolation) - transactions do not affect each other. Durability (Durability) - after transaction confirmation, data are permanently saved.")

    # Object-oriented programming
    insert_question(conn, "Explain concepts of object and class.", "open", "A class is a template defining properties and behaviors of objects, while an object is a specific instance of a class. A class contains fields (data) and methods (functions) defining its behavior. Objects are instances of a class - e.g., class Car can have objects Ford and Toyota, which inherit class properties, but can have different field values (e.g., color).")
    insert_question(conn, "Discuss the mechanism of virtual methods (functions).", "open", "Virtual methods allow dynamic (polymorphic) invocation of methods in derived classes. In languages like C++ and Java, a method marked as virtual (C++) or override (C#) can be overridden in a derived class, and the method call depends on the object type during program execution, not compilation.")

    # Computer networks
    insert_question(conn, "Discuss addressing mechanisms in networks.", "open", "Addressing in networks involves IP, MAC, and ports that enable device identification and communication. MAC address - a unique identifier of the network interface card at the data link layer. IP address - a logical address assigned to a device in a network (IPv4, IPv6). Ports - identify specific services (e.g., HTTP = port 80).")
    insert_question(conn, "Provide examples of routing protocols.", "open", "Routing protocols determine the route of packets in a network, e.g., RIP, OSPF, BGP. RIP (Routing Information Protocol) - a simple protocol based on the number of hops. OSPF (Open Shortest Path First) - an advanced protocol using the Dijkstra algorithm. BGP (Border Gateway Protocol) - used for routing between autonomous systems in the Internet.")
    insert_question(conn, "Discuss the OSI model.", "open", "The OSI model is a seven-layer structure describing communication in networks. OSI layers: Physical - transmission of electrical/optical signals. Data Link - MAC addressing, access to medium. Network - IP addressing, packet routing. Transport - session management, TCP/UDP protocols. Session - establishing, maintaining, and closing sessions. Presentation - encoding, encryption of data. Application - user interaction (HTTP, FTP).")

    # Computer architecture
    insert_question(conn, "Discuss the construction of the CISC and RISC program processor model.", "open", "CISC (Complex Instruction Set Computing) has a rich set of instructions, while RISC (Reduced Instruction Set Computing) limits the number of instructions for greater performance. CISC - complex instructions, multiple addressing modes, e.g., x86 processors. RISC - simple instructions, uniform execution time, e.g., ARM, MIPS.")

    # Software engineering
    insert_question(conn, "List and briefly characterize the most important software life cycle models.", "open", "Software life cycle models define the way they are created and developed, e.g., waterfall, incremental, spiral, and Agile. Waterfall model - linear, each phase ends before the next begins. Incremental model - system developed incrementally in successive versions. Spiral model - iterative approach with risk analysis. Agile - flexible approach with iterations and frequent interaction with the customer.")
    insert_question(conn, "Provide and briefly characterize the types of software testing.", "open", "Software testing is divided into unit, integration, system, and acceptance tests. Unit tests - check individual code modules. Integration tests - testing the interaction of different modules. System tests - check the entire system for functionality. Acceptance tests - performed by end users to approve the product.")

    # Artificial intelligence
    insert_question(conn, "Provide an example of a state space search algorithm in artificial intelligence systems.", "open", "State space search can be implemented, e.g., by A* algorithm or minimax algorithm. A* algorithm - optimal search with heuristics, used in route determination. Minimax - used in strategic games, selects the best move for the player, assuming the opponent plays optimally.")

    # Computer graphics
    insert_question(conn, "Present known color models.", "open", "Color models are RGB, CMYK, HSV, and LAB, used in graphics and printing. RGB (Red, Green, Blue) - additive model, used in screens. CMYK (Cyan, Magenta, Yellow, Black) - subtractive model, used in printing. HSV (Hue, Saturation, Value) - model based on human perception. LAB - model in which color describes lightness and two color axes, used for precise color manipulation")

    # Embedded systems
    insert_question(conn, "Characterize embedded systems.", "open", "Embedded systems are specialized computer systems designed to perform specific tasks. Embedded systems are computers operating in the background of devices, e.g., in cars, household appliances, medical equipment. They have optimized hardware and software, often operating in real-time.")
    insert_question(conn, "Specify the characteristics of modern embedded systems", "open", "Modern embedded systems are characterized by energy efficiency, small size, and high reliability. The most important characteristics are: Low power consumption - used in portable devices. Optimization for a specific task - lack of universality. Real-time - some systems must react immediately. Miniaturization - SoC (System on Chip) layouts allow for smaller size and energy consumption.")

    # Network security
    insert_question(conn, "Present fundamental concepts of cryptography.", "open", "Fundamental concepts are encryption, keys, hash functions, and digital signature. Symmetric encryption - the same key for encryption and decryption (AES). Asymmetric encryption - a public-private key pair (RSA). Hash functions - create a unique identifier for data (SHA-256). Digital signature - allows for sender authentication and data integrity.")
    insert_question(conn, "Discuss methods used to ensure network security.", "open", "Firewalls, encryption, VPN, and IDS/IPS systems are used for network protection. Firewalls - block unauthorized traffic. Encryption - protects data from interception. VPN - creates a secure, encrypted connection. IDS/IPS - detection and prevention of attacks.")

    # Database systems
    insert_question(conn, "Specify factors affecting database performance.", "open", "Performance depends on indexing, query optimization, and hardware. Indexing - speeds up data retrieval. Query optimization - eliminates unnecessary operations. Hardware resources - fast SSD disks improve performance. Buffering and caching - reduces the number of disk operations.")
    insert_question(conn, "Discuss selected database models.", "open", "Database models are relational, document, graph, and key-value. Relational (SQL) - based on tables and keys (MySQL, PostgreSQL). Document (NoSQL) - store data in JSON/XML format (MongoDB). Graph - represent data as nodes and edges (Neo4j). Key-value - fast mapping of keys to values (Redis).")
    insert_question(conn, "Discuss methods for executing complex SQL queries that allow for faster execution.", "open", "Query optimization involves using indexes, partitioning, and caching. Indexing - shortens search time. Partitioning - divides large tables into smaller fragments. Materialized views - save query results. EXPLAIN - query execution plan analysis allows for optimization.")

    # Interpersonal communication
    insert_question(conn, "Characterize the concept of interpersonal communication and its characteristics.", "open", "Interpersonal communication is the exchange of information between people, involving speech, gestures, and emotions. Main characteristics: Two-way communication - both sender and receiver exchange information. Verbal and non-verbal signals - meaning is not only content, but also method of transmission. Context - culture, situation, relationships influence interpretation.")

    # Basic creativity
    insert_question(conn, "Characterize concepts: intelligence, reason, knowledge, wisdom", "open", "Intelligence - ability to solve problems. Reasoning - ability to logical thinking. Knowledge - a collection of information obtained through experience and learning. Wisdom - ability to use knowledge in practice. Intelligence encompasses analytical and social aspects (IQ, EQ). Reasoning allows for drawing logical conclusions. Knowledge can be declarative (facts) or procedural (skills). Wisdom is conscious decision-making based on experience")
    insert_question(conn, "Discuss selected creative methods (assimilation, adaptation, inversion)", "open", "Creative methods are techniques that support creativity by leveraging existing solutions. Assimilation - combining known concepts in new ways. Adaptation - modifying existing solutions for new applications. Inversion - inverting known thought patterns to find a new approach.")

    conn.commit()

# After inserting questions, verify they are in the database
def check_database():
    c = conn.cursor()
    c.execute("SELECT type, COUNT(*) FROM questions GROUP BY type")
    counts = c.fetchall()
    print("Questions in database:")
    for type, count in counts:
        print(f"{type}: {count} questions")
    return counts

# Call this after inserting questions
check_database()

# GUI
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Programming Quiz - Professional Edition")
        self.geometry("1200x950")
        self.resizable(False, False)
        self.current_user = None
        self.quiz = None
        self.theme = 'light'
        self.show_login()

    def show_login(self):
        self.clear_screen()
        LoginScreen(self, self.login_success, self.show_register).pack(expand=True, fill='both')

    def show_register(self):
        self.clear_screen()
        RegisterScreen(self, self.login_success, self.show_login).pack(expand=True, fill='both')

    def login_success(self, user):
        self.current_user = user
        self.show_menu()

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_menu(self):
        self.clear_screen()
        MainMenuScreen(
            self,
            self.current_user,
            self.start_quiz,
            self.show_records,
            self.show_achievements,
            self.logout,
            self.show_stats,
            self.show_ranking,
            self.import_questions,
            self.export_questions,
            self.show_learning_mode,
            self.switch_theme
        ).pack(expand=True, fill='both')

    def start_quiz(self, test_type):
        self.clear_screen()
        # Pobierz pytania z bazy
        c = conn.cursor()
        c.execute("SELECT question, type, correct_answer, incorrect_options FROM questions WHERE type=?", (test_type,))
        rows = c.fetchall()
        questions = []
        for row in rows:
            q = {'question': row[0], 'type': row[1]}
            if row[1] == 'single':
                q['options'] = row[3].split(',') + [row[2]]
                random.shuffle(q['options'])
                q['answer'] = row[2]
            elif row[1] == 'multiple':
                q['options'] = row[3].split(',')
                q['answer'] = [a.strip() for a in row[2].split(',')]
            elif row[1] == 'open':
                q['options'] = []
                q['answer'] = row[2]
            questions.append(q)
        quiz = Quiz(questions, user=self.current_user)
        QuizScreen(self, quiz, self.show_menu).pack(expand=True, fill='both')

    def show_records(self):
        self.clear_screen()
        ResultsScreen(self, self.current_user, self.show_menu).pack(expand=True, fill='both')

    def show_achievements(self):
        self.clear_screen()
        AchievementsScreen(self, self.current_user, self.show_menu).pack(expand=True, fill='both')

    def logout(self):
        self.current_user = None
        self.quiz = None
        self.show_login()

    def show_stats(self):
        self.clear_screen()
        # Placeholder for stats screen
        tk.Label(self, text="Statistics Screen Placeholder", font=("Arial", 16)).pack(expand=True, fill='both')
        self.show_menu()

    def show_ranking(self):
        self.clear_screen()
        # Placeholder for ranking screen
        tk.Label(self, text="Ranking Screen Placeholder", font=("Arial", 16)).pack(expand=True, fill='both')
        self.show_menu()

    def import_questions(self):
        self.clear_screen()
        # Placeholder for import questions
        tk.Label(self, text="Import Questions Placeholder", font=("Arial", 16)).pack(expand=True, fill='both')
        self.show_menu()

    def export_questions(self):
        self.clear_screen()
        # Placeholder for export questions
        tk.Label(self, text="Export Questions Placeholder", font=("Arial", 16)).pack(expand=True, fill='both')
        self.show_menu()

    def show_learning_mode(self):
        # Example: use all questions from DB or a sample
        questions = [
            {'question': 'Which language is compiled?', 'type': 'single', 'options': ['Python', 'C++', 'JavaScript', 'PHP'], 'answer': 'C++', 'hint': 'It is used for high-performance applications.'},
            {'question': 'Select all OOP languages.', 'type': 'multiple', 'options': ['Java', 'C++', 'Python', 'HTML'], 'answer': ['Java', 'C++', 'Python'], 'hint': 'HTML is not a programming language.'},
            {'question': 'Describe the concept of inheritance in OOP.', 'type': 'open', 'options': [], 'answer': 'Inheritance allows a class to acquire properties and methods of another class.', 'hint': 'It is a key OOP principle.'}
        ]
        self.clear_screen()
        LearningModeScreen(self, questions, self.show_menu).pack(expand=True, fill='both')

    def switch_theme(self):
        self.theme = 'dark' if self.theme == 'light' else 'light'
        self.show_menu()

    def show_help(self):
        msg = (
            "Programming Quiz - User Guide\n\n"
            "1. Register or log in to your account.\n"
            "2. Use the menu to start a quiz, enter learning mode, view your records, achievements, statistics, or ranking.\n"
            "3. In quiz mode, answer questions, use lifelines (50/50, hint, skip), and watch the timer.\n"
            "4. In learning mode, practice questions with hints and see your mistakes.\n"
            "5. Use Import/Export to manage your own question sets.\n"
            "6. Switch between light and dark themes for your comfort.\n"
            "7. All your results and achievements are saved to your account.\n"
            "8. For help, click this button anytime!\n"
        )
        tk.messagebox.showinfo("Help / User Guide", msg)

app = App()
app.mainloop()

# Close the database connection
conn.close()
