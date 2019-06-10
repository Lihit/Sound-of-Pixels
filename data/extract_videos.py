# coding: utf-8
import numpy as np
import pandas as pd
import json
import youtube_dl
import subprocess
import time
import threading
import os
import shutil
import multiprocessing
import json
import argparse
import cv2
import subprocess


def extract_videos(data_dir, root_audio, root_frame, fps, audio_rate):
    for subdir_name in os.listdir(data_dir):
        data_subdir = os.path.join(data_dir, subdir_name)
        for vid_name in os.listdir(data_subdir):
            video_file_path = os.path(data_subdir, vid_name)
            vid_id = os.path.basename(vid_name)
            # extract audio
            audio_file_path = os.path.join(root_audio, subdir_name, vid_id + ".mp3")
            if not os.path.exists(os.path.dirname(audio_file_path)):
                os.makedirs(os.path.dirname(audio_file_path))
            command = ["ffmpeg", "-i", video_file_path, "-ab", "160k", "-ac", "1", "-ar", str(audio_rate), "-vn",
                       audio_file_path]
            subprocess.call(command)
            # extract video
            count = 0
            count2 = 1
            cap = cv2.VideoCapture(video_file_path)
            while 1:
                # get a frame
                frame_file_path = os.path.join(root_frame, subdir_name, vid_name, "%d.jpg" % (count2))
                if not os.path.exists(os.path.dirname(frame_file_path)):
                    os.makedirs(os.path.dirname(frame_file_path))
                    count2 += 1
                ret, frame = cap.read()
                if count % fps == 0:
                    cv2.imwrite(frame_file_path, frame)
                count += 1
            cap.release()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', default='./data_all',
                        help="data dir which you want to save")
    parser.add_argument('--root_audio', default='./data/audio',
                        help="root for extracted audio files")
    parser.add_argument('--root_frame', default='./data/frames',
                        help="root for extracted video frames")
    parser.add_argument('--fps', default=8, type=int,
                        help="fps of video frames")
    parser.add_argument('--audio_rate', default=11025, type=int,
                        help="rate of audio")
    args = parser.parse_args()
    if not os.path.exists(args.root_audio):
        os.makedirs(args.root_audio)
    if not os.path.exists(args.root_frame):
        os.makedirs(args.root_frame)
