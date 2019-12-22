from pydub import AudioSegment
from collections import namedtuple
import os

Track = namedtuple('Track', ['title', 'time'])

class SourceAudio:
    def __init__(self, path):
        self.path = path
        self.title, self.fmt = path.split('.', 1)
        print("Opening file.")
        self.audio_file_segment = AudioSegment.from_file(path, self.fmt)

    def set_tracks(self, album_info):
        with open(album_info) as info:
            info = map(lambda x : x.strip().split('-') ,info.readlines())
            self.tracks = [Track(title.strip(), min_to_milisenconds(start.strip())) for start, title in info]

    def cut_audio(self):
        start = 0
        self.audios = []
        for i in range(len(self.tracks)-1):
            self.audios.append(self.audio_file_segment[self.tracks[i].time:self.tracks[i+1].time])
        else:
            self.audios.append(self.audio_file_segment[self.tracks[i].time:])

    def save_files(self):
        artist, album = map(lambda x: x.strip(), self.title.split("-", 1))
        cmd = 'mkdir '+ "_".join([artist, album])
        os.system(cmd)
        for i,audio in enumerate(self.audios):
            track_path = "./"+"_".join([artist, album])+"/"+str(i+1)+"-"+".".join([self.tracks[i].title,self.fmt])            
            audio.export(track_path, format=self.fmt, tags={
            'artist': artist, 'album': album,
            })
    
def min_to_milisenconds(time):
    min, sec = map(int, time.split(':'))
    return((min*60)+sec)*1000


x = SourceAudio("Windows96 - Nematophy.mp3")
x.set_tracks("album_tracks.txt")
x.cut_audio()
x.save_files()