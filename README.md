# Wordle Breaker
## A CLI tool to help you solve Wordle

I decided to code a solution to help uncover Wordle's hidden word.

# How to use
### 0. Previous requirements
To run this tool , you will need python with a version at least 3.6
### 1. Clone the repo
```
git clone https://github.com/a96lex/wordle-breaker.git
```

### 2. Run the script
```
cd wordle-breaker
python wordle-breaker
```

Follow instructions to win!

# Decision heuristics

At first, a random word is selected.
Then, a random word containing none of the known letters is selected, until a solution is found.
I have yet to see the script fail to find a word.