import tkinter as tk
from tkinter import messagebox
from user import User
from quiz import Quiz
import threading
import time
import winsound

THEMES = {
    'light': {'bg': '#f7fbff', 'fg': '#003366', 'button': '#b3e6cc', 'accent': '#0059b3'},
    'dark': {'bg': '#222831', 'fg': '#eeeeee', 'button': '#393e46', 'accent': '#00adb5'}
}

class LoginScreen(tk.Frame):
    def __init__(self, master, on_login, on_register):
        super().__init__(master, bg='#e6f2ff')
        self.on_login = on_login
        self.on_register = on_register
        tk.Label(self, text="Login", font=("Arial", 18, "bold"), bg='#e6f2ff', fg='#0059b3').pack(pady=10)
        tk.Label(self, text="Username:", bg='#e6f2ff').pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=2)
        tk.Label(self, text="Password:", bg='#e6f2ff').pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=2)
        tk.Button(self, text="Login", command=self.try_login, bg='#b3e6cc', fg='#003300').pack(pady=8)
        tk.Button(self, text="Register", command=self.on_register, bg='#ffe680', fg='#665c00').pack()
        self.password_entry.bind('<Return>', lambda event: self.try_login())
        self.username_entry.bind('<Return>', lambda event: self.try_login())

    def try_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter both username and password.")
            return
        success, result = User.login(username, password)
        if success:
            self.on_login(result)
        else:
            messagebox.showerror("Login Failed", result)

class RegisterScreen(tk.Frame):
    def __init__(self, master, on_register_success, on_back):
        super().__init__(master, bg='#e6f2ff')
        self.on_register_success = on_register_success
        self.on_back = on_back
        tk.Label(self, text="Register", font=("Arial", 18, "bold"), bg='#e6f2ff', fg='#0059b3').pack(pady=10)
        tk.Label(self, text="Username:", bg='#e6f2ff').pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=2)
        tk.Label(self, text="Email:", bg='#e6f2ff').pack()
        self.email_entry = tk.Entry(self)
        self.email_entry.pack(pady=2)
        tk.Label(self, text="Password:", bg='#e6f2ff').pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=2)
        tk.Label(self, text="Confirm Password:", bg='#e6f2ff').pack()
        self.confirm_entry = tk.Entry(self, show="*")
        self.confirm_entry.pack(pady=2)
        tk.Button(self, text="Register", command=self.try_register, bg='#b3e6cc', fg='#003300').pack(pady=8)
        tk.Button(self, text="Back to Login", command=self.on_back, bg='#ffe680', fg='#665c00').pack()

    def try_register(self):
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm = self.confirm_entry.get().strip()
        if not username or not email or not password or not confirm:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return
        if password != confirm:
            messagebox.showwarning("Input Error", "Passwords do not match.")
            return
        success, result = User.register(username, email, password)
        if success:
            messagebox.showinfo("Registration Successful", result)
            user = User.get_user(username)
            self.on_register_success(user)
        else:
            messagebox.showerror("Registration Failed", result)

