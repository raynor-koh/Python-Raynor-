from tkinter import *
import math
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
TICK = '✅'
reps = 0
time = None
# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    window.after_cancel(time)
    # timer_text 00:00
    canvas.itemconfig(timer_text, text='00:00', fill='white', font=(FONT_NAME, 25, 'bold'))
    # title_label "Timer"
    timer.config(text='Timer', fg=GREEN, bg=YELLOW, font=(FONT_NAME, 40, 'bold'))

    # Reset ticks
    global reps
    reps = 0
    tick_count.config(text='', fg=GREEN, bg=YELLOW, font=(FONT_NAME, 15, 'bold'))
# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps
    #work_sec = WORK_MIN * 60
    #short_break_sec = SHORT_BREAK_MIN * 60
    #long_break_sec = LONG_BREAK_MIN * 60

    work_sec = 25
    short_break_sec = 5
    long_break_sec = 20

    reps += 1
    # If it's the 1st/3rd/5th/7th rep
    if reps % 2 == 1:
        count_down(work_sec)
        timer.config(text='WORK', fg=RED, bg=YELLOW, font=(FONT_NAME, 40, 'bold'))

    # If it's 2nd/4th/6th rep
    elif reps % 2 == 0 and reps % 8 != 0:
        timer.config(text='BREAK', fg=GREEN, bg=YELLOW, font=(FONT_NAME, 40, 'bold'))
        count_down(short_break_sec)

    # If it's the 8th rep
    elif reps % 8 == 0:
        timer.config(text='BREAK', fg=PINK, bg=YELLOW, font=(FONT_NAME, 40, 'bold'))
        count_down(long_break_sec)
        reps = 0


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):

    count_min = math.floor(count / 60)
    count_sec = count % 60

    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global time
        time = window.after(1000, count_down, count -1)
    else:
        start_timer()
        num_ticks = math.floor(reps/2)
        session = ''
        print(reps)
        for _ in range(int(num_ticks)):
            session += TICK
        tick_count.config(text=session, fg=GREEN, bg=YELLOW, font=(FONT_NAME, 15, 'bold'))


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)


# Canvas Widget
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill='white', font=(FONT_NAME, 25, 'bold'))
canvas.grid(column=2, row=1)

timer = Label(text='Timer', fg=GREEN, bg=YELLOW, font=(FONT_NAME, 40, 'bold'))
timer.grid(column=2, row=0)

start_button = Button(text='Start', font=(FONT_NAME, 10, 'bold'), highlightthickness=0, command=start_timer)
start_button.grid(column=1, row=2)

reset_button = Button(text='Reset', font=(FONT_NAME, 10, 'bold'), highlightthickness=0, command=reset_timer)
reset_button.grid(column=3, row=2)

tick_count = Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 15, 'bold'))
tick_count.grid(column=2, row=3)


window.mainloop()
