import tkinter as tk
from tkinter import messagebox, filedialog, Scrollbar, Canvas
import random
import re

def load_questions(filename, question_prefix, option_prefixes, answer_prefix):
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    questions = []
    question = {}
    answer_map = {}

    for line in lines:
        line = line.strip()
        if re.match(r'^\d+\.\s*[A-Z]', line):
            number, answer = line.split('.', 1)
            answer_map[int(number.strip())] = answer.strip()

    for line in lines:
        line = line.strip()
        if line.startswith(question_prefix):
            if question:
                questions.append(question)
                question = {}
            question['question'] = line
            question_number = len(questions) + 1
            if question_number in answer_map:
                question['answer'] = answer_map[question_number]
            else:
                question['answer'] = ''
        elif any(line.startswith(prefix) for prefix in option_prefixes):
            question.setdefault('options', []).append(line)
        elif line.startswith(answer_prefix) and question:
            question['answer'] = line.split(": ")[1].strip()

    if question:
        questions.append(question)

    for i, question in enumerate(questions):
        if 'answer' not in question or not question['answer']:
            question['answer'] = answer_map.get(i + 1, '')

    if not questions:
        raise ValueError("No questions found in the file. Please check the file format.")

    random.shuffle(questions)
    return questions

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic Quiz App")
        self.root.geometry("600x600")
        self.root.config(bg="#f0f0f0")

        # Create a canvas for scrolling
        self.canvas = Canvas(root, bg="#f0f0f0")
        self.scrollbar = Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f0f0f0")

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Title Label
        self.title_label = tk.Label(self.scrollable_frame, text="Quiz App", font=("Arial", 24, "bold"), bg="#f0f0f0", fg="#333")
        self.title_label.pack(pady=20)

        # Input for prefixes
        self.question_prefix_entry = tk.Entry(self.scrollable_frame, font=("Arial", 12), width=40)
        self.question_prefix_entry.pack(pady=5)
        self.question_prefix_entry.insert(0, "Question Prefix (e.g., NO.)")

        self.option_prefixes_entry = tk.Entry(self.scrollable_frame, font=("Arial", 12), width=40)
        self.option_prefixes_entry.pack(pady=5)
        self.option_prefixes_entry.insert(0, "Option Prefixes (e.g., A., B., C., D.)")

        self.answer_prefix_entry = tk.Entry(self.scrollable_frame, font=("Arial", 12), width=40)
        self.answer_prefix_entry.pack(pady=5)
        self.answer_prefix_entry.insert(0, "Answer Prefix (e.g., Answer:)")

        # Load Questions Button
        self.load_button = tk.Button(self.scrollable_frame, text="Load Questions", command=self.load_questions_from_file, bg="#4CAF50", fg="white", font=("Arial", 14))
        self.load_button.pack(pady=20)

        # Score and Percentage Labels
        self.score_label = tk.Label(self.scrollable_frame, text=f"Score: 0", font=("Arial", 14), bg="#f0f0f0")
        self.score_label.pack(pady=10)

        self.percentage_label = tk.Label(self.scrollable_frame, text="Percentage: 0%", font=("Arial", 14), bg="#f0f0f0")
        self.percentage_label.pack(pady=10)

        # Next button
        self.next_button = tk.Button(self.scrollable_frame, text="Next", command=self.check_answer, bg="#4CAF50", fg="white", font=("Arial", 14))
        self.next_button.pack(pady=20)

        # Question display area
        self.question_frame = tk.Frame(self.scrollable_frame, bg="#f0f0f0")
        self.question_frame.pack(fill=tk.BOTH, expand=True)

        # Centering the content
        self.center_content()

        # Other variables
        self.questions = []
        self.current_question = 0
        self.score = 0
        self.incorrect_answers = []

        # Bind resize event
        self.root.bind("<Configure>", self.center_content)

    def center_content(self, event=None):
        # Center the scrollable frame in the canvas
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        frame_width = self.scrollable_frame.winfo_width()
        frame_height = self.scrollable_frame.winfo_height()

        x = (width - frame_width) // 2
        y = (height - frame_height) // 2

        self.canvas.place(x=x, y=y, width=frame_width, height=frame_height)

    def load_questions_from_file(self):
        filename = filedialog.askopenfilename(title="Select a Questions File", filetypes=[("Text files", "*.txt")])
        if filename:
            question_prefix = self.question_prefix_entry.get().strip()
            option_prefixes = [prefix.strip() for prefix in self.option_prefixes_entry.get().split(',')]
            answer_prefix = self.answer_prefix_entry.get().strip()

            try:
                self.questions = load_questions(filename, question_prefix, option_prefixes, answer_prefix)
                self.current_question = 0
                self.score = 0
                self.score_label.config(text=f"Score: {self.score}")
                self.percentage_label.config(text="Percentage: 0%")
                self.load_question()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def load_question(self):
        for widget in self.question_frame.winfo_children():
            widget.destroy()  # Clear previous question and options

        if self.current_question < len(self.questions):
            question_data = self.questions[self.current_question]
            question_label = tk.Label(self.question_frame, text=question_data['question'], wraplength=550, font=("Arial", 16), bg="#f0f0f0")
            question_label.pack(pady=10)

            if ',' in question_data['answer']:
                self.check_vars = []
                for option in question_data['options']:
                    var = tk.BooleanVar()
                    checkbox = tk.Checkbutton(self.question_frame, text=option, variable=var, bg="#f0f0f0", font=("Arial", 12))
                    checkbox.pack(anchor='w')
                    self.check_vars.append(var)
            else:
                self.option_var = tk.StringVar()
                for option in question_data['options']:
                    rb = tk.Radiobutton(self.question_frame, text=option, variable=self.option_var, value=option, bg="#f0f0f0", font=("Arial", 12))
                    rb.pack(anchor='w')
        else:
            self.show_result()

    def check_answer(self):
        correct_answer = self.questions[self.current_question]['answer'].strip()

        if ',' in correct_answer:
            selected_options = [option[0] for var, option in zip(self.check_vars, self.questions[self.current_question]['options']) if var.get()]
            correct_options = [option.strip() for option in correct_answer.split(",")]

            if sorted(selected_options) == sorted(correct_options):
                self.score += 1
                messagebox.showinfo("Result", "Correct!")
            else:
                self.incorrect_answers.append((self.questions[self.current_question]['question'], correct_answer))
                messagebox.showinfo("Result", f"Wrong! The correct answers are: {', '.join(correct_options)}")
        else:
            selected_option = self.option_var.get().strip()
            selected_option_letter = selected_option.split('.')[0].strip()

            if selected_option_letter == correct_answer:
                self.score += 1
                messagebox.showinfo("Result", "Correct!")
            else:
                self.incorrect_answers.append((self.questions[self.current_question]['question'], correct_answer))
                messagebox.showinfo("Result", f"Wrong! The correct answer is: {correct_answer}")

        self.current_question += 1
        total_questions_attempted = self.current_question
        self.score_label.config(text=f"Score: {self.score}")

        if total_questions_attempted > 0:
            percentage = (self.score / total_questions_attempted) * 100
            self.percentage_label.config(text=f"Percentage: {percentage:.2f}%")

        self.load_question()

    def show_result(self):
        messagebox.showinfo("Quiz Completed", f"Your total score: {self.score}/{len(self.questions)}")
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
