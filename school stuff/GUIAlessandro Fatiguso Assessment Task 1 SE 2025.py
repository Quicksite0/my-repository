import tkinter as tk
import random
import time

class MathCyberAdventureGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Cyber Adventure")
        self.root.geometry("500x400")

        self.dark_mode = False
        self.light_bg = "white"
        self.light_fg = "black"
        self.dark_bg = "#333333"
        self.dark_fg = "white"

        self.set_theme()

        self.difficulty = None
        self.current_problem = None
        self.correct_answer = None
        self.data_recovered_count = 0
        self.num_questions = 5
        self.data_problems = []
        self.game_stage = "difficulty_selection"
        self.intel_obtained = False
        self.processing_answer = False
        self.delay_active = False

        self.label = tk.Label(root, text="Welcome to the Math Cyber Adventure!", wraplength=400, justify="center", **self.label_style())
        self.label.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        self.entry = tk.Entry(root, **self.entry_style())
        self.entry.pack(pady=10, padx=20, fill=tk.X)

        self.submit_button = tk.Button(root, text="Submit", command=self.submit_answer, **self.button_style())
        self.submit_button.pack(pady=10, padx=20)

        self.dark_mode_button = tk.Button(root, text="Toggle Dark Mode", command=self.toggle_dark_mode, **self.button_style())
        self.dark_mode_button.pack(pady=10, padx=20)

        self.start_over_button = tk.Button(root, text="Start Over", command=self.restart_game, **self.button_style())

        self.update_display()

    def set_theme(self):
        if self.dark_mode:
            self.root.config(bg=self.dark_bg)
        else:
            self.root.config(bg=self.light_bg)

    def label_style(self):
        if self.dark_mode:
            return {"bg": self.dark_bg, "fg": self.dark_fg, "font": ("Arial", 14)}
        else:
            return {"bg": self.light_bg, "fg": self.light_fg, "font": ("Arial", 14)}

    def entry_style(self):
        if self.dark_mode:
            return {"bg": "#555555", "fg": self.dark_fg, "font": ("Arial", 12), "relief": tk.SOLID, "borderwidth": 1}
        else:
            return {"bg": "white", "fg": "black", "font": ("Arial", 12), "relief": tk.SOLID, "borderwidth": 1}

    def button_style(self):
        if self.dark_mode:
            return {"bg": "#555555", "fg": self.dark_fg, "font": ("Arial", 12), "relief": tk.RAISED, "borderwidth": 2, "padx": 10, "pady": 5}
        else:
            return {"bg": "#f0f0f0", "fg": "black", "font": ("Arial", 12), "relief": tk.RAISED, "borderwidth": 2, "padx": 10, "pady": 5}

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.set_theme()
        self.label.config(**self.label_style())
        self.entry.config(**self.entry_style())
        self.submit_button.config(**self.button_style())
        self.dark_mode_button.config(**self.button_style())

    def restart_game(self):
        self.difficulty = None
        self.current_problem = None
        self.correct_answer = None
        self.data_recovered_count = 0
        self.num_questions = 5
        self.data_problems = []
        self.game_stage = "difficulty_selection"
        self.intel_obtained = False
        self.processing_answer = False
        self.delay_active = False
        self.update_display()
        self.start_over_button.pack_forget()
        self.root.geometry("500x400")

    def update_display(self, text=None):
        if text:
            self.label.config(text=text)
        elif self.game_stage == "difficulty_selection":
            self.label.config(text="Select difficulty: Easy, Medium or Hard:")
            self.entry.config(state=tk.NORMAL)
            self.entry.delete(0, tk.END)
            self.submit_button.config(command=self.submit_answer, state=tk.NORMAL)
        elif self.game_stage == "intro":
            intro_text = "Welcome to the Math Cyber Adventure!\n"
            intro_text += "You are a cyber security specialist using math to track down hackers.\n"
            intro_text += "There are portals to the Mainframe and Data Mines.\n"
            intro_text += "Solve the math challenges to secure the system!\n"
            self.label.config(text=intro_text)
            self.entry.config(state=tk.DISABLED)
            self.submit_button.config(command=self.choose_intel_stage, state=tk.NORMAL)
        elif self.game_stage == "choose_intel":
            self.label.config(text="To get intel, solve this problem:")
            self.entry.config(state=tk.NORMAL)
            self.entry.delete(0, tk.END)
            self.generate_math_problem()
            self.label.config(text=self.label.cget("text") + f"\n{self.current_problem} =?")
            self.submit_button.config(command=self.submit_answer, state=tk.NORMAL)
        elif self.game_stage == "choose_portal":
            self.label.config(text="Portal? (mainframe/data mines):")
            self.entry.config(state=tk.NORMAL)
            self.entry.delete(0, tk.END)
            self.submit_button.config(command=self.handle_portal_choice, state=tk.NORMAL)
        elif self.game_stage == "mainframe_portal":
            self.label.config(text="You find digital footprints left by the hackers.\nTo decode a vital clue, solve this:")
            self.entry.config(state=tk.NORMAL)
            self.entry.delete(0, tk.END)
            self.generate_math_problem()
            self.label.config(text=self.label.cget("text") + f"\n{self.current_problem} =?")
            self.submit_button.config(command=self.submit_answer, state=tk.NORMAL)
        elif self.game_stage == "data_mines_portal":
            self.label.config(text="You trigger a hidden trap set by the hackers!\nTo escape, solve this:")
            self.entry.config(state=tk.NORMAL)
            self.entry.delete(0, tk.END)
            self.generate_math_problem()
            self.label.config(text=self.label.cget("text") + f"\n{self.current_problem} =?")
            self.submit_button.config(command=self.submit_answer, state=tk.NORMAL)
        elif self.game_stage == "recover_data_intro":
            recover_data_text = "You have accessed a hidden data cache within the Mainframe!\n"
            recover_data_text += "To decrypt and recover the data, you must correctly answer a series of math problems."
            self.label.config(text=recover_data_text)
            self.entry.config(state=tk.DISABLED)
            self.submit_button.config(command=self.start_data_recovery, state=tk.NORMAL)
        elif self.game_stage == "recover_data_question":
            if self.data_problems:
                problem_text, _ = self.data_problems[0]
                self.label.config(text=f"Question {self.num_questions - len(self.data_problems) + 1}: {problem_text} =?")
                self.entry.config(state=tk.NORMAL)
                self.entry.delete(0, tk.END)
                self.submit_button.config(command=self.submit_data_answer, state=tk.NORMAL)
            else:
                self.handle_data_recovery_completion()
        elif self.game_stage == "final_question":
            self.label.config(text=f"{self.current_problem} =?")
            self.entry.config(state=tk.NORMAL)
            self.entry.delete(0, tk.END)
            self.submit_button.config(command=self.submit_final_answer, state=tk.NORMAL)
        elif self.game_stage == "game_over":
            self.label.config(text="Game Over!")
            self.entry.config(state=tk.DISABLED)
            self.submit_button.config(state=tk.DISABLED)
            self.start_over_button.pack(pady=10, padx=20)

    def difficulty_selection_logic(self, difficulty):
        if difficulty == "easy":
            self.difficulty = "easy"
            self.update_display("Easy difficulty selected!")
            self.game_stage = "intro"
            self.update_display()
        elif difficulty == "medium":
            self.difficulty = "medium"
            self.update_display("Medium difficulty selected!")
            self.game_stage = "intro"
            self.update_display()
        elif difficulty == "hard":
            self.difficulty = "hard"
            self.update_display("Hard difficulty selected!")
            self.game_stage = "intro"
            self.update_display()
        else:
            self.update_display("Invalid difficulty, Easy, Medium or Hard.")
            self.game_stage = "difficulty_selection"

    def choose_intel_stage(self):
        self.game_stage = "choose_intel"
        self.update_display()

    def handle_intel_answer(self, user_answer):
        try:
            user_answer = float(user_answer)
            if user_answer == self.correct_answer:
                self.label.config(text="Correct! Intercepted a message with the code MF!")
                self.intel_obtained = True
                self.start_delay(3000, "choose_portal")
            else:
                self.update_display("Incorrect! No intel available!")
                self.intel_obtained = False
                self.start_delay(3000, "choose_portal")
        except ValueError:
            self.update_display("Invalid input. No intel available.")
            self.game_stage = "game_over"
            self.update_display()
        finally:
            pass

    def handle_portal_choice(self):
        portal = self.entry.get().lower()
        if portal == "mainframe":
            self.game_stage = "mainframe_portal"
            self.update_display()
        elif portal == "data mines":
            self.game_stage = "data_mines_portal"
            self.update_display()
        else:
            self.update_display("Invalid input!")
            self.game_stage = "choose_portal"
            self.update_display()

    def handle_mainframe_answer(self, user_answer):
        try:
            user_answer = float(user_answer)
            if user_answer == self.correct_answer:
                self.update_display("Correct!\nYou follow them and catch the hackers in the act.\nYou have successfully secured the system!")
                self.game_stage = "recover_data_intro"
                self.update_display()
            else:
                self.update_display("Game Over!\nIncorrect! The hackers are alerted! They have escaped.\nRegroup and try again.")
                self.start_delay(3000, "game_over")
        except ValueError:
            self.update_display("Game Over!\nInvalid input. The hackers escaped!")
            self.start_delay(3000, "game_over")

    def handle_data_mines_answer(self, user_answer):
        try:
            user_answer = float(user_answer)
            if user_answer == self.correct_answer:
                self.update_display("Correct! You escaped the trap!\nHowever, the hackers have escaped! Regroup and try again.")
                self.start_delay(3000, "game_over")
            else:
                self.update_display("Game Over!\nIncorrect! You are caught in a loop of corrupted data.\nThe hackers escaped! Regroup and try again.")
                self.start_delay(3000, "game_over")
        except ValueError:
            self.update_display("Game Over!\nInvalid input. You are trapped!")
            self.start_delay(3000, "game_over")

    def start_delay(self, duration, next_stage=None):
        self.delay_active = True
        self.next_stage_after_delay = next_stage
        self.root.after(duration, self.end_delay)

    def end_delay(self):
        self.delay_active = False
        if self.next_stage_after_delay:
            self.game_stage = self.next_stage_after_delay
            self.update_display()
            if self.game_stage == "game_over":
                self.start_over_button.pack(pady=10, padx=20)

    def submit_answer(self, event=None):
        if self.processing_answer or self.game_stage == "game_over" or self.delay_active:
            return
        self.processing_answer = True
        user_answer = self.entry.get()
        self.entry.delete(0, tk.END)
        if self.game_stage == "difficulty_selection":
            self.difficulty_selection_logic(user_answer.lower())
        elif self.game_stage == "intro":
            self.game_stage = "choose_intel"
            self.update_display()
        elif self.game_stage == "choose_intel":
            self.handle_intel_answer(user_answer)
        elif self.game_stage == "mainframe_portal":
            self.handle_mainframe_answer(user_answer)
        elif self.game_stage == "data_mines_portal":
            self.handle_data_mines_answer(user_answer)
        elif self.game_stage == "recover_data_question":
            self.submit_data_answer()
        elif self.game_stage == "choose_portal":
            self.handle_portal_choice()
        self.processing_answer = False

    def generate_math_problem(self):
        num1 = 0
        num2 = 0
        operator = ""
        if self.difficulty == "easy":
            num1 = random.randint(5, 10)
            num2 = random.randint(1, 5)
            operator = random.choice(["+", "-"])
        elif self.difficulty == "medium":
            num1 = random.randint(10, 25)
            num2 = random.randint(2, 12)
            operator = random.choice(["+", "-", "*"])
        elif self.difficulty == "hard":
            num1 = random.randint(10, 25)
            num2 = random.randint(2, 12)
            operator = random.choice(["+", "-", "*", "/"])
            if operator == "/":
                num1 = num2 * random.randint(1,10)

        self.current_problem = f"{num1} {operator} {num2}"
        self.correct_answer = eval(self.current_problem)

    def start_data_recovery(self):
        self.game_stage = "recover_data_question"
        self.data_problems = []
        for _ in range(self.num_questions):
            num1 = 0
            num2 = 0
            operator = ""
            if self.difficulty == "easy":
                num1 = random.randint(5, 10)
                num2 = random.randint(1, 5)
                operator = random.choice(["+", "-"])
            elif self.difficulty == "medium":
                num1 = random.randint(10, 25)
                num2 = random.randint(2, 12)
                operator = random.choice(["+", "-", "*"])
            elif self.difficulty == "hard":
                num1 = random.randint(10, 25)
                num2 = random.randint(2, 12)
                operator = random.choice(["+", "-", "*", "/"])
                if operator == "/":
                    num1 = num2 * random.randint(1,10)
            problem = (f"{num1} {operator} {num2}")
            answer = eval(problem)
            self.data_problems.append((problem, answer))
        self.data_recovered_count = 0
        self.update_display()

    def submit_data_answer(self):
        if self.data_problems:
            problem_text, correct_answer = self.data_problems[0]
            user_answer_str = self.entry.get()
            self.entry.delete(0, tk.END)
            try:
                user_answer = float(user_answer_str)
                if user_answer == correct_answer:
                    self.update_display("Correct! Data fragment recovered.")
                    self.data_recovered_count += 1
                else:
                    self.update_display(f"Incorrect! The correct answer was {correct_answer}.")
            except ValueError:
                self.update_display("Game Over!\nInvalid input. The data fragment remains encrypted.")
                self.start_delay(3000, "game_over")
            finally:
                self.data_problems = self.data_problems[1:]
                if not self.data_problems:
                    self.handle_data_recovery_completion()
                else:
                    self.update_display()
        else:
            self.handle_data_recovery_completion()

    def handle_data_recovery_completion(self):
        if self.data_recovered_count == self.num_questions:
            self.update_display(f"Success! You have recovered {self.data_recovered_count} out of {self.num_questions} data fragments.\nThe recovered data reveals a vulnerability in the hacker's system! One more question to secure the data!")
            self.generate_math_problem()
            self.game_stage = "final_question"
            self.update_display()
        else:
            self.update_display(f"Unsuccessful. You have only recovered {self.data_recovered_count} out of {self.num_questions} data fragments.\nThe data remains fragmented and incomplete.")
            self.game_stage = "game_over"
            self.start_over_button.pack(pady=10, padx=20)

    def submit_final_answer(self):
        user_answer_str = self.entry.get()
        self.entry.delete(0, tk.END)
        try:
            user_answer = float(user_answer_str)
            if user_answer == self.correct_answer:
                self.update_display("Correct! Data has been secured from the hackers, good job!")
            else:
                self.update_display(f"Incorrect. Data has been secured from the hackers, good job!")
        except ValueError:
            self.update_display("Game Over!\nInvalid input. The data fragment remains encrypted.")
            self.start_delay(3000, "game_over")
        finally:
            self.start_delay(3000, "game_over")

if __name__ == "__main__":
    root = tk.Tk()
    gui = MathCyberAdventureGUI(root)
    root.mainloop()
