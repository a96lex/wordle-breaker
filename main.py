import random

WORD_SIZE = 9
MAX_TURNS = 6


class WordleSolver:
    data: list
    possible_answers: list

    turn: int = 1

    correct_with_position: dict = {}  # green
    present_but_incorrect_position: str = ""  # yellow
    present_but_incorrect_position_dict: dict = {}  # yellow
    not_present: str = ""  # gray

    def __init__(self, lang: str) -> None:
        d = [x.replace("\n", "") for x in open(f"languages/{lang}.dat", "r")]
        self.all_words_list = [x for x in d if len(x) == WORD_SIZE and "-" not in d]
        self.possible_answers = self.all_words_list

    def get_next_input(self):
        if self.turn == 1:
            print(
                f"There are {len(self.all_words_list)} words. introduce this randomly selected one:"
            )
            self.curr_choice = random.choice(self.all_words_list)

        else:
            potential_next_answers = self.get_possible_final_answer()
            self.possible_answers = potential_next_answers
            if len(potential_next_answers) == 1:
                print(f'Answer found! introduce "{potential_next_answers[0]}" to win')
                exit()
            print(f"\nThere are {len(potential_next_answers)} potential answers")
            if len(potential_next_answers) > MAX_TURNS - self.turn:
                choose_another = self.get_missing_letters()
                if len(choose_another) > 0:
                    potential_next_answers = choose_another
                    print(
                        """
since there are more potential answers than turns remaining,
introduce a random word containing none of the already guessed letters
(or enter "p" to see all possible answers)"""
                    )
            self.curr_choice = random.choice(potential_next_answers)
            print("Introduce this randomly selected word from the list")

        self.turn += 1

        print(f"\t{self.curr_choice}")
        return self.curr_choice

    def get_possible_final_answer(self):
        potential_next_answers = []
        for word in self.all_words_list:
            is_possible_answer = True
            for pos, letter in self.correct_with_position.items():
                if not word[pos] == letter:
                    is_possible_answer = False

            for (
                pos,
                incorrect_pos_letters,
            ) in self.present_but_incorrect_position_dict.items():
                for letter in incorrect_pos_letters:
                    if word[pos] == letter:
                        is_possible_answer = False

            for letter in self.present_but_incorrect_position:
                if not letter in word:
                    is_possible_answer = False

            for letter in self.not_present:
                if letter in word:
                    is_possible_answer = False

            if is_possible_answer:
                potential_next_answers.append(word)

        return potential_next_answers

    def get_missing_letters(self):

        words_with_unseen_letters = []
        for word in self.all_words_list:
            contains_seen_letters = False
            for letter in [
                *self.present_but_incorrect_position,
                *self.not_present,
                *self.correct_with_position.values(),
            ]:
                if letter in word:
                    contains_seen_letters = True

            if not contains_seen_letters:
                words_with_unseen_letters.append(word)

        return words_with_unseen_letters

    def handle_input(self, pattern: str):
        """
        Parses user input resulting from entering the current selected word
        Format:
            - - for gray (no match)
            - y for yellow (match, incorrect order)
            - g for green (match, correct order)

        Must be passed as a single string eg: "ygnng"
        """
        for i in range(WORD_SIZE):
            state = pattern[i]
            letter = self.curr_choice[i]
            if state == "g":
                self.correct_with_position[i] = letter

        for i in range(WORD_SIZE):
            state = pattern[i]
            letter = self.curr_choice[i]
            if state == "y":
                if letter not in self.present_but_incorrect_position:
                    self.present_but_incorrect_position += letter
                if not self.present_but_incorrect_position_dict.get(i):
                    self.present_but_incorrect_position_dict[i] = ""
                if letter not in self.present_but_incorrect_position_dict[i]:
                    self.present_but_incorrect_position_dict[i] += letter

        for i in range(WORD_SIZE):
            state = pattern[i]
            letter = self.curr_choice[i]
            if state == "-":
                if letter not in self.not_present:
                    if (
                        letter not in self.correct_with_position.values()
                        and letter not in self.present_but_incorrect_position
                    ):
                        self.not_present += letter


if __name__ == "__main__":
    import os
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-W", default=5, required=False, type=int)
    parser.add_argument("--words", default=5, required=False, type=int)
    args = parser.parse_args()

    print(
        """
WORDLE BREAKER

instructions: 
1. Select language
2. Introduce the shown word on wordle
3. Write on the 
terminal the results using the following format:
    - for gray (no match)
    y for yellow (match, incorrect order)
    g for green (match, correct order)

For example, 🟨🟩⬜⬜🟩 -> "yg--g"
"""
    )

    WORD_SIZE = args.W or args.words or 5

    accepted_lang = [l.replace(".dat", "") for l in os.listdir("languages")]
    lang = input(f"Introduce language ({', '.join(accepted_lang)}): ").lower()

    assert lang in accepted_lang, f"Only {', '.join(accepted_lang)} es supported"
    game = WordleSolver(lang)

    while True:
        game.get_next_input()
        while True:
            try:
                pattern = input(
                    """
Introduce pattern or:
    - introduce p to see all possible answers
    - introduce c to choose your own word): 

Your input:
    """
                )
                if pattern == "p":
                    print(game.possible_answers)
                    print(f"\nRecommended next guess:\t{game.curr_choice}")
                    continue

                if pattern == "c":
                    while True:
                        try:
                            word = input("Introduce the chosen word: ")
                            assert type(word) == str, "Word must be a string"
                            assert (
                                len(word) == WORD_SIZE
                            ), f"word should be {WORD_SIZE} characters long"
                            game.curr_choice = word
                            break
                        except AssertionError as e:
                            print(e)
                            continue

                assert type(pattern) == str, "Pattern must be a string"
                assert (
                    len(pattern) == WORD_SIZE
                ), f"Pattern should be {WORD_SIZE} characters long"
                assert set(pattern) <= set(
                    "-yg"
                ), "Patten must be composed of -, y and g"
                break
            except AssertionError as e:
                print(e)
                continue

        game.handle_input(pattern)
