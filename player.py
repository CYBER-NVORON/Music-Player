from tkinter import filedialog, messagebox, PhotoImage
from time import strftime, gmtime, sleep
from pygame import mixer
import mutagen

class Player():
    
    def __init__(self, songs_list, start_time, end_time, music_slider, volume_label, volume_slider, volume_but):
        self.mixer = mixer
        self.songs_list = songs_list
        self.start_time = start_time
        self.end_time = end_time
        self.music_slider = music_slider
        self.volume_label = volume_label
        self.volume_slider = volume_slider
        self.volume_but = volume_but
        self.songs_list_full = {}
        self.ispaused = False
        self.islooped = False
        self.ismuted = False
        self.mixer.init()
        self.volume_slider.set(100)
        self.mixer.music.set_volume(100)
        self.volume_none_img = PhotoImage(file = "./gui/volume_none.png")
        self.volume_low_img = PhotoImage(file = "./gui/volume_low.png")
        self.volume_mid_img = PhotoImage(file = "./gui/volume_mid.png")
        self.volume_high_img = PhotoImage(file = "./gui/volume_high.png")
        self.volume_but.config(image = self.volume_high_img)
        self.last_volume = 100
    
    def get_full_path(self, song_name):
        return self.songs_list_full[song_name]

    def add_file_to_playlist(self):
        songs = filedialog.askopenfilenames(title = "Choose A Song", filetypes=[("mp3 Files", "*.mp3"), 
                                                                                ("wav Files", "*.wav"),
                                                                                ("flac Files", "*.flac")]) # Появляется окно для выбора файлов
        for song in songs: # Перебираем каждую песню из списка
            if song.split(".")[-1] not in ["mp3", "wav", "flac"]: # На случай, если как-то обошли системную блокировку неподдерживаемых файлов
                messagebox.showwarning(title = "Неподдерживаемый тип файла", message = "Тип файла нет в списке поддерживаемых файлов!")
            else:
                song_name = ".".join([song.split("/")[-1].split(".")[i] for i in range(0, len(song.split("/")[-1].split("."))-1)]) # Вычленяем название файла от папок и типа
                self.songs_list_full[song_name] = song
                self.songs_list.insert('end', song_name)

    def remove(self):
        self.stop()
        self.songs_list_full.pop(self.songs_list.get("active"))
        self.songs_list.delete("active")

    def clear_playlist(self):
        self.stop()
        self.songs_list_full.clear()
        self.songs_list.delete(0, 'end')

    def stop(self):
        try:
            self.start_time.after_cancel(self.loop)
        except:
            pass
        self.mixer.music.stop()
        self.music_slider.set(0)
        self.music_slider.config(from_ = 0, to = 100)
        self.start_time.config(text="")
        self.end_time.config(text="")

    def previous_song(self):
        if len(self.songs_list_full) != 0:
            self.stop()
            if self.islooped:
                next_song_id = self.songs_list.curselection()[0]
            else:
                try:
                    next_song_id = self.songs_list.curselection()[0] - 1
                except:
                    next_song_id = 0

            self.songs_list.select_clear(0, 'end')
            self.songs_list.activate(next_song_id)
            self.songs_list.select_set(next_song_id)

            self.play_song()
                
    def play_song(self):
        if len(self.songs_list_full) != 0:
            self.stop()
            song = self.get_full_path(self.songs_list.get("active"))
            try:
                self.mixer.music.load(song)
                self.mixer.music.play(start = 0)
            except:
                messagebox.showerror(title = "Ошибка в запуске файла", message = "Не удалось прочитать файл!")
                self.remove()
                return
            self.music_slider.set(0)
            self.start_time.config(text="00:00:00")
            self.end_time.config(text = strftime('%H:%M:%S', gmtime(int(mutagen.File(song).info.length))))
            self.music_slider.config(from_ = 0, to = int(mutagen.File(song).info.length))
            self.play_time()
    
    def pause_song(self):
        if len(self.songs_list_full) != 0:
            if self.ispaused:
                self.mixer.music.unpause()
            elif not self.ispaused:
                self.mixer.music.pause()
            self.ispaused = not self.ispaused

    def next_song(self):
        if len(self.songs_list_full) != 0:
            self.stop()
            if self.islooped:
                next_song_id = self.songs_list.curselection()[0]
            else:
                try:
                    next_song_id = self.songs_list.curselection()[0] + 1
                except:
                    next_song_id = 0
            self.songs_list.select_clear(0, 'end')
            self.songs_list.activate(next_song_id)
            self.songs_list.select_set(next_song_id)
            self.play_song()
    
    def play_time(self):
        cur_time = int(self.mixer.music.get_pos() / 1000) + 1
        song = self.get_full_path(self.songs_list.get("anchor"))
        try:
            song_info = mutagen.File(song)
        except:
            pass
        if int(self.music_slider.get()) + 1 == song_info.info.length:
            return self.next_song()
        elif self.ispaused:
            pass
        elif abs(int(self.music_slider.get()) - cur_time) < 2:
            self.music_slider.set(cur_time)
            self.start_time.config(text = strftime('%H:%M:%S', gmtime(cur_time-1)))
        else:
            self.music_slider.set(int(self.music_slider.get()))
            self.start_time.config(text = strftime('%H:%M:%S', gmtime(int(self.music_slider.get()))))
            self.music_slider.set(int(self.music_slider.get()) + 1)
            try:
                self.mixer.music.set_pos(int(self.music_slider.get()))
            except:
                return self.next_song()

        self.loop = self.start_time.after(1000, self.play_time)

    def volume_slide(self, val):
        slider_val = int(val)
        self.mixer.music.set_volume(int(slider_val) / 100.)
        self.volume_label.config(text = str(slider_val) + "%")
        if slider_val == 0:
            self.volume_but.config(image = self.volume_none_img)
        elif slider_val <= 33:
            self.volume_but.config(image = self.volume_low_img)
        elif 33 < slider_val <= 66:
            self.volume_but.config(image = self.volume_mid_img)
        elif 66 < slider_val <= 100:
            self.volume_but.config(image = self.volume_high_img)

    def mute(self):
        if int(self.volume_slider.get()) == 0:
            self.volume_slider.set(self.last_volume)
        else:
            last_volume_temp = int(self.volume_slider.get())
            self.volume_slider.set(0)
            self.last_volume = last_volume_temp