class MainMenuScreen(tk.Frame):
    def __init__(self, master, user, on_start_quiz, on_show_records, on_show_achievements, on_logout, on_show_stats, on_show_ranking, on_import, on_export, on_learning_mode, on_theme):
        super().__init__(master, bg=THEMES[master.theme]['bg'])
        self.user = user
        self.on_start_quiz = on_start_quiz
        self.on_show_records = on_show_records
        self.on_show_achievements = on_show_achievements
        self.on_logout = on_logout
        self.on_show_stats = on_show_stats
        self.on_show_ranking = on_show_ranking
        self.on_import = on_import
        self.on_export = on_export
        self.on_learning_mode = on_learning_mode
        self.on_theme = on_theme
        self.welcome_label = tk.Label(self, text=f"Welcome, {user.username}!", font=("Arial", 16, "bold"), bg=THEMES[master.theme]['bg'], fg=THEMES[master.theme]['accent'])
        self.welcome_label.pack(pady=15)
        self.fade_in(self.welcome_label)
        tk.Button(self, text="Start Quiz", command=self.choose_quiz_type, bg=THEMES[master.theme]['button'], fg=THEMES[master.theme]['fg'], font=("Arial", 12, "bold")).pack(pady=8)
        tk.Button(self, text="Learning Mode", command=self.on_learning_mode, bg=THEMES[master.theme]['button'], fg=THEMES[master.theme]['accent'], font=("Arial", 12, "bold")).pack(pady=8)
        tk.Button(self, text="Show Records", command=self.show_records, bg='#ffe680', fg='#665c00', font=("Arial", 12, "bold")).pack(pady=8)
        tk.Button(self, text="Show Achievements", command=self.show_achievements, bg=THEMES[master.theme]['bg'], fg=THEMES[master.theme]['accent'], font=("Arial", 12, "bold")).pack(pady=8)
        tk.Button(self, text="Statistics", command=self.show_stats, bg=THEMES[master.theme]['bg'], fg=THEMES[master.theme]['accent'], font=("Arial", 12, "bold")).pack(pady=8)
        tk.Button(self, text="Ranking", command=self.show_ranking, bg=THEMES[master.theme]['bg'], fg=THEMES[master.theme]['accent'], font=("Arial", 12, "bold")).pack(pady=8)
        tk.Button(self, text="Import Questions", command=self.show_import, bg=THEMES[master.theme]['bg'], fg=THEMES[master.theme]['accent'], font=("Arial", 12, "bold")).pack(pady=8)
        tk.Button(self, text="Export Questions", command=self.show_export, bg=THEMES[master.theme]['bg'], fg=THEMES[master.theme]['accent'], font=("Arial", 12, "bold")).pack(pady=8)
        tk.Button(self, text="Switch Theme", command=self.on_theme, bg=THEMES[master.theme]['button'], fg=THEMES[master.theme]['accent'], font=("Arial", 12, "bold")).pack(pady=8)
        tk.Button(self, text="Logout", command=self.on_logout, bg='#ffcccc', fg='#990000', font=("Arial", 12, "bold")).pack(pady=20)
        # Dodaj suwak do info_box
        frame = tk.Frame(self)
        frame.pack(pady=10, fill=tk.BOTH, expand=True)
        self.info_box = tk.Text(frame, height=14, width=120, bg=THEMES[master.theme]['bg'], fg=THEMES[master.theme]['fg'], state=tk.DISABLED, wrap=tk.WORD)
        self.info_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(frame, command=self.info_box.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.info_box.config(yscrollcommand=scrollbar.set)
        self.show_info("Welcome to the Programming Quiz! Use the menu to start.")

    def fade_in(self, label, step=0):
        colors = ['#e6f2ff', '#d0e6fa', '#b3d8f7', '#99c9f3', '#80bbf0', '#66acec', '#4d9ee9', '#3390e5', '#1a81e2', '#0059b3']
        if step < len(colors):
            label.config(fg=colors[step])
            self.after(50, lambda: self.fade_in(label, step+1))

    def choose_quiz_type(self):
        self.show_info("Select quiz type: Single Choice, Multiple Choice, Open Questions.")
        self.clear_info_buttons()
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=5)
        self.info_btn_frame = btn_frame
        for t, label in [("single", "Single Choice"), ("multiple", "Multiple Choice"), ("open", "Open Questions")]:
            b = tk.Button(btn_frame, text=label, font=("Arial", 12), command=lambda typ=t: self._start_quiz_and_clear_buttons(typ))
            b.pack(side=tk.LEFT, padx=10)
    def _start_quiz_and_clear_buttons(self, test_type):
        self.clear_info_buttons()
        self.on_start_quiz(test_type)
    def clear_info_buttons(self):
        if hasattr(self, 'info_btn_frame') and self.info_btn_frame:
            self.info_btn_frame.destroy()
            self.info_btn_frame = None

    def show_records(self):
        records = self.user.get_records()
        msg = '\n'.join([f"{t} - {p} pts ({d})" for t, p, d in records]) or "No records yet."
        self.show_info(msg)

    def show_achievements(self):
        achievements = self.user.get_achievements()
        if not achievements:
            msg = "No achievements yet."
        else:
            msg = '\n'.join([f"{n} ({d}): {desc}" for n, desc, d in achievements])
        self.show_info(msg)

    def show_stats(self):
        stats = self.user.get_stats()
        msg = f"Quizzes taken: {stats['quizzes']}\nBest score: {stats['best']}\nAverage: {stats['avg']}"
        self.show_info(msg)

    def show_ranking(self):
        ranking = self.user.get_ranking()
        msg = '\n'.join([f"{i+1}. {u} - {p} pts" for i, (u, p) in enumerate(ranking)]) or "No ranking yet."
        self.show_info(msg)

    def show_import(self):
        self.show_info("Import Questions: (functionality to be implemented)")

    def show_export(self):
        self.show_info("Export Questions: (functionality to be implemented)")

    def show_info(self, msg):
        self.info_box.config(state=tk.NORMAL)
        self.info_box.delete(1.0, tk.END)
        self.info_box.insert(tk.END, msg)
        self.info_box.config(state=tk.DISABLED)
        self.info_box.see(tk.END)

