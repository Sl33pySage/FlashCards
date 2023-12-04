from tkinter import *
import pandas
import random


BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}


try:
    data = pandas.read_csv("data/Words_to_learn.csv")
except FileNotFoundError:
    japanese = pandas.read_csv("data/Japanese_words.csv").drop(
        ["First"], axis=1)
    to_learn = japanese.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def learned():
    to_learn.remove(current_card)
    data1 = pandas.DataFrame(to_learn)
    data1.to_csv("data/Words_to_learn.csv", index=False)
    new_word()


def new_word():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_img, image=card_front)
    canvas.itemconfig(title, text="Japanese", fill="black")
    canvas.itemconfig(word, text=current_card["Japanese"], fill="black")
    flip_timer = window.after(3000, func=flip)


def flip():
    canvas.itemconfig(card_img, image=card_back)
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word, text=current_card["English"], fill="white")


# TK WINDOW
window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip)
# CANVAS
canvas = Canvas(width=800, height=526, background=BACKGROUND_COLOR,
                highlightthickness=0)

card_back = PhotoImage(file="images/card_back.png")
card_front = PhotoImage(file="images/card_front.png")
card_img = canvas.create_image(400, 263, image=card_front)
canvas.grid(column=0, columnspan=2, row=0)
title = canvas.create_text(400, 150, font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 263, font=("Ariel", 60, "bold"))


right = PhotoImage(file="images/right.png")
right_button = Button(image=right, highlightthickness=0, command=learned)
right_button.grid(column=1, row=1)

wrong = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong, highlightthickness=0, command=new_word)
wrong_button.grid(column=0, row=1)

new_word()

window.mainloop()
