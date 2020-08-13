import sys, subprocess, shutil
try:
    from pytube import YouTube
except ModuleNotFoundError as e:
    print('Module pytube not installed')
    print('run [pip install pytube]')
# importing os in win32



platform = sys.platform
if platform == 'linux':
    print('Checking if ffmpeg is installed')
    result = subprocess.run('dpkg -s ffmpeg')
    
    if result.returncode != 0:
        print('Not installed, installing')
        subprocess.Popen('sudo apt-get install ffmpeg',shell=True).wait()

elif platform == 'win32':
    
    import os
    files = {
            'ffmpeg.exe':'https://srv-file10.gofile.io/download/OzwhgD/ffmpeg.exe',
             'ffplay.exe':'https://srv-file10.gofile.io/download/OzwhgD/ffplay.exe',
             'ffprobe.exe':'https://srv-file10.gofile.io/download/OzwhgD/ffprobe.exe'
             }

    print('Checking for installation files')
    # make the C:\FFMPEG directory and then check for files
    if not os.path.exists('C:\FFMPEG'):
        # os.makedirs('C:\FFMPEG')
        # print('Making Directory for ffmpeg')
        print('No installation of ffmpeg')
    
    for fil in files.keys():
        # Check if file does not exists then download it form link
        if not os.path.exists(f'C:\FFMPEG\{fil}'):
            print(f"Downloading: {fil}")
            import requests as req
            print(files[fil])
            res = req.get(files[fil])
            name = os.path.basename(files[fil])
            writeTo = open(name,'wb')
            for chunk in res.iter_content(100000):
                writeTo.write(chunk)
            writeTo.close()
            # STILL HAVE TO ADD THE FINAL FEATURE TO ADD THE FILES TO THE C:\FFMPEG
'''
Done checking requirnments
Download part         
Progressive / low quality is always with audio and video but adaptive or high quality is mostly without audio 
Make seperate directorirs for audio and video
'''
# seperate directoirs
os.makedirs('audio',exist_ok=True)
os.makedirs('video',exist_ok=True)
# Check if user wants adaptive or progressive
input('Do want high quality (adaptive) or low quality (progressive) {[(h/l)]}?')
# download audio and save it in audio
yt = YouTube('https://www.youtube.com/watch?v=VZ60FEaZZXA')
# yt = YouTube('https://www.youtube.com/watch?v=3WGjIXeJ1Tg')
print('\n##### '+yt.title+' #####')
for stream in yt.streams.filter(only_audio=True).order_by('filesize').desc():
    print(stream,stream.filesize)
# yt.streams.filter(only_audio=True).order_by('filesize').desc().first().download('audio')
print('\t\tVIDEO')
# download video and save it in video
for stream in yt.streams.filter(adaptive=True).order_by('resolution').desc():
    print(stream)
# yt.streams.filter(adaptive=True).order_by('resolution').desc().first().download('video')
'''
Download done now merging files
'''
filesInAudio = os.listdir('audio')
filesInVideo = os.listdir('video')
for fil in filesInAudio:
    for file in filesInVideo:
        if fil == file:
            print(f'Compiling {fil}')
            subprocess.Popen(f'ffmpeg -i audio/"{fil}" -i video/"{fil}" -c copy "{fil}"',shell=True).wait()

if input('Delete pre-complied audio and video files?'):
    shutil.rmtree('audio')
    shutil.rmtree('video')

print('Downloading and compiling done')