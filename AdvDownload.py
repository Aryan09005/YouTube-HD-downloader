import subprocess, os, shutil, sys, requests, argparse
from pprint import pprint
try:
    from pytube import YouTube# Sure that YouTube and Playlist can be downloaded
except Exception as e:
    print(e)
    print('[Run] pip(/3) install pytube')
    exit()

print('''
██╗   ██╗ ██████╗ ██╗   ██╗████████╗██╗   ██╗██████╗ ███████╗██████╗ 
╚██╗ ██╔╝██╔═══██╗██║   ██║╚══██╔══╝██║   ██║██╔══██╗██╔════╝██╔══██╗
 ╚████╔╝ ██║   ██║██║   ██║   ██║   ██║   ██║██████╔╝█████╗  ██████╔╝
  ╚██╔╝  ██║   ██║██║   ██║   ██║   ██║   ██║██╔══██╗██╔══╝  ██╔══██╗
   ██║   ╚██████╔╝╚██████╔╝   ██║   ╚██████╔╝██████╔╝███████╗██║  ██║
   ╚═╝    ╚═════╝  ╚═════╝    ╚═╝    ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝v2.0
''')

class AdvDownload():
    def __init__(self,url):
        '''checking for installation and making small sequence changes for playlist and single video'''
        self.checkinstall()
        if 'https://www.youtube.com/playlist' in url:
            from pytube import Playlist
            import re
            self.pl = Playlist(url)
            self.pl._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
            qual = input('Wish to download (H)D[ 720 & + ] or (S)D[ 720 & - (30FPS mostly)] or just (a)udio (h/s/a): ')[0].lower()
            for url in self.pl.video_urls:
                self.yt = YouTube(url)
                print(f'\nTITLE {self.yt.title}')
                if qual == 'h':
                    self.makeDirs()
                streams = self.getQuality(qual)
                self.downloader(qual)
                if qual == 'a':
                   continue
                self.compile()

        else:
            self.yt = YouTube(url)
            print(f'\nTITLE {self.yt.title}')
            qual = input('Wish to download (H)D[ 720 & + ] or (S)D[ 720 & - (30FPS mostly)] or just (a)udio (h/s/a): ')[0].lower()
            if qual == 'h':
                self.makeDirs()
            streams = self.getQuality(qual)
            self.downloader(qual)
            if qual == 'a':
                sys.exit()
            self.compile()
        
        
    def downloader(self, qual):
        '''Download audio and or video stream'''
        if qual == 'h':
            # Downloading the video
            print('\n   {0:<13}{1:>10}{2:>9}'.format('No.','Resolution','fps'))
            for num, stream in enumerate(self.yt.streams.filter(adaptive=True).order_by('resolution').desc()):
                print(f'|-Stream {num:-<{5}} {stream.resolution:->{10}} {stream.fps:->{10}}')
            choice = int(input('Enter the stream number: '))
            print(self.yt.streams.filter(adaptive=True).order_by('resolution').desc()[choice].download('video'))
            #  DOWNLOADING VIDEO DONE
            print(self.yt.streams.filter(only_audio=True).order_by('filesize').desc().first().download('audio'))
            # DOWNLOADING AUDIO DONE
            
        elif qual == 's':
            print('\n   {0:<13}{1:>10}{2:>9}'.format('No.','Resolution','fps'))
            for num, stream in enumerate(self.yt.streams.filter(progressive=True).order_by('resolution').desc()):
               print(f'\Stream {num:-<{5}} {stream.resolution:->{10}} {stream.fps:->{10}}')
            choice = int(input('Enter the stream number: '))
            print(self.yt.streams.filter(progressive=True).order_by('resolution').desc()[choice].download())
            # DOWNLOAD COMPLETED
            # sys.exit()
        elif qual == 'a':
            ret = self.yt.streams.filter(only_audio=True).order_by('filesize').desc().first().download()
            ext = os.path.splitext(ret)[1]
            if ext != 'mp3':
                shutil.move(ret,self.yt.title+'.mp3')
            # DOWNLOADED AND EXTENSION CHANGED
            # sys.exit()

            
    def compile(self):
        '''Complies and deletes the folders'''
        audiofiles = os.listdir('audio')
        videofiles = os.listdir('video')
        for audiofile in audiofiles:
            audio = audiofile.split('.')[0]
            for videofile in videofiles:
                video = videofile.split('.')[0]
                if audio == video:
                    print(f'Compiling {audiofile} with {videofile}')
                    subprocess.Popen(f'ffmpeg -i audio/"{audiofile}" -i video/"{videofile}" -c copy "{audiofile}" -y').wait()
        # COMPILING DONE
        # if input('Delete the uncompiled audio and video files?(y/n)')[0].lower() == 'y':
        shutil.rmtree('video')
        shutil.rmtree('audio')
        #REMOVED THE FOLDERS
                
    def getQuality(self, qual):
        '''Get what quality the user wants'''
        if qual == 's':
            # for stream in self.yt.streams.filter(progressive=True):
                # print(stream)
            return self.yt.streams.filter(progressive=True).order_by('resolution').desc()
        elif qual == 'h':
            return self.yt.streams.filter(adaptive=True).order_by('resolution').desc()

    def checkinstall(self):
        '''Checking what OS and if ffmpeg is installed and installing ffmpeg'''
        platform = sys.platform
        if platform == 'linux':
            print('[+] Linux detected checking for ffmpeg installation')
            res = sp.run('dpkg -s ffmpeg')
            if res.returncode != 0:
                print('ffmpeg not installed')
                subprocess.Popen('sudo apt-get install ffmpeg',shell=True).wait()
        elif platform == 'win32':
            print('[+] Windows detected checking for ffmpeg installation')
            if not os.path.exists('C:\FFMPEG\\ffmpeg.exe'):
                print('[+] No installation checking for temp ffmpeg.exe file')
                if 'ffmpeg.exe' not in os.listdir():
                    print('[+] ffmpeg.exe not found')
                    files = {'ffmpeg.exe':'https://filebin.net/505d74kxyod1h80c/ffmpeg.exe?t=9mqqo7ms'}
                    print('Downloading ffmpeg.exe')
                    res = requests.get(files['ffmpeg.exe'])
                    fil = open('ffmpeg.exe','wb')
                    for chunk in res.iter_content(100000):
                        fil.write(chunk)
                    fil.close()# HAVE TO CHECK IF THIS WORKS
                else:
                    print('[+] ffmpeg.exe found in current dir')
                    

    def makeDirs(self):
        '''
        make dirs for uncompiled audio and video
        '''
        os.makedirs('audio',exist_ok=True)
        os.makedirs('video',exist_ok=True)
        # print('making temp audio and video dirs for uncompiled data')


def getargs():
    parser = argparse.ArgumentParser(description='Download YouTube videos')
    parser.add_argument('-u','--url',help='url of YouTube page')
    args = parser.parse_args()
    return args

if getargs().url != None:
    y = AdvDownload(getargs().url)
else:
    print('[syntax] python AdvDownload.py -u https:\\\\YOUTUBE_URL')
