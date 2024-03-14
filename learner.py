"""
Learning tool to learn learnables for learning...

TODO
LOW PRIO:
    # CONNECT CHECK: ASK FOR FAULTY PAIRS INDIVIDUALLY, RATHER THAN HAVING TO INSERT THE WHOLE ANSWER AGAIN
"""
from random import randint, shuffle, sample, choice
from difflib import SequenceMatcher


class LearnObject:
    """A Learn object."""

    def __init__(self, term: str, definition: str, hint_delimiter: str = ". ", year: str = None) -> None:
        """
        Class initializer.

        Attributes:
        term - term
        definition - term definition
        hint_delimiter - substring where the definition is split into hints.

        Variables:
        self.term - term
        self.definition - definition
        self.hints - a list of hints. when doing an exercise, a hint is
                randomly selected as the definition for the term. Allows for multiple
                definitions to be set for one term.
        """
        self.term = term
        self.year = year
        self.definition = self.definition_censor(definition)
        self.hints = self.hint_splitter(self.definition, hint_delimiter)

    def hint_splitter(self, definition: str, hint_delimiter: str) -> list:
        """
        Hint splitter.

        splits definition into list of hints.

        returns:
        list of hints
        """
        return definition.split(hint_delimiter)

    def definition_censor(self, definition: str) -> str:
        """
        Definition censor.

        Removes the term from the definition and replaces it with "___".

        returns:
        censored definition
        """
        return definition.replace(self.term, "___")

    def lower(self) -> str:
        """
        Class lower() function.

        Is needed for __eq__ function

        returns:
        lowered self.term
        """
        return self.term.lower()

    def __eq__(self, other) -> bool:
        """
        Class equal function.

        function compares lowered self.term and a lowered string.
        will work with string and LearnObject.

        returns:
        bool - true if self.term and other match else false
        """
        return self.lower() == other.lower()


