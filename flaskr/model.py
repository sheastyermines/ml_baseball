from flaskr.saved_models import *

def run_model(team, year, model="sameYear"):
    # model will be either (0, 1, 3, 5)
    # team will be a string of the acronym (if you find an error, the mappings are located in flaskr/config)
    # year is an int of the year in question
    # return -1 for wins will result in an error message being displayed to the user.

    # Example to read from a file in the saved_models folder
    f=open("flaskr/saved_models/example.txt", "r")
    print(f.read())

    
    wins = 42
    actual_wins = 24
    return (wins, actual_wins)
