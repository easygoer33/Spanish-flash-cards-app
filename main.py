from tkinter import *
from tkinter import messagebox
import random
import pandas

BACKGROUND_COLOR = "#B1DDC6"
TITLE_FONT = ("Arial", 40, "italic")
WORD_FONT = ("Arial", 60, "bold")

try:
    flash_card_df = pandas.read_csv("data/Spanish_words_to_learn.csv", encoding="utf-8")
except (FileNotFoundError, pandas.errors.EmptyDataError):
    flash_card_df = pandas.read_csv("data/Spanish_5000-words-google translate_unicode.csv", encoding="ISO-8859-1")

random_row_index = None

# --------------------------------------- Random word -------------------------------------------#


def random_word():
    global random_row_index, flip_timer
    window.after_cancel(flip_timer)
    random_row_index = random.randint(0, len(flash_card_df) - 1)
    random_spanish_word = flash_card_df.iloc[random_row_index, 0]
    canvas.itemconfig(title_text, text="Spanish", fill="black")
    canvas.itemconfig(word_text, text=random_spanish_word, fill="black")
    canvas.itemconfig(canvas_image, image=card_front_img)
    flip_timer = window.after(3000, update)


def right_button():
    i = flash_card_df[flash_card_df.Spanish == flash_card_df.iloc[random_row_index, 0]].index
    flash_card_df.drop(i, inplace=True)
    random_word()
# ----------------------------------------- Timer ----------------------------------------------- #


def save_files():
    if messagebox.askyesno("Save Progress", "Do you want to save your progress?"):
        flash_card_df.to_csv("data/Spanish_words_to_learn.csv", encoding='utf-8', index=False)
        window.destroy()
    else:
        window.destroy()

# ----------------------------------------- Save on Window Close -------------------------------- #

def update():
    english_translit_word = flash_card_df.iloc[random_row_index, 1]
    canvas.itemconfig(canvas_image, image=card_back_img)
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=english_translit_word, fill="white")


# -----------------------------------------------UI --------------------------------------------- #

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, update)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(411, 265, image=card_front_img)
canvas.grid(row=0, column=0, columnspan=2)

title_text = canvas.create_text(400, 150, text="", font=TITLE_FONT)
word_text = canvas.create_text(400, 280, text="", font=WORD_FONT)

wrong_button_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_button_image, highlightthickness=0, command=random_word)
wrong_button.grid(column=0, row=1)

right_button_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_button_image, highlightthickness=0, command=right_button)
right_button.grid(column=1, row=1)

random_word()

# set callback for window close
window.protocol("WM_DELETE_WINDOW", save_files)

window.mainloop()