class LearnSet:
    """Set of LearnObjects, and exercise functions."""

    def __init__(self, name: str, set: list[LearnObject] = [], correct: dict = {}) -> None:
        """
        Class initializer.

        Attributes:
        name - name of the set
        set - list of LearnObject objects
        correct - dictionary of term and amount of correct answers pairs

        Variables:
        self.name - name of the set
        self.set - lost of LearnObject objects
        self.correct - dictionary of term and amount of correct answers pairs
        self.test_missed_answers - incorrect test answers
        self.min_ratio - minimum ratio which lets answer overwriting. Ratio is calculated with
                         difflib.SequenceMatcher
        """
        self.name = name
        self.set: list[LearnObject] = set
        self.correct = correct
        self.test_missed_answers = 0
        self.min_ratio = 0.8
        if set:
            self.set_info()

    def __add__(self, other) -> any:
        """
        Class addition method.

        unifies two LearnSet object together and creates a new one.

        returns:
        unified LearnSet with name union.
        """
        return LearnSet("union", self.set + other.set, self.correct | other.correct)

    def set_info(self):
        """
        Print set info
        """
        print(f"Set name: {self.name}")
        print(f"{len(self.set)} terms in the set.")
        print(f"Typo ratio is {self.min_ratio}\n")

    def add(self, obj: LearnObject) -> None:
        """
        Add a term to the set.

        Function appends LearnObject object to self.set list.
        also adds a record to self.correction dictionary.
        """
        self.set.append(obj)
        self.correct[obj.term] = 0

    def get_result(self) -> None:
        """
        Result function.

        prints the result of the learning session.
        """
        print("Your result:\n")
        total = 0
        for term in self.correct:
            if self.correct[term]:
                total += self.correct[term]
                print(f"{term:<15}{self.correct[term]}")
        print(f"Total: {total} out of {len(self.correct) * 6}\n")

    def get_random(self, number: int) -> LearnObject | list[LearnObject]:
        """
        Return number of random LearnObjects from self.set.

        returns:
        LearnObject, if number is 1
        list of LearnObjects, if number is greater than 1
        """
        if number == 1:
            return choice(self.set)
        return sample(self.set, number)

    def match_ratio(self, answer: str, correct: str) -> bool:
        """
        Typo checker.

        Checks for possible typos with difflib.SequenceMatcher

        return:
        bool - True if ratio is bigger then self.min_ratio else False
        """
        ratio = SequenceMatcher(None, answer, correct).ratio()
        if ratio >= self.min_ratio:
            return True
        return False

    def multiple_choice(self, nr_options: int, correct: LearnObject = None) -> None:
        """
        Multiple choice excercise.

        Picks a random LearnObject from self.set and prints a random hint and multiple options.

        variables:
        nr_options - the number of choices

        optional:
        correct - when provided, will use provided LearnObject as the correct answer

        inputs:
        answer - users answer to the question
        """
        if not correct:
            correct = self.get_random(1)
        choices = self.get_random(nr_options - 1)
        while correct in choices:
            choices = self.get_random(nr_options - 1)
        choices += [correct]
        print(choice(correct.hints) + "\n")
        names = list(map(lambda x: x.term, choices))
        shuffle(names)
        print(names)
        answer = input("Enter the correct term: ")
        self.choice_and_answer_check(correct, answer)
    
    def write_answer(self, correct: LearnObject = None) -> None:
        """
        Writing exercise.

        Picks a random LearnObject from self.set.

        variables:
        optional:
        correct - when provided, will use provided LearnObject as the correct answer

        inputs:
        answer - users answer to the question
        """
        if not correct:
            correct = self.get_random(1)
        print(choice(correct.hints) + "\n")
        answer = input("Enter the correct term: ")
        self.choice_and_answer_check(correct, answer)

    def choice_and_answer_check(self, correct: LearnObject, answer: str) -> None:
        """
        Check whether provided answer is correct.

        Checks the multiple choice and write exercise answers.

        Variables:
        correct - the correct LearnObject object
        answer - users answer

        modifications:
        self.correct - modifies the correct LearnObjects correct value, used in learning function
        self.test_missed_answers - modifies the amount of missed items in a test, used in test function
        """
        if correct == answer:
            print("Correct!")
            self.correct[correct.term] += 1
            input("Press {enter} to continue...\n")
        else:
            print(f"False! Correct: {correct.term}")
            if self.match_ratio(answer.lower(), correct.lower()):
                if input("There seems to be a typo, overwrite? ").lower() in ["y", "yes", "true", "1", "t"]:
                    print("Overwriting...")
                    self.correct[correct.term] += 1
                    input("Press {enter} to continue...\n")
                    return None
            self.correct[correct.term] -= 1 if self.correct[correct.term] else 0
            self.test_missed_answers += 1
            input("Press {enter} to continue...\n")

    def year(self, correct: LearnObject = None, ask: bool = True) -> None:
        """Ask the year."""
        if not correct:
            correct = self.get_random(1)
        if ask:
            print(correct.term)
        answer = input("Enter the correct year: ")
        self.year_check(correct, answer)
    
    def year_check(self, correct: LearnObject, answer: str) -> None:
        """Check the year."""
        if correct.year == answer:
            print("Correct!")
        else:
            print(f"False! Correct: {correct.year}")
        input("Press {enter} to continue...\n")


    def learn(self, round_length: int, ask_years: bool = False) -> None:
        """
        Learn module.

        Joint exercise, that uses multiple choice and write exercises.
        keeps track of how many times a term is answered correctly.
        dynamically changes the exercise type, if enough multiple choice
        exercises are answered correctly.

        finish when every term is answered correctly 6 times.
        """
        self.correct = {term: 0 for term in self.correct}
        round_nr = 0

        while True:
            round_nr += 1
            for question_number in range(round_length):
                if all(score == 6 for score in self.correct.values()):
                    print("Congratulations! All Done!")
                    return None
                print(f"##### {question_number + 1}. #####")
                correct = self.get_random(1)
                while self.correct[correct.term] > 5:
                    correct = self.get_random(1)
                if self.correct[correct.term] > 2:
                    self.write_answer(correct)
                else:
                    self.multiple_choice(4, correct)
                if correct.year:
                    if ask_years:
                        self.year(correct, False)
                    else:
                        print(correct.year)
                        input("Press {enter} to continue...\n")
            print("\n")
            self.get_result()
            if input(f"You are done with round {round_nr}! Continue? ").lower() in ["n", "no", "false", "0", "f"]:
                print("\n")
                break

    def connect(self, nr_options: int = 8) -> None:
        """
        Connect exercise.

        prints a number of terms and definitions and shuffles them.

        variables:
        nr_options - the number of randomly picked term

        inputs:
        answer - the answer to the question, has to be in Enter the correct pairs {nr} {term}, {nr} {term}, ... format.
        """
        choices = self.get_random(nr_options)
        shuffle(choices)
        names = list(map(lambda x: x.term, choices))
        shuffle(choices)
        option = 1
        for ch in choices:
            print(f"{option}. {choice(ch.hints)}")
            option += 1
        print("\n")
        print(names)
        answer = input("\nEnter the correct pairs {nr} {term}, {nr} {term}, ...\n")
        self.connect_check(choices, answer)

    def connect_answer_check(self, answer: str) -> dict:
        """
        Check the connect answer for format errors and map to dictionary.

        If an error is found, promts a new answer input.
        maps the string input to a dictionary with definition number as the key and term as the value.

        returns:
        dictionary of answered definition number and term pairs
        """
        if "," not in answer:
            answers = [answer.split(" ")]
        else:
            answers = [i.split(" ") for i in answer.split(", ")]
        if answers == [[""]]:
            answers = {}
        elif not all([len(pair) == 2 and pair[0].isdigit() for pair in answers]):
            answers = input("Format error! One or more answers are not pairs, the delimiter is wrong or pair order is reversed. Please enter the answer again.\n")
            answers = [i.split(" ") for i in answer.split(", ")]
        return {int(k): v for k, v in answers}

    def connect_check(self, correct: list, answer: str) -> None:
        """
        Check whether provided answer is correct.

        Checks the connect exercise.

        When a pair is missing, return feedback for the correct answer
        When a pair is incorrect check for typos and return feedback for the correct answer

        modifies:
        self.test_missed_answers - modifies the amount of missed items in a test, used in test function
        """
        answers = self.connect_answer_check(answer)
        incorrect_amount = 0
        for index in range(len(correct)):
            if index + 1 not in answers:
                print(f"{index + 1} was not answered. {index + 1} is {correct[index].term}")
                self.test_missed_answers += 1
                incorrect_amount += 1
                input("Press {enter} to continue...\n")
            elif correct[index] != answers[index + 1]:
                print(f"Incorrect! {index + 1} is {correct[index].term}, not {answers[index + 1]}")
                if self.match_ratio(answers[index + 1].lower(), correct[index].lower()):
                    if input("There seems to be a typo, overwrite? ").lower() in ["y", "yes", "true", "1", "t"]:
                        print("Overwriting...")
                    else:
                        self.test_missed_answers += 1
                        incorrect_amount += 1
                else:
                    self.test_missed_answers += 1
                    incorrect_amount += 1
                input("Press {enter} to continue...\n")
        if incorrect_amount == 0:
            print("All are Correct!")
        else:
            print(f"{incorrect_amount} out of {len(correct)} were incorrect.")
        input("Press {enter} to continue...\n")

    def true_false(self) -> None:
        """
        True or False exercise.

        Chooses whether to give a True or False question and prints the question.

        inputs:
        answer - answer to the question, has to be one of:
                 ["true", "t", "yes", "y"] is True and
                 ["false", "f", "no", "n"] is False
        """
        if randint(0,1):
            correct = self.get_random(1)
            print(choice(correct.hints))
            print(correct.term)
            answer = input("True or False? ").lower()
            while answer not in ["true", "t", "yes", "y", "false", "f", "no", "n"]:
                answer = input("Please enter true or false! ")
            self.true_false_check(True, answer)
        else:
            term, definition = self.get_random(2)
            print(choice(definition.hints))
            print(term.term)
            answer = input("True or False? ").lower()
            while answer not in ["true", "t", "yes", "y", "false", "f", "no", "n", ""]:
                answer = input("Please enter true or false! ")
            self.true_false_check(False, answer)

    def true_false_check(self, correct: bool, answer: str) -> None:
        """
        Check whether provided answer is correct.

        Checks the true or false exercise.

        correct:
        True and answer is one of ["true", "t", "y", "yes"]
        False and answer is one of ["false", "f", "no", "n"]

        incorrect otherwise.
        """
        if answer in ["true", "t", "y", "yes"] and correct or answer in ["false", "f", "no", "n"] and not correct:
            print("Correct!")
            input("Press {enter} to continue...\n")
        else:
            print(f"Incorrect! It was {str(correct)}")
            self.test_missed_answers += 1
            input("Press {enter} to continue...\n")

    def test(self, configuration: list = [("true_false", 4), ("multiple_choice", 4), ("connect", 8), ("write", 4)]) -> None:
        """
        A test module.

        Creates a test based on the configuration.

        configuration:
        a list of tuples with (exercise_type, number_of_questions) pairs.
        exercises are printed in the order of the list.
        if an exercise is not found, the pair is skipped.

        default configuration:
        [
            ("true_false", 4),
            ("multiple_choice", 4),
            ("connect", 8),
            ("write", 4)
        ]

        gives feedback based on how many questions were answered incorrectly.
        """
        self.test_missed_answers = 0

        for exercise, number in configuration:
            if exercise == "true_false":
                print("True OR False?\n")
                print("-" * 20)
                for question_number in range(number):
                    print(f"##### {question_number + 1}. #####")
                    self.true_false()

            elif exercise == "multiple_choice":
                print("\n\nMultiple Choice\n")
                print("-" * 20)
                for question_number in range(number):
                    print(f"##### {question_number + 1}. #####")
                    self.multiple_choice(4)

            elif exercise == "write":
                print("\n\nCorrect Answer\n")
                print("-" * 20)
                for question_number in range(number):
                    print(f"##### {question_number + 1}. #####")
                    self.write_answer()

            elif exercise == "connect":
                print("\n\nConnect\n")
                print("-" * 20)
                self.connect(number)

        print(f"Well Done! You missed {self.test_missed_answers} out of {sum(map(lambda x: x[1], configuration))} questions.")

    def flashcards(self) -> None:
        """Print terms and definitions."""
        nr = 0
        term = self.set[nr]
        flipped = True

        print(f"Term #{nr + 1}")
        print(term.term)
        while True:
            inp = input("Next(K), Last(L), Flip(F), Exit(E)? ").lower()
            if inp not in ["k", "l", "f", "e"]:
                continue
            if inp == "e":
                print("\nExiting...")
                break
            if inp == "f":
                print(term.definition if flipped else term.term)
                flipped = not flipped
                continue
            if inp == "k":
                if nr == len(self.set) - 1:
                    over = input("This is the last term. Start over(Y)? ").lower()
                    nr = -1 if over == "y" else len(self.set) - 2
                nr += 1
            elif inp == "l":
                if nr == 0:
                    print("This is the first term...")
                    nr = 1
                nr -= 1
            term = self.set[nr]
            print(f"\nTerm #{nr + 1}")
            print(term.term)
            


