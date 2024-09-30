import tkinter as tk
from tkinter import messagebox, filedialog, Scrollbar, Canvas
import random
import re

def load_questions(filename, question_prefix, option_prefixes, answer_prefix):
    """Load questions from a specified file, parsing them based on provided prefixes."""
    with open(filename, 'r') as file:
        lines = file.readlines()

    questions = []
    answer_map = {}

    # Parse answers if they're provided separately in the file
    for line in lines:
        line = line.strip()
        if re.match(r'^\d+\.\s*[A-Z]', line):
            number, answer = line.split('.', 1)
            answer_map[int(number.strip())] = answer.strip()

    question_text = []
    options = []
    question = False

    for line in lines:
        line = line.strip()
        # Check for a question line
        if line.startswith(question_prefix):
            if question:
                questions.append({
                    'question': ' '.join(question_text), 
                    'options': options, 
                    'answer': answer_map.get(len(questions) + 1, '')
                })
                question_text = []
                options = []
            question = True
            question_text.append(line[len(question_prefix):].strip())
        # Check for options
        elif question and any(line.startswith(prefix) for prefix in option_prefixes):
            options.append(line)
        # Check for answers with a new format
        elif question and line.startswith(answer_prefix):
            answer = line.split(": ")[1].strip()
            questions.append({
                'question': ' '.join(question_text), 
                'options': options, 
                'answer': answer
            })
            question_text = []
            options = []
            question = False
        # Check for blank lines to finalize a question
        elif question and line == "":
            questions.append({
                'question': ' '.join(question_text), 
                'options': options, 
                'answer': answer_map.get(len(questions) + 1, '')
            })
            question_text = []
            options = []
            question = False
        # Handle the old format for answers
        elif question and line:
            question_text.append(line)

    if question_text:
        questions.append({
            'question': ' '.join(question_text), 
            'options': options, 
            'answer': answer_map.get(len(questions) + 1, '')
        })

    for i, question in enumerate(questions):
        if 'answer' not in question or not question['answer']:
            question['answer'] = answer_map.get(i + 1, '')

    if not questions:
        raise ValueError("No questions found in the file. Please check the file format.")

    random.shuffle(questions)
    return questions

