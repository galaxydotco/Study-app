import json
import random

class FlashcardApp:
    def __init__(self):
        self.flashcards = {}
        self.load_flashcards()
        self.high_incorrect_flashcards = {}
        self.scores = []

    def load_flashcards(self):
        try:
            with open("flashcards.json", "r") as file:
                self.flashcards = json.load(file)
                # Ensure the loaded data is a dictionary
                if not isinstance(self.flashcards, dict):
                    raise ValueError("Flashcards data should be a dictionary.")
                for term, data in self.flashcards.items():
                    if not isinstance(data, dict) or "definition" not in data:
                        raise ValueError(f"Flashcard for term '{term}' is improperly formatted.")
        except (FileNotFoundError, ValueError) as e:
            print(f"Error loading flashcards: {e}")
            self.flashcards = {}

    def save_flashcards(self):
        with open("flashcards.json", "w") as file:
            json.dump(self.flashcards, file)

    def save_high_incorrect_flashcards(self):
        with open("high_incorrect_flashcards.json", "w") as file:
            json.dump(self.high_incorrect_flashcards, file)

    def save_scores(self):
        with open("scores.json", "w") as file:
            json.dump(self.scores, file)

    def load_scores(self):
        try:
            with open("scores.json", "r") as file:
                self.scores = json.load(file)
        except FileNotFoundError:
            self.scores = []

    def add_flashcard(self):
        term = input("Enter the term: ")
        definition = input("Enter the definition: ")
        self.flashcards[term] = {"definition": definition, "incorrect_count": 0}
        self.save_flashcards()
        print("Flashcard saved!")

    def edit_flashcard(self):
        term = input("Enter the term you want to edit: ")
        if term in self.flashcards:
            new_definition = input("Enter the new definition: ")
            self.flashcards[term]["definition"] = new_definition
            self.save_flashcards()
            print("Flashcard updated!")
        else:
            print("Term not found.")

    def delete_flashcard(self):
        term = input("Enter the term you want to delete: ")
        if term in self.flashcards:
            del self.flashcards[term]
            self.save_flashcards()
            print("Flashcard deleted!")
        else:
            print("Term not found.")

    def review_flashcards(self):
        if not self.flashcards:
            print("No flashcards available.")
            return
        
        study_direction = input("Do you want to (1) study terms or (2) study definitions? Enter 1 or 2: ")
        num_flashcards = int(input("How many flashcards do you want to review? "))
        terms = list(self.flashcards.keys())
        random.shuffle(terms)
        
        for i in range(min(num_flashcards, len(terms))):
            if study_direction == "1":
                term = terms[i]
                print(f"Term: {term}")
                input("Press Enter to see the definition...")
                print(f"Definition: {self.flashcards[term]['definition']}\n")
            elif study_direction == "2":
                definition = self.flashcards[terms[i]]["definition"]
                print(f"Definition: {definition}")
                answer = input("What is the term? ")
                if answer == terms[i]:
                    print("Correct!\n")
                else:
                    self.flashcards[terms[i]]["incorrect_count"] += 1
                    print(f"Incorrect! The correct term is: {terms[i]}")
                    print(f"This term has been answered incorrectly {self.flashcards[terms[i]]['incorrect_count']} times.\n")
            else:
                print("Invalid option. Please start again.")
                break

        self.save_flashcards()  
        self.update_high_incorrect_flashcards()

    def update_high_incorrect_flashcards(self):
        self.high_incorrect_flashcards = {
            term: data for term, data in self.flashcards.items() 
            if isinstance(data, dict) and "incorrect_count" in data and data["incorrect_count"] > 0
        }
        self.save_high_incorrect_flashcards()

    def review_high_incorrect_flashcards(self):
        if not self.high_incorrect_flashcards:
            print("No flashcards with incorrect answers.")
            return
        
        terms = list(self.high_incorrect_flashcards.keys())
        random.shuffle(terms)

        num_flashcards = int(input("How many incorrect flashcards do you want to review? "))
        
        for i in range(min(num_flashcards, len(terms))):
            term = terms[i]
            definition = self.high_incorrect_flashcards[term]["definition"]
            print(f"Definition: {definition}")
            answer = input("What is the term? ")
            if answer == term:
                print("Correct!\n")
            else:
                print(f"Incorrect! The correct term is: {term}")
                print(f"This term has been answered incorrectly {self.high_incorrect_flashcards[term]['incorrect_count']} times.\n")

    def quiz(self):
        if not self.flashcards:
            print("No flashcards available for quizzing.")
            return
        
        num_questions = int(input("How many questions do you want in the quiz? "))
        terms = list(self.flashcards.keys())
        random.shuffle(terms)
        
        score = 0

        for i in range(min(num_questions, len(terms))):
            correct_term = terms[i]
            definition = self.flashcards[correct_term]["definition"]
            choices = random.sample(terms, 3)  # Get 3 random terms
            choices.append(correct_term)  # Add the correct term
            random.shuffle(choices)  # Shuffle the choices

            print(f"\nDefinition: {definition}")
            for idx, choice in enumerate(choices, start=1):
                print(f"{chr(96 + idx)}) {choice}")  # a) b) c) d)

            answer = input("Select the correct term (a, b, c, d): ").lower()
            if choices[ord(answer) - 97] == correct_term:  # 'a' is 97 in ASCII
                print("Correct!")
                score += 1
            else:
                print(f"Incorrect! The correct term is: {correct_term}")

        self.scores.append(score)
        self.save_scores()
        print(f"\nYour score: {score}/{min(num_questions, len(terms))}")

    def view_scores(self):
        if not self.scores:
            print("No scores available.")
            return
        print("\nScores:")
        for i, score in enumerate(self.scores, start=1):
            print(f"Attempt {i}: {score}")

    def list_flashcards(self):
        if not self.flashcards:
            print("No flashcards available.")
            return
        print("\nFlashcards:")
        for term, data in self.flashcards.items():
            if isinstance(data, dict) and "definition" in data:
                print(f"Term: {term} | Definition: {data['definition']}")
            else:
                print(f"Term: {term} | Definition: {data}")  # Fallback for incorrect data structure

    def main_menu(self):
        self.load_scores()
        while True:
            print("\nFlashcard App")
            print("1. Add Flashcard")
            print("2. Edit Flashcard")
            print("3. Delete Flashcard")
            print("4. Review Flashcards")
            print("5. Review Incorrect Flashcards")
            print("6. Take a Quiz")
            print("7. View Scores")
            print("8. List Flashcards")
            print("9. Exit")
            choice = input("Choose an option: ")

            if choice == "1":
                self.add_flashcard()
            elif choice == "2":
                self.edit_flashcard()
            elif choice == "3":
                self.delete_flashcard()
            elif choice == "4":
                self.review_flashcards()
            elif choice == "5":
                self.review_high_incorrect_flashcards()
            elif choice == "6":
                self.quiz()
            elif choice == "7":
                self.view_scores()
            elif choice == "8":
                self.list_flashcards()
            elif choice == "9":
                break
            else:
                print("Invalid option. Please try again.")

if __name__ == "__main__":
    app = FlashcardApp()
    app.main_menu()

if __name__ == "__main__":
    app = FlashcardApp()
    app.main_menu()
