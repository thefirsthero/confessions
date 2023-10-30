import platform
import os
import random
import re
import json
import sys
import subprocess
import asyncio
import multiprocessing
import logging
from typing import Tuple
import datetime
import argparse

# PyTorch
import torch

# ENV
from dotenv import load_dotenv, find_dotenv

# OpenAI Whisper Model PyTorch
# import whisper
import stable_whisper as whisper

# MicrosoftEdge TTS
import edge_tts
from edge_tts import VoicesManager

# FFMPEG (Python)
import ffmpeg

# utils.py
from utils import *

# msg.py
import msg

HOME = os.getcwd()

# Logging
if not os.path.isdir('log'):
    os.mkdir('log')

with KeepDir() as keep_dir:
    keep_dir.chdir("log")
    log_filename = f'{datetime.date.today()}.log'
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
        ]
    )
    logger = logging.getLogger(__name__)

# Load existing video data from video.json
jsonData = json.load(open('video.json', encoding='utf-8'))
json_copy = jsonData.copy()

# Create a copy of the JSON data
json_copy = jsonData.copy()

async def main() -> bool:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="small", help="Model to use",
                        choices=["tiny", "base", "small", "medium", "large"], type=str)
    parser.add_argument("--non_english", action='store_true',
                        help="Don't use the English model.")
    parser.add_argument("--url", metavar='U', default="https://www.youtube.com/watch?v=intRX7BRA90",
                        help="Youtube URL to download as a background video.", type=str)
    parser.add_argument("--tts", default="en-US-ChristopherNeural",
                        help="Voice to use for TTS", type=str)
    parser.add_argument(
        "--list-voices", help="Use `edge-tts --list-voices` to list all voices", action='help')
    parser.add_argument("--random_voice", action='store_true',
                        help="Random voice for TTS", default=False)
    parser.add_argument("--gender", choices=["Male", "Female"],
                        help="Gender of the random TTS voice", type=str)
    parser.add_argument(
        "--language", help="Language of the random TTS voice for example: en-US", type=str)
    parser.add_argument("-v", "--verbose", action='store_true',
                        help="Verbose")
    args = parser.parse_args()

    if args.random_voice:
        args.tts = None
        if not args.gender or not args.language:
            console.log(
                f"{msg.ERROR}When using --random_voice, please specify both --gender and --language arguments.")
            sys.exit(1)
        else:
            voices = await VoicesManager.create()
            voices = voices.find(Gender=args.gender, Locale=args.language)
            if len(voices) == 0:
                # Locale not found
                console.log(
                    f"{msg.ERROR}Specified TTS language not found. Make sure you are using the correct format. For example: en-US")
                sys.exit(1)

            # Check if the language is English
            if not str(args.language).startswith('en'):
                args.non_english = True

    # Clear the terminal
    console.clear()

    logger.debug('Creating video')
    with console.status(msg.STATUS) as status:
        load_dotenv(find_dotenv())  # Optional

        console.log(
            f"{msg.OK}Finish loading environment variables")
        logger.info('Finish loading environment variables')

        # Check if GPU is available for PyTorch (CUDA).
        if torch.cuda.is_available():
            console.log(f"{msg.OK}PyTorch GPU version found")
            logger.info('PyTorch GPU version found')
        else:
            console.log(
                f"{msg.WARNING}PyTorch GPU not found, using CPU instead")
            logger.warning('PyTorch GPU not found')

        download_video(url=args.url)

        # OpenAI-Whisper Model
        model = args.model
        if args.model != "large" and not args.non_english:
            model = args.model + ".en"
        whisper_model = whisper.load_model(model)

        console.log(f"{msg.OK}OpenAI-Whisper model loaded")
        logger.info('OpenAI-Whisper model loaded')

        # # Text 2 Speech (Edge TTS API)
        for video_id, video in enumerate(json_copy):
            series = video['series']
            part = video['part']
            outro = video['outro']
            path = video['path']
            text = video['text']

            req_text, filename = create_full_text(
                path, series, part, text, outro)

            console.log(f"{msg.OK}Text converted successfully")
            logger.info('Text converted successfully')

            await tts(req_text, outfile=filename, voice=args.tts, random_voice=args.random_voice, args=args)

            console.log(
                f"{msg.OK}Text2Speech mp3 file generated successfully!")
            logger.info('Text2Speech mp3 file generated successfully!')

            # Whisper Model to create SRT file from Speech recording
            srt_filename = srt_create(
                whisper_model, path, series, part, text, filename)

            console.log(
                f"{msg.OK}Transcription srt and ass file saved successfully!")
            logger.info('Transcription srt and ass file saved successfully!')

            # Background video with srt and duration
            background_mp4 = random_background()
            file_info = get_info(background_mp4, verbose=args.verbose)
            final_video = prepare_background(
                background_mp4, filename_mp3=filename, filename_srt=srt_filename, duration=int(file_info.get('duration')), series_name=series, part_name=part, verbose=args.verbose)

            console.log(
                f"{msg.OK}MP4 video saved successfully!\nPath: {final_video}")
            logger.info(f'MP4 video saved successfully!\nPath: {final_video}')

            # Remove the processed video data from the original JSON
            jsonData.remove(video)
    
            # Write the updated JSON data back to the file
            with open('video.json', 'w', encoding='utf-8') as json_file:
                json.dump(jsonData, json_file, ensure_ascii=False, indent=4)

    console.log(f'{msg.DONE}')
    return True