class QuizApp:
    def __init__(self, root):
        """Initialize the main application window."""
        self.root = root
        self.root.title("Dynamic Quiz App")
        self.root.geometry("600x500")
        self.root.config(bg="#f0f0f0")

        # Create a canvas for scrolling
        self.canvas = Canvas(self.root, bg="#f0f0f0")
        self.scrollbar = Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f0f0f0")

        # Configure the scrollable frame
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Title Label
        self.title_label = tk.Label(self.scrollable_frame, text="Quiz App", font=("Arial", 24, "bold"), bg="#f0f0f0", fg="#333")
        self.title_label.pack(pady=10)

        # Input for prefixes
        self.question_prefix_entry = tk.Entry(self.scrollable_frame, font=("Arial", 12), width=40)
        self.question_prefix_entry.pack(pady=5)
        self.question_prefix_entry.insert(0, "Question Prefix,NO.")  # Default prefix

        self.option_prefixes_entry = tk.Entry(self.scrollable_frame, font=("Arial", 12), width=40)
        self.option_prefixes_entry.pack(pady=5)
        self.option_prefixes_entry.insert(0, "A., B., C., D.")  # Default option prefixes

        self.answer_prefix_entry = tk.Entry(self.scrollable_frame, font=("Arial", 12), width=40)
        self.answer_prefix_entry.pack(pady=5)
        self.answer_prefix_entry.insert(0, "Answer:")  # Default answer prefix

        # Load Questions Button
        self.load_button = tk.Button(self.scrollable_frame, text="Load Questions", command=self.load_questions_from_file, bg="#4CAF50", fg="white", font=("Arial", 14))
        self.load_button.pack(pady=10)

        # Score and Percentage Labels
        self.score_label = tk.Label(self.scrollable_frame, text=f"Score: 0", font=("Arial", 14), bg="#f0f0f0")
        self.score_label.pack(pady=5)

        self.attempted_label = tk.Label(self.scrollable_frame, text="Total Attempted: 0 | Total Incorrect: 0 | Percentage Incorrect: 0%", font=("Arial", 12), bg="#f0f0f0")
        self.attempted_label.pack(pady=5)

        self.questions_left_label = tk.Label(self.scrollable_frame, text="Questions Left: 0", font=("Arial", 12), bg="#f0f0f0")
        self.questions_left_label.pack(pady=5)

        # Progress Bar (Battery-like)
        self.progress_canvas = Canvas(self.scrollable_frame, width=200, height=40, bg="#f0f0f0", highlightthickness=0)
        self.progress_canvas.pack(pady=10)
        self.progress_rect = self.progress_canvas.create_rectangle(0, 0, 0, 40, fill="lightgreen")

        # Next button to check the answer
        self.next_button = tk.Button(self.scrollable_frame, text="Next", command=self.check_answer, bg="#4CAF50", fg="white", font=("Arial", 14))
        self.next_button.pack(pady=10)

        # Question display area
        self.question_frame = tk.Frame(self.scrollable_frame, bg="#f0f0f0")
        self.question_frame.pack(fill=tk.BOTH, expand=True)

        # Message Label for loading questions
        self.message_label = tk.Label(self.question_frame, text="Please load questions to start the quiz.", font=("Arial", 14), bg="#f0f0f0")
        self.message_label.pack(pady=10)

        # Other variables
        self.questions = []
        self.current_question = 0
        self.score = 0
        self.incorrect_answers = []
        self.attempted = 0
        self.correct = 0
        self.incorrect = 0
        self.check_vars = []  # Track the states of checkboxes

    def load_questions_from_file(self):
        """Load questions from a file selected by the user."""
        filename = filedialog.askopenfilename(title="Select a Questions File", filetypes=[("Text files", "*.txt")])
        if filename:
            question_prefix = self.question_prefix_entry.get().strip()
            option_prefixes = [prefix.strip() for prefix in self.option_prefixes_entry.get().split(',')]
            answer_prefix = self.answer_prefix_entry.get().strip()

            try:
                self.questions = load_questions(filename, question_prefix, option_prefixes, answer_prefix)
                self.current_question = 0
                self.score = 0
                self.attempted = 0
                self.correct = 0
                self.incorrect = 0
                self.score_label.config(text=f"Score: {self.score}")
                self.attempted_label.config(text="Total Attempted: 0 | Total Incorrect: 0 | Percentage Incorrect: 0%")
                self.questions_left_label.config(text=f"Questions Left: {len(self.questions)}")
                self.load_question()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def load_question(self):
        """Load and display the current question and its options."""
        for widget in self.question_frame.winfo_children():
            widget.destroy()  # Clear previous question and options

        if self.current_question < len(self.questions):
            question_data = self.questions[self.current_question]
            question_label = tk.Label(self.question_frame, text=question_data['question'], wraplength=550, font=("Arial", 14), bg="#f0f0f0", anchor="w")
            question_label.pack(pady=10)

            self.check_vars = []  # Reset checkbox states for new question
            for i, option in enumerate(question_data['options']):
                var = tk.BooleanVar()  # Variable for the checkbox state
                check_button = tk.Checkbutton(self.question_frame, text=option, variable=var, bg="#f0f0f0")
                check_button.pack(anchor=tk.W, pady=5)
                self.check_vars.append(var)  # Track the checkbox state

            self.next_button['state'] = tk.NORMAL
            self.questions_left_label.config(text=f"Questions Left: {len(self.questions) - (self.current_question + 1)}")
            self.message_label.pack_forget()  # Hide the message once questions are loaded

            self.update_progress_bar()

        else:
            self.finish_quiz()

    def check_answer(self):
        """Check the selected answer against the correct answer and update the score."""
        if self.current_question < len(self.questions):
            question_data = self.questions[self.current_question]
            correct_answer = question_data['answer'].strip()

            # Collect selected answers based on checkbox states
            selected_answers = [chr(65 + i) for i, var in enumerate(self.check_vars) if var.get()]  # A=65, B=66, etc.
            selected_answer_string = ''.join(selected_answers)

            self.attempted += 1
            self.attempted_label.config(text=f"Total Attempted: {self.attempted} | Total Incorrect: {self.incorrect} | Percentage Incorrect: {self.calculate_percentage():.2f}%")

            if sorted(selected_answer_string) == sorted(correct_answer):
                self.score += 1
                self.correct += 1
                messagebox.showinfo("Correct!", "Your answer is correct!")
            else:
                self.incorrect_answers.append(question_data['question'])
                self.incorrect += 1
                messagebox.showerror("Incorrect", f"Your answer is incorrect! The correct answer(s) is/are: {correct_answer}.")

            self.score_label.config(text=f"Score: {self.score}")
            self.current_question += 1
            self.load_question()

    def calculate_percentage(self):
        """Calculate the percentage of incorrect answers."""
        return (self.incorrect / self.attempted * 100) if self.attempted > 0 else 0

    def finish_quiz(self):
        """Display the final score and percentage after quiz completion."""
        for widget in self.question_frame.winfo_children():
            widget.destroy()  # Clear the question frame

        total_questions = len(self.questions)
        percentage = (self.score / total_questions * 100) if total_questions > 0 else 0

        final_label = tk.Label(self.question_frame, text=f"Quiz Finished!\nScore: {self.score}/{total_questions}\nPercentage: {percentage:.2f}%", font=("Arial", 16), bg="#f0f0f0")
        final_label.pack(pady=20)

    def update_progress_bar(self):
        """Update the progress bar to reflect the attempted questions."""
        total_questions = len(self.questions)
        if total_questions > 0:
            progress_width = (self.attempted / total_questions) * 200  # Scale the progress bar
            self.progress_canvas.coords(self.progress_rect, 0, 0, progress_width, 40)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
