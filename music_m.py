# -*- coding:utf-8 -*-
import pygame, threading, time, os, sys, Queue
from playsound import playsound

class MusicUtil(object):
    __music = None
    __index = 0
    __musics = []
    __records = Queue.Queue(maxsize=50)
    __isPlay = False
    __dir = ''
    __record_dir = ''
    __event = threading.Event()

    def __init__(self, dir, recordDir):
        self.__dir = dir
        self.__record_dir = recordDir
        pygame.mixer.init()
        self.__music = pygame.mixer.music
        self.__music.set_endevent()
        self.flush_musics()
        self.__event.clear()

    def __thread(self):
        while 1:
            if self.__isPlay and self.__music.get_busy():
                time.sleep(5)
            elif self.__isPlay:
                self.nex()
            else:
                self.__event.wait()

    def __record_thread(self):
        p_num = 0
        while 1:
            p_num = p_num+1
            record_path = self.__records.get()
            if self.__isPlay:
                self.__music.stop()
                self.__music.load(record_path)
                self.__music.play()
                while self.__music.get_busy():
                    time.sleep(1)
                self.play()
            else:
                self.__music.load(record_path)
                self.__music.play()
            if p_num % 5 == 0:
                for file in os.listdir(self.__record_dir):
                    print file
                    try:
                        os.remove(os.path.join(self.__record_dir, file))
                    except OSError:
                        pass

    def run_thread(self):
        t = threading.Thread(target=self.__thread)
        t.setDaemon(True)
        t.start()
        r = threading.Thread(target=self.__record_thread)
        r.setDaemon(True)
        r.start()

    def flush_musics(self):
        for file in os.listdir(self.__dir):
            if file.endswith('.mp3') or file.endswith('.wav'):
                file = os.path.join(self.__dir, file).decode(sys.getfilesystemencoding())
                self.__musics.append(file)

    def play(self):
        if len(self.__musics) > 0:
            if self.__music.get_busy():
                self.__music.unpause()
            else:
                filePath = (self.__musics[self.__index]).encode('utf-8')
                print 'playing ' + filePath
                self.__music.load(filePath)
                self.__music.play(0)
            self.__isPlay = True
            self.__event.set()
            return True
        else:
            return False

    def pause(self):
        self.__music.pause()
        self.__isPlay = False
        self.__event.clear()
        return False

    def nex(self):
        if self.__isPlay:
            self.__index=(self.__index+1)%len(self.__musics)
            self.__music.stop()
            filePath = (self.__musics[self.__index]).encode('utf-8')
            print 'nex playing %s' % filePath
            self.__music.load(filePath)
            self.__music.play()
            return True
        else:
            return False

    def prev(self):
        if self.__isPlay:
            if self.__index-1<0:
                self.__index=len(self.__musics)-1
            self.__index = (self.__index - 1) % len(self.__musics)
            self.__music.stop()
            filePath = (self.__musics[self.__index]).encode('utf-8')
            print 'prev playing %s' % filePath
            self.__music.load(filePath)
            self.__music.play()
            return True
        else:
            return False

    def set_volume(self, volume):
        self.__music.set_volume(volume)
        return True

    def get_volume(self):
        return self.__music.get_volume()

    def is_play(self):
        return self.__isPlay

    def add_record(self, record_path):
        self.__records.put(record_path)

