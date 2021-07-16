import tkinter as tk
import os
import pygame
from win32api import GetSystemMetrics
from moviepy.editor import *
from mutagen.mp3 import MP3
from PIL import ImageTk, Image
from random import *

class MusicPlayer:

    def __init__(self, master, width, height, pauseImg, playImg, fastForwardImg, rewindImg, shuffleImg):

        self.shuffled = False
        self.paused = False
        self.currentSong = -1

        # retrieves the path to each song in the MusicMasterFolder and stores them in a dictionary.
        #---------------------------------------------------------------------------------------------------------------
        self.musicD = {}
        directory = r"C:\MusicMasterFolder"
        num = 0
        for filename in os.listdir(directory):
            self.musicD[num] = (os.path.join(directory, filename))
            num += 1
        self.numSongs = len(self.musicD)
        #---------------------------------------------------------------------------------------------------------------

        # Adjusts the size of the listbox depending on the screens resolution
        #------------------------
        h = 30
        if width == 1920:
            h = 50
        #------------------------

        # Main Frame (contains song listbox)
        self.master = master
        self.title = tk.Label(self.master, text="Music Player", font="helvetica 25 bold", background="thistle3")
        self.frame = tk.Frame(self.master, background="thistle4")
        self.songListBox = tk.Listbox(self.frame, height=h, width=150, bd=5, background="thistle1")
        self.songListBox.grid(padx=10, pady=10, row=0, columnspan=3)

        # Inserts all of the songs into the main listbox
        #------------------------------------------
        for i in self.musicD:
            temp = self.musicD[i]
            temp = temp.split("\\")
            temp = temp[2]
            temp = temp[:-4]
            self.songListBox.insert("end", temp)
        #-------------------------------------------

        self.frame.grid(row=1, column=0)

        # stores the currents songs length
        self.songLength = 0


        # Button Frame
        #---------------------------------------------------------------------------------------------------------------
        self.buttonFrame = tk.Frame(self.master, background="thistle3")

        self.currentSongText = tk.Label(self.buttonFrame, font="helvetica 10", background="thistle3")
        self.currentSongText.grid(row=0, column=0)

        self.songDisplay = tk.Scale(self.buttonFrame, from_=0, to_=self.songLength, orient="horizontal", length=500, highlightbackground="thistle4", highlightthickness=3)
        self.songDisplay.grid(row = 1, column=0, padx=5, pady=(0, 20))

        self.rewindButton = tk.Button(self.buttonFrame, image=rewindImg, font="helvetica 10", command=self.play, background="white")
        self.rewindButton.grid(row=1, column=1, padx=5, pady=(0, 20))

        self.playButton = tk.Button(self.buttonFrame, image=playImg, font="helvetica 10", command=self.play, background="white")
        self.playButton.grid(row=1, column=2, padx=5, pady=(0, 20))

        self.fastForwardButton = tk.Button(self.buttonFrame, image=fastForwardImg, font="helvetica 10", command=self.skip, background="white")
        self.fastForwardButton.grid(row=1, column=3, padx=5, pady=(0, 20))

        self.pauseButton = tk.Button(self.buttonFrame, image=pauseImg, font="helvetica 10", command=self.pause, background="white")
        self.pauseButton.grid(row=1, column=4, padx=5, pady=(0, 20))

        self.shuffleButton = tk.Button(self.buttonFrame, image=shuffleImg, font="helvetica 10", command=self.shuffle, background="white")
        self.shuffleButton.grid(row=1, column=5, padx=5, pady=(0, 20))

        self.volumeText = tk.Label(self.buttonFrame, text="volume", font="helvetica 10", background="thistle3")
        self.volumeText.grid(row=0, column=6)

        self.volumeScale = tk.Scale(self.buttonFrame, from_=0, to_=100, orient="horizontal", highlightbackground="thistle4", highlightthickness=3, command=self.updateVolume)
        self.volumeScale.grid(row=1, column=6, padx=10, pady=(0, 20))

        self.buttonFrame.grid(row=2, column=0, pady=10)
        #---------------------------------------------------------------------------------------------------------------


        # Defaults the songs volume to zero
        pygame.mixer.music.set_volume(0)


    # called by the play button
    #-------------------------------------------------------------------------------------------------------------------
    def play(self):
        # gets the corresponding number to the selected song within the listbox
        selection1 = self.songListBox.curselection()
        selection = -1
        if selection1 != ():
            selection = selection1[0]

        if self.paused and self.currentSong == selection:
            pygame.mixer.music.unpause()
            self.pauseButton.config(background="white")
            self.updateTime()
        else:
            if selection1 != ():
                self.currentSong = selection
                song = MP3(r"" + self.musicD[selection])
                length = round(song.info.length)
                self.songLength = length
                self.songDisplay.config(from_=0, to_=self.songLength)
                pygame.mixer.music.load(r"" + self.musicD[selection])
                pygame.mixer.music.play()
                songTitle = self.songListBox.get(selection)
                self.currentSongText.config(text=songTitle)

                self.updateTime()
    #-------------------------------------------------------------------------------------------------------------------


    # called when the volume scale is adjusted
    #-------------------------------------------------------------------------------------------------------------------
    def updateVolume(self, volume):
        pygame.mixer.music.set_volume(int(volume) / 100)
    #-------------------------------------------------------------------------------------------------------------------


    # called by the skip button
    #-------------------------------------------------------------------------------------------------------------------
    def skip(self):
        if self.currentSong != -1:
            if not self.shuffled:
                self.songListBox.selection_clear(0, "end")
                self.songListBox.select_set(self.currentSong + 1)
                self.songListBox.activate(self.currentSong + 1)
                self.play()
            else:
                self.songListBox.select_clear(0, "end")
                num = randint(0, self.numSongs)
                self.songListBox.select_set(num)
                self.songListBox.activate(num)
                self.play()
    #-------------------------------------------------------------------------------------------------------------------



    #  called by the rewind button
    #-------------------------------------------------------------------------------------------------------------------
    def restart(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.rewind()
    #-------------------------------------------------------------------------------------------------------------------

    def shuffle(self):
        if not self.shuffled:
            self.shuffled = True
            self.shuffleButton.config(background="red")
        else:
            self.shuffled = False
            self.shuffleButton.config(background="white")

    # called by the pause button
    #-------------------------------------------------------------------------------------------------------------------
    def pause(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.paused = True
            self.pauseButton.config(background="red")
    #-------------------------------------------------------------------------------------------------------------------


    # calls itself every second when a song is playing
    #-------------------------------------------------------------------------------------------------------------------
    def updateTime(self):
        if pygame.mixer.music.get_busy():
            pos = (round(pygame.mixer.music.get_pos() / 1000))
            self.songDisplay.set(pos)
            self.master.after(1000, self.updateTime)
            if pos == self.songLength:
                self.songListBox.selection_clear(0, "end")
                self.songListBox.select_set(self.currentSong + 1)
                self.songListBox.activate(self.currentSong + 1)
                self.play()
    #-------------------------------------------------------------------------------------------------------------------


    # Opens the add homework page
    #def new_window(self):
        #self.newWindow = tk.Toplevel(self.master)
        #self.app = AddHomeworkPage(self.newWindow)


#-----------------------------------------------------------------------------------------------------------------------
def main():
    pygame.mixer.init()
    pygame.init()
    root = tk.Tk()

    root.state("zoomed")

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # gets the resolution of the users monitor
    screenWidth = GetSystemMetrics(0)
    screenHeight = GetSystemMetrics(1)

    # opens all the icon images
    i1 = Image.open("icons8-pause-30.png")
    pauseImg = ImageTk.PhotoImage(i1)
    i2 = Image.open("icons8-fast-forward-30.png")
    fastForwardImg = ImageTk.PhotoImage(i2)
    i3 = Image.open("icons8-rewind-30.png")
    rewindImg = ImageTk.PhotoImage(i3)
    i4 = Image.open("icons8-play-30.png")
    playImg = ImageTk.PhotoImage(i4)
    i5 = Image.open("icons8-shuffle-32.png")
    shuffleImg = ImageTk.PhotoImage(i5)

    # sets the size of the window to match the users resolution
    root.geometry(f"{screenWidth}x{screenHeight}")

    # sets the background of the root window
    root.config(background="thistle3")

    app = MusicPlayer(root, screenWidth, screenHeight, pauseImg, playImg, fastForwardImg, rewindImg, shuffleImg)

    # refreshes the window
    root.mainloop()
#-----------------------------------------------------------------------------------------------------------------------



if __name__ == '__main__':
    main()
