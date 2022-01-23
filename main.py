import random

WORD_SIZE = 9
MAX_TURNS = 6


class WordleSolver:
    data: list

    turn: int = 1

    correct_with_position: dict = {}
    correct_without_position: str = ""
    incorrect: str = ""

    def __init__(self, lang: str) -> None:
        d = [x.replace("\n", "") for x in open(f"db/{lang}.dat", "r")]
        self.data = [x for x in d if len(x) == WORD_SIZE]

    def get_next_input(self):
        if self.turn == 1:
            print(
                f"There are {len(self.data)} words. introduce this randomly selected one:"
            )
            self.curr_choice = random.choice(self.data)

        else:
            maybe_are = self.get_final_answers()
            if len(maybe_are) == 1:
                print(f'Answer found! introduce "{maybe_are[0]}" to win')
                exit()
            print(f"\nThere are {len(maybe_are)} potential answers")
            if len(maybe_are) > MAX_TURNS - self.turn:
                choose_another = self.get_missing_letters()
                if len(choose_another) > 0:
                    maybe_are = choose_another
                else:
                    print(
                        """
since there are more potential answers than turns remaining,
introduce a random word containing none of the already guessed letters"""
                    )
            self.curr_choice = random.choice(maybe_are)
            print("introduce this randomly selected word from the list")

        self.turn += 1

        print(f"\t{self.curr_choice}")
        return self.curr_choice

    def get_final_answers(self):
        maybe_are = []
        for d in self.data:
            maybe = True
            for k, v in self.correct_with_position.items():
                if not d[k] == v:
                    maybe = False
            for c in self.correct_without_position:
                if not c in d:
                    maybe = False
            for c in self.incorrect:
                if c in d:
                    maybe = False

            if maybe:
                maybe_are.append(d)

        return maybe_are

    def get_missing_letters(self):

        maybe_are = []
        for d in self.data:
            maybe = True
            for c in self.correct_without_position:
                if c in d:
                    maybe = False

            for c in self.incorrect:
                if c in d:
                    maybe = False

            for c in self.correct_with_position.values():
                if c in d:
                    maybe = False

            if maybe:
                maybe_are.append(d)

        return maybe_are

    def handle_input(self, pattern: str):
        """
        Parses user input resulting from entering the current selected word
        Format:
            - n for gray (no match)
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
                if letter not in self.correct_without_position:
                    self.correct_without_position += letter

        for i in range(WORD_SIZE):
            state = pattern[i]
            letter = self.curr_choice[i]
            if state == "n":
                if letter not in self.incorrect:
                    if (
                        letter not in self.correct_with_position.values()
                        and letter not in self.correct_without_position
                    ):
                        self.incorrect += letter


if __name__ == "__main__":
    import os
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-W", default=5, required=False, type=int)
    args = parser.parse_args()

    WORD_SIZE = args.W or 5

    accepted_lang = [l.replace(".dat", "") for l in os.listdir("db")]
    lang = input(f"Introduce language {accepted_lang = }: ").lower()

    assert lang in accepted_lang, f"Only {', '.join(accepted_lang)} es supported"
    game = WordleSolver(lang)

    while True:
        game.get_next_input()
        while True:
            try:
                pattern = input("Introduce pattern: ")

                assert type(pattern) == str, "Patter must be a string"
                assert (
                    len(pattern) == WORD_SIZE
                ), f"Pattern should be {WORD_SIZE} characters long"
                assert set(pattern) <= set(
                    "nyg"
                ), "Patten must be composed of n, y and g"
                break
            except AssertionError as e:
                print(e)
                continue

        game.handle_input(pattern)