def set_from_file(file_name: str, set_name: str = "default", card_delimiter: str = "\n", definition_delimiter: str = " - ", hint_delimiter: str = ". ") -> LearnSet:
    """
    Create a LearnSet object from a file.

    variables:
    file_name - name of the file
    set_name - name of the set
    card_delimiter - delimiter of cards, default newline (\n)
    definition_delimiter - delimiter of term and definition, default tab (\t)
    hint_delimiter - delimiter of hints in definition, default period (. )

    returns
    LearnSet object
    """

    with open(f"{file_name}", "r", encoding="UTF-8") as file:
        set = LearnSet(set_name, [], {})
        for card in file.read().split(card_delimiter):
            if card.startswith("\\\\"):
                continue
            split = card.split(definition_delimiter)
            if len(split) == 2:
                term, definition = split
                set.add(LearnObject(term, definition, hint_delimiter))
            elif len(split) == 3:
                term, year, definition = split
                set.add(LearnObject(term, definition, hint_delimiter, year))
            else:
                print(f"No data found: {card}")
        set.set_info()
        return set


def save_set_to_file(file_name: str, set: LearnSet, card_delimiter: str = "\n", definition_delimiter: str = " - ") -> None:
    """
    Save a LearnSet object to a file

    variables:
    file_name - name of the save file
    set - LearnSet object, which will be saved
    card_delimiter - delimiter of cards, default newline (\n)
    definition_delimiter - delimiter of term and definition, default tab (\t)
    """
    with open(f"{file_name}", "w", encoding="UTF-8") as file:
        content = card_delimiter.join([definition_delimiter.join([card.term, card.definition]) for card in set.set])
        file.write(content)



if __name__ == "__main__":
    example = set_from_file(
        file_name="example.txt",
        set_name="default",
        card_delimiter="\n",
        definition_delimiter=" - ",
        hint_delimiter=". "
    )

    # learn
    example.learn(round_length=7)

    #test
    # example.test()

    # flashcards
    # example.flashcards()

    # create new set
    example = LearnSet(name="example")

    # add terms
    example.add(
        LearnObject(
            term="term1", 
            definition="Definition - hint1. hint2.", 
            year="year1",           # optional
            hint_delimiter=". "     # default value, optional
        )
    )

    # optional: save set, to load later
    # save_set_to_file(
    #     file_name="example_set",
    #     set=example
    #     # optionally add custom delimiters
    # )