import ffmpeg

def mp3(file):
    try:
        ffmpeg.input(file).output("media/repair.mp3").run()
        return "Succes."

    except ffmpeg.Error as e:
        return "Failled."