class QuizScreen(tk.Frame):
    def __init__(self, master, quiz, on_finish):
        super().__init__(master, bg='#f7fbff')
        self.quiz = quiz
        self.on_finish = on_finish
        self.timer_label = tk.Label(self, text="", font=("Arial", 14, "bold"), bg='#f7fbff', fg='#990000')
        self.timer_label.pack(pady=5)
        self.counter_label = tk.Label(self, text="", font=("Arial", 12, "bold"), bg='#f7fbff', fg='#0059b3')
        self.counter_label.pack(pady=2)
        self.question_label = tk.Label(self, text="", font=("Arial", 14), wraplength=900, bg='#f7fbff', fg='#003366')
        self.question_label.pack(pady=10)
        self.options_frame = tk.Frame(self, bg='#f7fbff')
        self.options_frame.pack(pady=5)
        self.answer_entry = tk.Entry(self, width=70)
        self.lifeline_frame = tk.Frame(self, bg='#f7fbff')
        self.lifeline_frame.pack(pady=10)
        self.fifty_btn = tk.Button(self.lifeline_frame, text="50/50", command=self.use_fifty, bg='#ffe680', fg='#665c00')
        self.fifty_btn.pack(side=tk.LEFT, padx=5)
        self.hint_btn = tk.Button(self.lifeline_frame, text="Hint", command=self.use_hint, bg='#e6f2ff', fg='#0059b3')
        self.hint_btn.pack(side=tk.LEFT, padx=5)
        self.skip_btn = tk.Button(self.lifeline_frame, text="Skip", command=self.use_skip, bg='#ffcccc', fg='#990000')
        self.skip_btn.pack(side=tk.LEFT, padx=5)
        self.submit_button = tk.Button(self, text="Submit", command=self.submit_answer, bg='#b3e6cc', fg='#003300', font=("Arial", 14, "bold"), height=2, width=16)
        self.submit_button.pack(pady=10)
        self.prev_btn = tk.Button(self, text="Previous", command=self.go_previous, bg='#e6f2ff', fg='#0059b3', font=("Arial", 11, "bold"))
        self.prev_btn.pack(pady=5)
        self.return_btn = tk.Button(self, text="Return to Menu", command=self.on_finish, bg='#b3e6cc', fg='#003300', font=("Arial", 11, "bold"))
        self.return_btn.pack(pady=5)
        self.time_limit = 45
        self.time_left = self.time_limit
        self.timer_running = False
        self.time_up_shown = False
        self.timer_start = None
        frame = tk.Frame(self)
        frame.pack(pady=10, fill=tk.BOTH, expand=True)
        self.message_box = tk.Text(frame, height=10, width=120, bg='#f7fbff', fg='#003366', state=tk.DISABLED, wrap=tk.WORD)
        self.message_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(frame, command=self.message_box.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.message_box.config(yscrollcommand=scrollbar.set)
        self.incorrect_answers = []
        self.show_question()

    def show_question(self):
        self.clear_options()
        self.clear_messages()
        self.time_up_shown = False
        if self.quiz.current_question >= len(self.quiz.questions):
            self.show_results()
            return
        q = self.quiz.questions[self.quiz.current_question]
        self.counter_label.config(text=f"Question {self.quiz.current_question+1} / {len(self.quiz.questions)}")
        self.question_label.config(text=f"Q{self.quiz.current_question+1}: {q['question']}")
        self.time_left = self.time_limit
        self.timer_start = time.time()
        self.update_timer()
        if q['type'] == 'single':
            self.vars = []
            for i, opt in enumerate(q['options']):
                var = tk.IntVar()
                rb = tk.Radiobutton(self.options_frame, text=opt, variable=var, value=1, bg='#f7fbff', anchor='w')
                rb.pack(fill='x', padx=10, pady=2)
                self.vars.append((var, opt))
            self.answer_entry.pack_forget()
        elif q['type'] == 'multiple':
            self.vars = []
            for i, opt in enumerate(q['options']):
                var = tk.IntVar()
                cb = tk.Checkbutton(self.options_frame, text=opt, variable=var, bg='#f7fbff', anchor='w')
                cb.pack(fill='x', padx=10, pady=2)
                self.vars.append((var, opt))
            self.answer_entry.pack_forget()
        elif q['type'] == 'open':
            self.answer_entry.pack(pady=10)
        else:
            self.answer_entry.pack_forget()
        self.add_message("--- New question ---")
        # Dodaj domyślny hint jeśli nie ma
        if 'hint' in q and q['hint']:
            self.add_message(f"Hint: {q['hint']}")
        else:
            self.add_message("Hint: Think carefully and use your knowledge!")

    def clear_options(self):
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        self.answer_entry.pack_forget()

    def clear_messages(self):
        self.message_box.config(state=tk.NORMAL)
        self.message_box.delete(1.0, tk.END)
        self.message_box.config(state=tk.DISABLED)

    def submit_answer(self):
        q = self.quiz.questions[self.quiz.current_question]
        if q['type'] == 'single':
            selected = [opt for var, opt in self.vars if var.get() == 1]
            if not selected:
                self.add_message("Please select an answer.")
                return
            user_answer = selected[0]
        elif q['type'] == 'multiple':
            selected = [opt for var, opt in self.vars if var.get() == 1]
            if not selected:
                self.add_message("Please select at least one answer.")
                return
            user_answer = selected
        elif q['type'] == 'open':
            user_answer = self.answer_entry.get().strip()
            if not user_answer:
                self.add_message("Please enter your answer.")
                return
        else:
            user_answer = None
        correct = self.quiz.check_answer(user_answer)
        if correct:
            self.add_message("[CORRECT] Your answer is correct!")
            self.quiz.points += 1
        else:
            self.add_message(f"[INCORRECT] Your answer is incorrect. Correct answer: {q['answer']}")
            self.incorrect_answers.append((self.quiz.current_question+1, q['question'], q['answer']))
        self.quiz.current_question += 1
        self.show_question()

    def update_timer(self):
        elapsed = int(time.time() - self.timer_start) if self.timer_start else 0
        self.time_left = max(self.time_limit - elapsed, 0)
        self.timer_label.config(text=f"Time left: {self.time_left}s")
        if self.time_left > 0:
            self.after(1000, self.update_timer)
        else:
            if not self.time_up_shown:
                self.add_message("Time's up! You ran out of time for this question.")
                self.time_up_shown = True
                self.incorrect_answers.append((self.quiz.current_question+1, self.quiz.questions[self.quiz.current_question]['question'], self.quiz.questions[self.quiz.current_question]['answer']))
                self.quiz.current_question += 1
                self.show_question()

    def add_message(self, msg):
        self.message_box.config(state=tk.NORMAL)
        self.message_box.insert(tk.END, msg + '\n')
        self.message_box.config(state=tk.DISABLED)
        self.message_box.see(tk.END)

    def use_fifty(self):
        if not self.quiz.lifelines['fifty_fifty']:
            self.add_message("You have already used 50/50.")
            return
        q = self.quiz.questions[self.quiz.current_question]
        if q['type'] not in ['single', 'multiple']:
            self.add_message("50/50 is only for single or multiple choice questions.")
            return
        correct = q['answer'] if isinstance(q['answer'], list) else [q['answer']]
        options = q['options'][:]
        to_remove = [opt for opt in options if opt not in correct]
        if len(to_remove) > 1:
            import random
            remove = random.sample(to_remove, len(to_remove)-1)
            for var, opt in self.vars:
                if opt in remove:
                    var.set(0)
        self.quiz.lifelines['fifty_fifty'] = False
        self.fifty_btn.config(state=tk.DISABLED)
        self.add_message("50/50 used.")

    def use_hint(self):
        if not self.quiz.lifelines['hint']:
            self.add_message("You have already used Hint.")
            return
        q = self.quiz.questions[self.quiz.current_question]
        hint = q.get('hint', 'Think carefully and use your knowledge!')
        self.add_message(f"Hint: {hint}")
        self.quiz.lifelines['hint'] = False
        self.hint_btn.config(state=tk.DISABLED)

    def use_skip(self):
        if not self.quiz.lifelines['skip']:
            self.add_message("You have already used Skip.")
            return
        self.quiz.current_question += 1
        self.quiz.lifelines['skip'] = False
        self.skip_btn.config(state=tk.DISABLED)
        self.add_message("Question skipped.")
        self.show_question()

    def go_previous(self):
        if self.quiz.current_question > 0:
            self.quiz.current_question -= 1
            self.show_question()

    def show_results(self):
        self.clear_options()
        self.clear_messages()
        self.counter_label.config(text="Quiz completed!")
        self.question_label.config(text=f"Your score: {self.quiz.points} / {len(self.quiz.questions)}")
        self.add_message(f"Quiz completed! Your score: {self.quiz.points} / {len(self.quiz.questions)}")
        if self.incorrect_answers:
            self.add_message("Incorrect answers:")
            for num, qtext, ans in self.incorrect_answers:
                self.add_message(f"Q{num}: {qtext}\nCorrect answer: {ans}")
        else:
            self.add_message("All answers were correct!")
        self.submit_button.pack_forget()
        self.lifeline_frame.pack_forget()
        self.timer_label.pack_forget()
        self.prev_btn.pack_forget()
        self.return_btn.pack(pady=20)

class ResultsScreen(tk.Frame):
    def __init__(self, master, quiz, on_return):
        super().__init__(master, bg='#f7fbff')
        self.quiz = quiz
        self.on_return = on_return
        tk.Label(self, text="Quiz Results", font=("Arial", 16, "bold"), bg='#f7fbff', fg='#0059b3').pack(pady=15)
        tk.Label(self, text=f"Score: {quiz.points} / {len(quiz.questions)}", font=("Arial", 14), bg='#f7fbff', fg='#003366').pack(pady=10)
        tk.Button(self, text="Return to Menu", command=self.on_return, bg='#b3e6cc', fg='#003300', font=("Arial", 12, "bold")).pack(pady=20)

class AchievementsScreen(tk.Frame):
    def __init__(self, master, achievements, on_return):
        super().__init__(master, bg='#f7fbff')
        self.achievements = achievements
        self.on_return = on_return
        tk.Label(self, text="Achievements", font=("Arial", 16, "bold"), bg='#f7fbff', fg='#0059b3').pack(pady=15)
        if not achievements:
            tk.Label(self, text="No achievements yet.", font=("Arial", 12), bg='#f7fbff', fg='#003366').pack(pady=10)
        else:
            for name, desc, date in achievements:
                tk.Label(self, text=f"{name} ({date})", font=("Arial", 12, "bold"), bg='#f7fbff', fg='#0059b3').pack(pady=2)
                tk.Label(self, text=desc, font=("Arial", 11), bg='#f7fbff', fg='#003366').pack(pady=1)
        tk.Button(self, text="Return to Menu", command=self.on_return, bg='#b3e6cc', fg='#003300', font=("Arial", 12, "bold")).pack(pady=20) 

class LearningModeScreen(tk.Frame):
    def __init__(self, master, questions, on_return):
        super().__init__(master, bg=THEMES[master.theme]['bg'])
        self.questions = questions
        self.on_return = on_return
        self.current = 0
        self.errors = {}
        self.messages = []
        self.label = tk.Label(self, text="Learning Mode", font=("Arial", 16, "bold"), bg=THEMES[master.theme]['bg'], fg=THEMES[master.theme]['accent'])
        self.label.pack(pady=10)
        self.question_label = tk.Label(self, text="", font=("Arial", 14), wraplength=900, bg=THEMES[master.theme]['bg'], fg=THEMES[master.theme]['fg'])
        self.question_label.pack(pady=10)
        self.hint_label = tk.Label(self, text="", font=("Arial", 11), bg=THEMES[master.theme]['bg'], fg=THEMES[master.theme]['accent'])
        self.hint_label.pack(pady=5)
        self.answer_entry = tk.Entry(self, width=70)
        self.answer_entry.pack(pady=5)
        self.submit_btn = tk.Button(self, text="Check", command=self.check, bg=THEMES[master.theme]['button'], fg=THEMES[master.theme]['fg'])
        self.submit_btn.pack(pady=10)
        self.next_btn = tk.Button(self, text="Next", command=self.next_q, bg=THEMES[master.theme]['button'], fg=THEMES[master.theme]['fg'])
        self.next_btn.pack(pady=5)
        self.stats_label = tk.Label(self, text="", font=("Arial", 11), bg=THEMES[master.theme]['bg'], fg=THEMES[master.theme]['accent'])
        self.stats_label.pack(pady=10)
        frame = tk.Frame(self)
        frame.pack(pady=10, fill=tk.BOTH, expand=True)
        self.message_box = tk.Text(frame, height=10, width=120, bg=THEMES[master.theme]['bg'], fg=THEMES[master.theme]['fg'], state=tk.DISABLED, wrap=tk.WORD)
        self.message_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(frame, command=self.message_box.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.message_box.config(yscrollcommand=scrollbar.set)
        self.return_btn = tk.Button(self, text="Return to Menu", command=self.on_return, bg='#b3e6cc', fg='#003300', font=("Arial", 11, "bold"))
        self.return_btn.pack(pady=10)
        self.show_q()

    def next_q(self):
        self.current += 1
        self.show_q()

    def show_q(self):
        if self.current >= len(self.questions):
            self.question_label.config(text="End of learning session.")
            self.hint_label.config(text="")
            self.answer_entry.pack_forget()
            self.submit_btn.pack_forget()
            self.next_btn.config(text="Return", command=self.on_return)
            self.stats_label.config(text=f"Mistakes: {sum(self.errors.values())}")
            return
        q = self.questions[self.current]
        self.question_label.config(text=f"Q{self.current+1}: {q['question']}")
        self.hint_label.config(text=f"Hint: {q.get('hint', 'No hint')}")
        self.answer_entry.delete(0, tk.END)
        self.stats_label.config(text=f"Mistakes: {self.errors.get(self.current, 0)}")
        self.add_message(f"--- New question ---")

    def add_message(self, msg):
        self.messages.append(msg)
        self.message_box.config(state=tk.NORMAL)
        self.message_box.delete(1.0, tk.END)
        for m in self.messages[-10:]:
            self.message_box.insert(tk.END, m + '\n')
        self.message_box.config(state=tk.DISABLED)
        self.message_box.see(tk.END)

    def check(self):
        q = self.questions[self.current]
        answer = self.answer_entry.get().strip().lower()
        if not answer:
            self.add_message("Please enter your answer.")
            return
        # Obsługa różnych typów pytań
        if q['type'] == 'single':
            correct = q['answer'].strip().lower()
            is_correct = answer == correct
        elif q['type'] == 'multiple':
            correct_set = set([a.strip().lower() for a in q['answer']]) if isinstance(q['answer'], list) else set([q['answer'].strip().lower()])
            user_set = set([a.strip() for a in answer.split(',') if a.strip()])
            is_correct = user_set == correct_set
        elif q['type'] == 'open':
            correct_answer = q['answer'].lower()
            key_words = [word for word in correct_answer.split() if len(word) > 3][:5]
            matches = sum(1 for word in key_words if word in answer)
            is_correct = matches >= 2
        else:
            is_correct = False
        if is_correct:
            self.add_message("Correct! Good job!")
            self.after(1200, self.clear_messages)
            self.next_q()
        else:
            self.add_message(f"Incorrect. Correct answer: {q['answer']}")
            self.errors[self.current] = self.errors.get(self.current, 0) + 1
            self.stats_label.config(text=f"Mistakes: {self.errors.get(self.current, 0)}")
            if self.errors[self.current] >= 3:
                self.add_message(f"Incorrect. Correct answer: {q['answer']}")
                self.next_q()
            else:
                self.add_message(f"Incorrect. Try again! ({self.errors[self.current]}/3)") 