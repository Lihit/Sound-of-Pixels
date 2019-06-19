# coding: utf-8
import os
import argparse
import cv2
import subprocess
import multiprocessing


def extract_videos(data_dir, subdir_name, vid_name, root_audio, root_frame, fps, audio_rate):
    data_subdir = os.path.join(data_dir, subdir_name)
    video_file_path = os.path.join(data_subdir, vid_name)
    vid_id = vid_name.split('.')[0]
    # extract audio
    audio_file_path = os.path.join(root_audio, subdir_name, vid_id + ".mp3")
    if not os.path.exists(os.path.dirname(audio_file_path)):
        os.makedirs(os.path.dirname(audio_file_path))
    aud_command = ["ffmpeg", "-i", video_file_path, "-ab", "160k", "-ac", "1", "-ar", str(audio_rate), "-vn",
                   audio_file_path]
    subprocess.call(aud_command)
    video_file_path_fps = os.path.join(data_subdir, vid_id + '_fps.mp4')
    vid_command = ["ffmpeg", "-i", video_file_path, "-r", "8", video_file_path_fps]
    subprocess.call(vid_command)
    # extract video
    count = 1
    cap = cv2.VideoCapture(video_file_path_fps)
    cap_fps = cap.get(cv2.CAP_PROP_FPS)
    assert cap_fps == fps
    while 1:
        # get a frame
        frame_file_path = os.path.join(root_frame, subdir_name, vid_name, '{:06d}.jpg'.format(count))
        if not os.path.exists(os.path.dirname(frame_file_path)):
            os.makedirs(os.path.dirname(frame_file_path))
        ret, frame = cap.read()
        if not ret:
            break
        count += 1
        cv2.imwrite(frame_file_path, frame)
    cap.release()
    os.remove(video_file_path_fps)
    print('I am done!')


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

    # use multiprocessing pool
    pool = multiprocessing.Pool(8)
    for subdir_name in os.listdir(args.data_dir):
        data_subdir = os.path.join(args.data_dir, subdir_name)
        for vid_name in os.listdir(data_subdir):
            print('%s:%s' % (subdir_name, vid_name))
            pool.apply_async(extract_videos, args=(
                args.data_dir, subdir_name, vid_name, args.root_audio, args.root_frame, args.fps, args.audio_rate))
    pool.close()
    pool.join()
