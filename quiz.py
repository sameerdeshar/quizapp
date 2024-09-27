import tkinter as tk
from tkinter import messagebox, filedialog, Scrollbar, Canvas
import random
import re

def load_questions(filename, question_prefix, option_prefixes, answer_prefix):
    """Load questions from a specified file, parsing them based on provided prefixes."""
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    questions = []  # List to hold all the questions
    answer_map = {}  # Dictionary to map question numbers to their answers
    
    # Create a mapping for answers from the file
    for line in lines:
        line = line.strip()
        if re.match(r'^\d+\.\s*[A-Z]', line):
            number, answer = line.split('.', 1)
            answer_map[int(number.strip())] = answer.strip()

    question_text = []  # To store text of the current question
    options = []  # To store options for the current question
    question = False  # Flag to track if we're currently building a question

    for line in lines:
        line = line.strip()
        
        # Check for the start of a question
        if line.startswith(question_prefix):
            if question:  # If we were already building a question, save it
                questions.append({'question': ' '.join(question_text), 'options': options, 'answer': answer_map.get(len(questions) + 1, '')})
                question_text = []  # Reset for the new question
                options = []  # Reset options for the new question
            
            question = True  # Set flag to indicate we are in a question
            question_text.append(line[len(question_prefix):].strip())  # Add the question text
        
        # If we're building a question, check for options and answer prefix
        elif question:
            # Check for option prefixes
            if any(line.startswith(prefix) for prefix in option_prefixes):
                options.append(line)  # Add option to the list
            elif line.startswith(answer_prefix):
                # Save the answer directly
                questions.append({'question': ' '.join(question_text), 'options': options, 'answer': line.split(": ")[1].strip()})
                question_text = []  # Reset question text after saving
                options = []  # Reset options after saving
                question = False  # End the current question
            elif line:  # Non-empty line while in question context
                question_text.append(line)  # Collect the rest of the question lines

        # Empty line signifies the end of the current question
        elif question and line == "":
            questions.append({'question': ' '.join(question_text), 'options': options, 'answer': answer_map.get(len(questions) + 1, '')})
            question_text = []  # Reset for the next question
            options = []  # Reset options for the next question
            question = False  # End the current question

    # Add the last question if it exists
    if question_text:
        questions.append({'question': ' '.join(question_text), 'options': options, 'answer': answer_map.get(len(questions) + 1, '')})

    # Fill in missing answers for questions without one
    for i, question in enumerate(questions):
        if 'answer' not in question or not question['answer']:
            question['answer'] = answer_map.get(i + 1, '')

    if not questions:
        raise ValueError("No questions found in the file. Please check the file format.")

    random.shuffle(questions)  # Shuffle the questions for randomness
    return questions

