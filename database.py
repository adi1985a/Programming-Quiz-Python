import sqlite3

def create_connection(db_file):
    """ Create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    """ Create a table from the create_table_sql statement """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

def insert_question(conn, question, question_type, correct_answer, incorrect_options=None):
    """ Insert a question into the questions table """
    sql = ''' INSERT INTO questions(question,type,correct_answer,incorrect_options)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (question, question_type, correct_answer, incorrect_options))
    conn.commit()
    return cur.lastrowid

def check_questions(conn):
    """Check questions in the database"""
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM questions")
    total = cur.fetchone()[0]
    
    cur.execute("SELECT type, COUNT(*) FROM questions GROUP BY type")
    types = cur.fetchall()
    
    return total, types

def create_database():
    database = "knowledge_tests.db"

    sql_create_questions_table = """
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY,
        question TEXT NOT NULL,
        type TEXT NOT NULL,
        correct_answer TEXT NOT NULL,
        incorrect_options TEXT
    );
    """

    sql_create_results_table = """
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY,
        type TEXT NOT NULL,
        points INTEGER NOT NULL,
        date TEXT NOT NULL
    );
    """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        create_table(conn, sql_create_questions_table)
        create_table(conn, sql_create_results_table)
        return conn
    else:
        print("Error! cannot create the database connection.")
        return None
