from tkinter import Tk, Listbox, PhotoImage, Button, Frame, Menu, Label, Scale, Toplevel
from player import Player
import platform

def about():
    about_win = Toplevel(window)
    about_win.geometry("220x120")
    about_win.config(bg = "#262626")
    about_win.resizable(False, False)
    about_frame = Frame(about_win, bg = "#262626")
    version = Label(master = about_frame, text = "Version: 1.0.0", fg = "white", bg = "#262626")
    created = Label(master = about_frame, text = "Created by NVORON", fg = "white", bg = "#262626")

    about_frame.pack(fill = "x", pady = 5, padx = 10)
    version.pack()
    created.pack()


#Окно
window = Tk()
window.title("Music Player")
if platform.system() == 'Windows':
    window.geometry("300x450")
else:
    window.geometry("300x400")
window.config(bg = "#262626")
window.resizable(False, False)
window.iconphoto(True, PhotoImage(file = './gui/logo.png'))
songs_list = Listbox(master = window, fg = "white", bg = "black", borderwidth = 5, justify = "left", width = 29, font = ('poppins', 14))


time_frame = Frame(window, bg = "#262626")
start_time = Label(master = time_frame, text = '', fg = "white", anchor = "w", bg = "#262626", padx = 10)
end_time = Label(master = time_frame, text = '', fg = "white", anchor = "e", bg = "#262626", padx = 10)
music_slider = Scale(master = window, from_ = 0, to = 100, orient = "horizontal", bg = "#262626", relief = "flat", length = 270, showvalue = False)

volume_frame = Frame(window, bg = "#262626")
volume_but = Button(master = volume_frame, borderwidth = 0, relief = "flat", bg = "#262626")
volume_slider  = Scale(master = volume_frame, from_ = 0, to = 100, relief = "flat", orient = "horizontal", bg = "#262626", length = 240, showvalue = False, label = "")
volume_label = Label(master = window, text = '100%', fg = "white", relief = "flat", anchor = "center", bg = "#262626")

player = Player(songs_list, start_time, end_time, music_slider, volume_label, volume_slider, volume_but)

#Картинки кнопок
previous_img = PhotoImage(file = "./gui/previous.png")
play_img = PhotoImage(file = "./gui/play.png")
pause_img = PhotoImage(file = "./gui/pause.png")
next_img = PhotoImage(file = "./gui/next.png")
add_img = PhotoImage(file = "./gui/add.png")
remove_img = PhotoImage(file = "./gui/remove.png")

#Кнопки
btn_frame = Frame(window, bg = "#262626")
previous_btn = Button(master = btn_frame, image = previous_img, borderwidth = 0, relief = "flat", bg = "#262626", command = player.previous_song)
play_btn = Button(master = btn_frame, image = play_img, borderwidth = 0, relief = "flat", bg = "#262626", command = player.play_song)
pause_btn = Button(master = btn_frame, image = pause_img, borderwidth = 0, relief = "flat", bg = "#262626", command = player.pause_song)
next_btn = Button(master = btn_frame, image = next_img, borderwidth = 0, relief = "flat", bg = "#262626", command = player.next_song)

edit_list_frame = Frame(window, bg = "#262626")
remove_btn = Button(master = edit_list_frame, image = remove_img, borderwidth = 0, relief = "flat", bg = "#262626", command = player.remove)
add_btn = Button(master = edit_list_frame, image = add_img, borderwidth = 0, relief = "flat", bg = "#262626", command = player.add_file_to_playlist)

songs_list.pack()

edit_list_frame.pack(fill = "x", pady = 5, padx=20)
remove_btn.pack(side="left", padx=20)
add_btn.pack(side="right", padx=20)

time_frame.pack(fill = "x", pady = 5, padx = 10)
start_time.pack(side="left")
end_time.pack(side="right")

music_slider.pack()

btn_frame.pack(fill = "x", pady = 10)
previous_btn.grid(row=0, column=0, padx = (12,10))
play_btn.grid(row=0, column=1, padx = 10)
pause_btn.grid(row=0, column=2, padx = 10)
next_btn.grid(row=0, column=3, padx=(10,12))

volume_frame.pack(fill = "x", pady = (5, 0))
volume_but.pack(padx = (12, 10), side = "left")
volume_slider.pack(padx = (10, 22), side = "right")
volume_label.pack()

#Меню
main_menu = Menu(window)
window.config(menu = main_menu)

#Добавляем в меню возможность добавить музыкальные файлы
menu = Menu(main_menu)
main_menu.add_cascade(label = "File", menu = menu)
menu.add_command(label = "About", command = about)
menu.add_separator()
menu.add_command(label = "Reload", command = window.update)
menu.add_separator()
menu.add_command(label = "Add Song To Playlist", command = player.add_file_to_playlist)
menu.add_separator()
menu.add_command(label = "Clear Playlist", command = player.clear_playlist)
menu.add_separator()
menu.add_command(label = "Quit", command = window.destroy)


if __name__ == "__main__":
    volume_but.config(command = player.mute)
    volume_slider.config(command = player.volume_slide)
    window.mainloop()