class QuizApp:
    def __init__(self, root):
        """Initialize the main application window."""
        self.root = root
        self.root.title("Dynamic Quiz App")
        self.root.geometry("600x600")
        self.root.config(bg="#f0f0f0")

        # Create a canvas for scrolling
        self.canvas = Canvas(root, bg="#f0f0f0")
        self.scrollbar = Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f0f0f0")

        # Configure the scrollable frame
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
        self.question_prefix_entry.insert(0, "Question Prefix,NO.")  # Default prefix

        self.option_prefixes_entry = tk.Entry(self.scrollable_frame, font=("Arial", 12), width=40)
        self.option_prefixes_entry.pack(pady=5)
        self.option_prefixes_entry.insert(0, "A., B., C., D.")  # Default option prefixes

        self.answer_prefix_entry = tk.Entry(self.scrollable_frame, font=("Arial", 12), width=40)
        self.answer_prefix_entry.pack(pady=5)
        self.answer_prefix_entry.insert(0, "Answer:")  # Default answer prefix

        # Load Questions Button
        self.load_button = tk.Button(self.scrollable_frame, text="Load Questions", command=self.load_questions_from_file, bg="#4CAF50", fg="white", font=("Arial", 14))
        self.load_button.pack(pady=20)

        # Score and Percentage Labels
        self.score_label = tk.Label(self.scrollable_frame, text=f"Score: 0", font=("Arial", 14), bg="#f0f0f0")
        self.score_label.pack(pady=10)

        self.percentage_label = tk.Label(self.scrollable_frame, text="Percentage: 0%", font=("Arial", 14), bg="#f0f0f0")
        self.percentage_label.pack(pady=10)

        # Next button to check the answer
        self.next_button = tk.Button(self.scrollable_frame, text="Next", command=self.check_answer, bg="#4CAF50", fg="white", font=("Arial", 14))
        self.next_button.pack(pady=20)

        # Question display area
        self.question_frame = tk.Frame(self.scrollable_frame, bg="#f0f0f0")
        self.question_frame.pack(fill=tk.BOTH, expand=True)

        # Centering the content
        self.center_content()

        # Other variables
        self.questions = []  # List of loaded questions
        self.current_question = 0  # Index of the current question
        self.score = 0  # User's score
        self.incorrect_answers = []  # List to store incorrect answers

        # Bind resize event to adjust layout
        self.root.bind("<Configure>", self.center_content)

    def center_content(self, event=None):
        """Center the scrollable frame in the canvas."""
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        frame_width = self.scrollable_frame.winfo_width()
        frame_height = self.scrollable_frame.winfo_height()

        x = (width - frame_width) // 2
        y = (height - frame_height) // 2

        self.canvas.place(x=x, y=y, width=frame_width, height=frame_height)

    def load_questions_from_file(self):
        """Load questions from a file selected by the user."""
        filename = filedialog.askopenfilename(title="Select a Questions File", filetypes=[("Text files", "*.txt")])
        if filename:
            question_prefix = self.question_prefix_entry.get().strip()
            option_prefixes = [prefix.strip() for prefix in self.option_prefixes_entry.get().split(',')]
            answer_prefix = self.answer_prefix_entry.get().strip()

            try:
                # Load the questions using the specified prefixes
                self.questions = load_questions(filename, question_prefix, option_prefixes, answer_prefix)
                self.current_question = 0
                self.score = 0
                self.score_label.config(text=f"Score: {self.score}")  # Reset score label
                self.percentage_label.config(text="Percentage: 0%")  # Reset percentage label
                self.load_question()  # Load the first question
            except ValueError as e:
                # Show error if questions could not be loaded
                messagebox.showerror("Error", str(e))

    def load_question(self):
        """Load and display the current question and its options."""
        for widget in self.question_frame.winfo_children():
            widget.destroy()  # Clear previous question and options

        if self.current_question < len(self.questions):
            question_data = self.questions[self.current_question]
            question_label = tk.Label(self.question_frame, text=question_data['question'], wraplength=550, font=("Arial", 16), bg="#f0f0f0")
            question_label.pack(pady=10)  # Display the question

            if ',' in question_data['answer']:
                # Handle multiple correct answers
                self.check_vars = []
                for option in question_data['options']:
                    var = tk.BooleanVar()  # Variable to hold the checkbox state
                    check_button = tk.Checkbutton(self.question_frame, text=option, variable=var, bg="#f0f0f0")
                    check_button.pack(anchor=tk.W)  # Place checkbox in the question frame
                    self.check_vars.append((var, option))  # Append to list for answer checking
            else:
                # For single correct answer
                self.selected_option = tk.StringVar()  # Variable to hold selected answer
                for option in question_data['options']:
                    radio_button = tk.Radiobutton(self.question_frame, text=option, variable=self.selected_option, value=option, bg="#f0f0f0")
                    radio_button.pack(anchor=tk.W)  # Place radio button in the question frame

            self.next_button['state'] = tk.NORMAL  # Enable the Next button

        else:
            # No more questions
            self.finish_quiz()

    def check_answer(self):
        """Check the selected answer against the correct answer and update the score."""
        if self.current_question < len(self.questions):
            question_data = self.questions[self.current_question]
            correct_answer = question_data['answer']

            if ',' in correct_answer:  # Check for multiple answers
                selected_answers = [var[1] for var in self.check_vars if var[0].get()]  # Collect selected answers
                if sorted(selected_answers) == sorted(correct_answer.split(', ')):  # Compare with correct answers
                    self.score += 1  # Increase score if correct
                else:
                    self.incorrect_answers.append(question_data['question'])  # Save incorrect answer
            else:
                # For single answer comparison
                if self.selected_option.get() == correct_answer:
                    self.score += 1  # Increase score if correct
                else:
                    self.incorrect_answers.append(question_data['question'])  # Save incorrect answer

            self.score_label.config(text=f"Score: {self.score}")  # Update score display
            self.current_question += 1  # Move to the next question
            self.load_question()  # Load the next question

    def finish_quiz(self):
        """Display the final score and percentage after quiz completion."""
        for widget in self.question_frame.winfo_children():
            widget.destroy()  # Clear the question frame

        total_questions = len(self.questions)
        percentage = (self.score / total_questions) * 100 if total_questions > 0 else 0

        final_label = tk.Label(self.question_frame, text=f"Quiz Finished!\nScore: {self.score}/{total_questions}\nPercentage: {percentage:.2f}%", font=("Arial", 16), bg="#f0f0f0")
        final_label.pack(pady=20)  # Show final score and percentage

        if self.incorrect_answers:
            incorrect_label = tk.Label(self.question_frame, text="Incorrect Answers:\n" + "\n".join(self.incorrect_answers), font=("Arial", 14), bg="#f0f0f0")
            incorrect_label.pack(pady=10)  # Display incorrect answers

if __name__ == "__main__":
    root = tk.Tk()  # Create the main application window
    app = QuizApp(root)  # Initialize the QuizApp
    root.mainloop()  # Start the main loop
