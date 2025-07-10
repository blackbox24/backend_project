from random import randint

# display welcome and rules
print("""
Welcome to the Number Guessing Game!
I'm thinking of a number between 1 and 100.
You have 5 chances to guess the correct number.

"""
)

guessed_number = randint(1,100)
chances = 0
tries = 0
# display rules and prompts
print("""
Please select the difficulty level:
1. Easy (10 chances)
2. Medium (5 chances)
3. Hard (3 chances)
""")

game_level = str(input("Enter your choice: "))

if game_level == "3":
    chances = 10
elif game_level == "2":
    chances = 5
else:
    chances = 3

"""
Great! You have selected the Medium difficulty level.
Let's start the game!
"""

# make sure it is int /  validate input

# Player tries per number of counts ontill wins and runs out of chances
while tries <= chances:
    if tries == chances:
        print("You have run out of chances")
        break
    elif tries == 0:
        player_guess = int(input("Enter your guess: "))
    else:
        if guessed_number == player_guess:
            print(f"Congratulations! You guessed the correct number in {tries} attempts.")
            break
        elif guessed_number > player_guess:
            print(f"Incorrect! The number is greater than {player_guess} ")
            player_guess = int(input("Enter your guess again: "))

        elif guessed_number < player_guess:
            print(f"Incorrect! The number is lesser than {player_guess} ")
            player_guess = int(input("Please, Enter your guess: "))

    tries += 1
    print("Tries: ",str(tries))