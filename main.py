from tkinter import Tk, Listbox, PhotoImage, Button, Frame, Menu
from pygame import mixer

#Окно
window = Tk()
window.title("Music Player")
window.iconbitmap("./gui/logo.ico")
window.geometry("300x500")

#Музыка
mixer.init()

#Список музыки
songs_list = Listbox(master = window, width=60)
songs_list.pack(pady=20)

#Рамка для кнопок
btn_frame = Frame(window)
btn_frame.pack()

#Картинки кнопок
previous_img = PhotoImage(file = "gui/previous.png")
play_img = PhotoImage(file = "gui/play.png")
next_img = PhotoImage(file = "gui/next.png")
pause_img = PhotoImage(file = "gui/pause.png")

#Кнопки
previous_btn = Button(master = btn_frame, image = previous_img, borderwidth = 0)
play_btn = Button(master = btn_frame, image = play_img, borderwidth = 0)
next_btn = Button(master = btn_frame, image = next_img, borderwidth = 0)
pause_btn = Button(master = btn_frame, image = pause_img, borderwidth = 0)

#Установка кнопок
previous_btn.grid(row = 0, column = 0)
play_btn.grid(row = 0, column = 1)
next_btn.grid(row = 0, column = 2)
pause_btn.grid(row = 0, column = 3)

#Меню
menu = Menu(window)
window.config(menu = menu)

#Добавляем в меню возможность добавить музыкальные файлы
add_song = Menu(menu)
add_song.add_cascade(Label = "Add Song", menu = add_song)




if __name__ == "__main__":
    window.mainloop()