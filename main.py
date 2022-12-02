from tkinter import *
import pandas
import random
import os
BACKGROUND_COLOR = "#B1DDC6"
ORIGINAL_WORD_FONT = ("Ariel", 40, "italic")
TRANSLATED_WORD_FONT = ("Ariel", 60, "bold")
count = 100

data = pandas.read_csv("./data/french_words.csv")
# making sure that it checked the words to learn first.
if os.path.exists("data/words_to_learn.csv"):
    data = pandas.read_csv("data/words_to_learn.csv")
    learn = data.to_dict(orient="records")
else:
    learn = data.to_dict(orient="records")

french_english = {}


# -----------------------------# CHOOSING A RANDOM FRENCH WORD #-----------------------#


def next_card():
    """This function helps flip the cards to the next one"""
    global french_english, flip_timer
    window.after_cancel(flip_timer)
    # the orient="records" is a parameter that organizes our list of dictionary in a specific way
    # Reference: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_dict.html
    french_english = random.choice(learn)
    # using dictionary unpacking
    french_tuple, english_tuple = french_english.items()
    french, french_word = french_tuple
    canvas.itemconfig(card_image, image=card_front_img)
    canvas.itemconfig(card_word, text=french_word, fill="black")
    canvas.itemconfig(card_title, text=french, fill="black")
    flip_timer = window.after(3000, flip_card)


# ---------------------------------- SAVING DATA ---------------------------------------------#


def save_data():
    """This function takes out any word already mastered and save the one left in word_to_learn.csv"""
    global learn
    learn.remove(french_english)
    data_learned = pandas.DataFrame(learn)
    data_learned.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# ----------------------------------- FLIPPING THE CARD ---------------------------------------#


def flip_card():
    global french_english
    canvas.itemconfig(card_image, image=card_back_img)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=french_english["English"], fill="white")


# ----------------------------------------------------------------------------------------------#


window = Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, pady=50, padx=50)
flip_timer = window.after(3000, flip_card)
# Inserting pictures ---> canvas
card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")
canvas = Canvas(width=800, height=562, bg=BACKGROUND_COLOR, highlightthickness=0)
card_image = canvas.create_image(400, 270, image=card_front_img)
# creating text within the canvas
card_title = canvas.create_text(400, 150, text="", font=ORIGINAL_WORD_FONT)
card_word = canvas.create_text(400, 280, text="", font=TRANSLATED_WORD_FONT)
canvas.grid(row=0, column=0, columnspan=2)


# Buttons
right_button_img = PhotoImage(file="./images/right.png")
right_button = Button(image=right_button_img, bg=BACKGROUND_COLOR, highlightthickness=0, command=save_data)
right_button.grid(row=1, column=1)
wrong_button_img = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_button_img, bg=BACKGROUND_COLOR, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)

# To display the title and word immediately at application start.
next_card()


window.mainloop()
