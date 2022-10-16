import random
from tkinter import *


words = ["apple", "banana", "kiwi", "orange", "pear", "laptop", "tablet", "phone", "bulldog", "book", "pen", "bag",
         "novel", "with", "table", "leg", "arm", "brown", "yellow", "blue", "cat", "car", "lion", "tiger", "picture"]
words_entered = []
random_words = []
timer = 60


def get_random_words():
    global words, random_words
    for i in range(0, 10):
        word = words[random.randint(0, len(words) - 1)]
        random_words.append(word)


def start():
    global words, random_words
    get_random_words()
    canvas.itemconfig(words_to_type, text=random_words)
    type_entry.focus_set()
    counter_label()


def counter_label():

    def count():
        global timer
        timer -= 1
        label.config(text=str(timer))
        label.after(1000, count)
        if timer == 0:
            global words_entered, words
            label.config(text="Done")
            label.destroy()
            type_entry.destroy()
            correct_words = [word for word in words_entered if word in words]
            if (len(words_entered) - len(correct_words)) > 0:
                incorrect_words = len(words_entered) - len(correct_words)
                new_label = Label(window, text=f"You have entered {len(words_entered)} words, but {incorrect_words} of "
                                               f"them was incorrect. Your score is {len(correct_words)} WPM.")
                new_label.grid(row=4, column=0, columnspan=3)
                evaluate_high_score(len(correct_words))
            else:
                new_label = Label(window, text=f"You have entered {len(correct_words)} WPM.")
                new_label.grid(row=4, column=0, columnspan=3)
                evaluate_high_score(len(correct_words))
    count()


def high_score():
    with open("data.txt") as data:
        hi_score = int(float(data.read()))
        return hi_score


def word_entered(entry):
    global words_entered
    entry = type_entry.get()
    words_entered.append(entry.strip())
    if len(words_entered) % 10 == 0:
        more_words()
    type_entry.delete(0, END)
    type_entry.focus_set()


def evaluate_high_score(correct_score):
    with open("data.txt") as data:
        score = int(float(data.read()))
    if correct_score > score:
        with open("data.txt", mode="w") as data:
            data.write(f"{correct_score}")
            score_label = Label(window, text=f"Highest Score: {correct_score} WPM", font=8)
            score_label.grid(row=0, column=2)


def more_words():
    random_words.clear()
    get_random_words()
    canvas.itemconfig(words_to_type, text=random_words)


# TODO 4
# expand words base


window = Tk()
window.geometry("500x500")
window.config(padx=50, pady=30)
window.title("Typing Speed Test App")

canvas = Canvas(window, width=400, height=250, bg="lightgray")
words_to_type = canvas.create_text(200, 125, width=300, text="Welcome to Miralem's Typing Speed Test.\n"
                                                             "Press Start to Begin", font=("Arial", 15),
                                   justify="center")
canvas.grid(row=1, column=0, columnspan=3)

btn_start = Button(window, text=" Start ", command=start, font=10)
btn_start.grid(row=3, column=1)


score_label = Label(window, text=f"Highest Score: {high_score()} WPM", font=8)
score_label.grid(row=0, column=2)

label = Label(window, width=10, height=2, text=60, fg="white", bg="blue", font=16)
label.grid(row=0, column=0)

type_entry = Entry(window, width=30, justify="center", font=("Arial", 16))
type_entry.bind("<space>", word_entered)
type_entry.grid(row=2, column=0, columnspan=3)

window.mainloop()
