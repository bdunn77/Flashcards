import random
from tkinter import *
import pandas

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
learned = []

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    print(original_data)
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

try:
    learned_data = pandas.read_csv("data/words_learned.csv")
    learned = learned_data.to_dict(orient="records")
except FileNotFoundError:
    learned = []


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill=BACKGROUND_COLOR)
    canvas.itemconfig(card_word, text=current_card["French"], fill=BACKGROUND_COLOR)
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


def is_known():
    # add to learned
    learned.append(current_card)
    learned_data = pandas.DataFrame(learned)
    learned_data.to_csv("data/words_learned.csv", index=False)
    print(len(learned))
    canvas.itemconfig(learned_amount, text=f"{len(learned)}\n words learned")
    # remove from study list
    to_learn.remove(current_card)
    print(len(to_learn))
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    canvas.itemconfig(to_learn_amount, text=f"{len(to_learn)}\n words to learn")
    next_card()


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

# canvas
canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 50, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 80, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

# words learned amount
learned_amount = canvas.create_text(100, 450, text=f"{len(learned)}\n words learned", font=("Ariel", 20, "italic"))

# words to learn amount
to_learn_amount = canvas.create_text(700, 450, text=f"{len(to_learn)}\n words to learn", font=("Ariel", 20, "italic"))
# buttons
cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)
check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)


def show_learned():
    learned_data = pandas.DataFrame(learned)
    learned_data.index = learned_data.index + 1
    top = Toplevel()  # Create a new top-level window
    text = Text(top)
    text.insert("1.0", learned_data.to_string(index=True))
    text.pack()


# button to show words learned
learned_button = Button(text="Show learned words", bg=BACKGROUND_COLOR, command=show_learned)
learned_button.grid(row=2, column=0, columnspan=2)

next_card()

window.mainloop()