def download_video(url: str, folder: str = 'background'):
    if not os.path.isdir(folder):
        os.mkdir(folder)
    with KeepDir() as keep_dir:
        keep_dir.chdir(folder)
        with subprocess.Popen(['yt-dlp', '--restrict-filenames', '--merge-output-format', 'mp4', url]) as process:
            pass
        console.log(
            f"{msg.OK}Background video downloaded successfully")
        logger.info('Background video downloaded successfully')
    return


def random_background(folder_path: str = "background"):
    with KeepDir() as keep_dir:
        keep_dir.chdir(f"{HOME}{os.sep}{folder_path}")
        files = os.listdir(".")
        random_file = random.choice(files)
    return random_file


def get_info(filename: str, verbose: bool = False):
    try:
        with KeepDir() as keep_dir:
            keep_dir.chdir("background")
            probe = ffmpeg.probe(filename)
            video_stream = next(
                (stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
            audio_stream = next(
                (stream for stream in probe['streams'] if stream['codec_type'] == 'audio'), None)
            try:
                duration = float(audio_stream['duration'])
            except Exception:
                if verbose:
                    console.log(
                        f"{msg.WARNING}MP4 default metadata not found")
                    logger.warning('MP4 default metadata not found')
                duration = (datetime.datetime.strptime(
                    audio_stream['DURATION'], '%H:%M:%S.%f') - datetime.datetime.min).total_seconds()
            if video_stream is None:
                if verbose:
                    console.log(
                        f"{msg.WARNING}No video stream found")
                    logger.warning('No video stream found')
                bit_rate = int(audio_stream['bit_rate'])
                return {'bit_rate': bit_rate, 'duration': duration}

            width = int(video_stream['width'])
            height = int(video_stream['height'])
            return {'width': width, 'height': height, 'duration': duration}
    except ffmpeg.Error as e:
        console.log(f"{msg.ERROR}{e.stderr}")
        logger.exception(e.stderr)
        sys.exit(1)


def prepare_background(background_mp4, filename_mp3, filename_srt, duration: int, series_name, part_name, verbose: bool = False):
    # Get length of MP3 file to be merged with
    audio_info = get_info(filename_mp3)

    # Get starting time:
    audio_duration = int(round(audio_info.get('duration'), 0))
    # print(duration-audio_duration)
    ss = random.randint(0, (duration-audio_duration))
    audio_duration = convert_time(audio_info.get('duration'))
    if ss < 0:
        ss = 0

    srt_filename = filename_srt.split('\\')[-1]
    # Update this line to point to the 'Trash' subdirectory
    srt_path = os.path.join(os.getcwd(), "Trash")


    create_directory(os.getcwd(), "output")
    outfile = f"{os.getcwd()}{os.sep}output{os.sep}{series_name}_{part_name}.mp4"

    with KeepDir() as keep_dir:
        keep_dir.chdir("background")
        mp4_absolute_path = os.path.abspath(background_mp4)

    if verbose:
        rich_print(
            f"{filename_srt = }\n{mp4_absolute_path = }\n{filename_mp3 = }\n", style='bold green')   #
        # 'Alignment=9,BorderStyle=3,Outline=5,Shadow=3,Fontsize=15,MarginL=5,MarginV=25,FontName=Lexend Bold,ShadowX=-7.1,ShadowY=7.1,ShadowColour=&HFF000000,Blur=141'Outline=5
    args = ["ffmpeg", "-ss", str(ss), "-t", str(audio_duration), "-i", mp4_absolute_path, "-i", filename_mp3, "-map", "0:v", "-map", "1:a", "-filter:v",
            f"crop=ih/16*9:ih, scale=w=1080:h=1920:flags=bicubic, gblur=sigma=2, subtitles={srt_filename}:force_style=',Alignment=8,BorderStyle=7,Outline=3,Shadow=5,Blur=15,Fontsize=15,MarginL=45,MarginR=55,FontName=Lexend Bold'", "-c:v", "libx265", "-preset", "5", "-b:v", "5M", "-c:a", "aac", "-ac", "1", "-b:a", "96K", f"{outfile}", "-y", "-threads", f"{multiprocessing.cpu_count()/2}"]

    if verbose:
        rich_print('[i] FFMPEG Command:\n'+' '.join(args)+'\n', style='yellow')

    with KeepDir() as keep_dir:
        keep_dir.chdir(srt_path)
        with subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE) as process:
            pass

    return outfile


def srt_create(model, path: str, series: str, part: int, text: str, filename: str) -> bool:
    """
    Srt_create is a function that takes in five arguments: a model for speech-to-text conversion, a path to a directory, a series name, a part number, text content, and a filename for the audio file. The function uses the specified model to convert the audio file to text, and creates a .srt file with the transcribed text and timestamps.

    Args:
        model: A model object used for speech-to-text conversion.
        path (str): A string representing the path to the directory where the .srt file will be created.
        series (str): A string representing the name of the series.
        part (int): An integer representing the part number of the series.
        text (str): A string representing the main content of the audio file.
        filename (str): A string representing the name of the audio file.

    Returns:
        bool: A boolean indicating whether the creation of the .srt file was successful or not.

    """
    transcribe = model.transcribe(
        filename, regroup=True, fp16=torch.cuda.is_available())
    transcribe.split_by_gap(0.5).split_by_length(
        38).merge_by_gap(0.15, max_words=2)
    series = series.replace(' ', '_')
    srtFilename = os.path.join(
        f"{path}{os.sep}{series}{os.sep}", f"{series}_{part}")
    transcribe.to_srt_vtt(srtFilename+'.srt', word_level=True)
    transcribe.to_ass(srtFilename+'.ass', word_level=True)
    os.chdir(HOME)
    return srtFilename+".srt"


def convert_time(time_in_seconds):
    hours = int(time_in_seconds // 3600)
    minutes = int((time_in_seconds % 3600) // 60)
    seconds = int(time_in_seconds % 60)
    milliseconds = int((time_in_seconds - int(time_in_seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"


def batch_create(filename: str) -> None:
    """
    Batch_create is a function that takes in a filename as input and creates a new file with the concatenated contents of all the files in the './batch/' directory, sorted in alphanumeric order.

    Args:
    filename (str): A string representing the name of the output file to be created.

    Returns:
    None: This function does not return anything, but creates a new file with the contents of all the files in the './batch/' directory sorted in alphanumeric order.

    """
    with open(filename, 'wb') as out:
        def sorted_alphanumeric(data):
            def convert(text): return int(
                text) if text.isdigit() else text.lower()
            def alphanum_key(key): return [convert(c)
                                           for c in re.split('([0-9]+)', key)]
            return sorted(data, key=alphanum_key)

        for item in sorted_alphanumeric(os.listdir('./batch/')):
            filestuff = open('./batch/' + item, 'rb').read()
            out.write(filestuff)


def create_directory(path: str, directory: str) -> bool:
    """
    Create_directory is a function that takes in two arguments: a path to a directory and a name for a new directory. The function creates a new directory with the specified name in the specified path if it doesn't already exist, and returns a boolean indicating whether the directory was created.

    Args:
    path (str): A string representing the path to the directory where the new directory will be created.
    directory (str): A string representing the name of the new directory.

    Returns:
    bool: Returns True if a new directory was created, False otherwise.

    """
    current_dir = os.getcwd()
    os.chdir(path)
    if not os.path.isdir(directory):
        os.mkdir(directory)
        os.chdir(current_dir)
        return True
    return False


def create_full_text(path: str = '', series: str = '', part: int = 1, text: str = '', outro: str = '') -> Tuple[str, str]:
    """
    Create_full_text is a function that takes in four arguments: a path to a directory, a series name, a part number, text content, and outro content. The function creates a new text with series, part number, text, and outro content and returns a tuple containing the resulting text and the filename.

    Args:
        path (str): A string representing the path to the directory where the new text file will be created. Default value is an empty string.
        series (str): A string representing the name of the series. Default value is an empty string.
        part (int): An integer representing the part number of the series. Default value is 1.
        text (str): A string representing the main content of the text file. Default value is an empty string.
        outro (str): A string representing the concluding remarks of the text file. Default value is an empty string.

    Returns:
        Tuple[str, str]: A tuple containing the resulting text and the filename of the text file.

    """
    req_text = f"{series} Part {part}.\n{text}\n{outro}" # This line had the series, part and then the text & outro
    # req_text = f"{text}\n{outro}" # This line removes the series & part, it's just the text & outro now
    series = series.replace(' ', '_')
    filename = f"{path}{os.sep}{series}{os.sep}{series}_{part}.mp3"
    create_directory(path, directory=series)
    return req_text, filename


async def tts(final_text: str, voice: str = "en-US-ChristopherNeural", random_voice: bool = False, stdout: bool = False, outfile: str = "tts.mp3", args=None) -> bool:
    """
    Tts is an asynchronous function that takes in four arguments: a final text string, a voice string, a boolean value for random voice selection, a boolean value to indicate if output should be directed to standard output or not, and a filename string for the output file. The function uses Microsoft Azure Cognitive Services to synthesize speech from the input text using the specified voice, and saves the output to a file or prints it to the console.

    Args:
        final_text (str): A string representing the text to be synthesized into speech.
        voice (str): A string representing the name of the voice to be used for speech synthesis. Default value is "en-US-ChristopherNeural".
        random_voice (bool): A boolean value indicating whether to randomly select a male voice for speech synthesis. Default value is False.
        stdout (bool): A boolean value indicating whether to output the speech to the console or not. Default value is False.
        outfile (str): A string representing the name of the output file. Default value is "tts.mp3".

    Returns:
        bool: A boolean indicating whether the speech synthesis was successful or not.

    """
    voices = await VoicesManager.create()
    if random_voice:
        voices = voices.find(Gender=args.gender, Locale=args.language)
        voice = random.choice(voices)["Name"]
    communicate = edge_tts.Communicate(final_text, voice)
    if not stdout:
        await communicate.save(outfile)
    return True

if __name__ == "__main__":

    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(main())

    except Exception as e:
        loop.close()
        console.log(f"{msg.ERROR}{e}")
        logger.exception(e)

    finally:
        loop.close()

    sys.exit(1)