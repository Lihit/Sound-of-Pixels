import youtube_dl
import os
import multiprocessing
import json
import argparse


def download_vid(data_dir, key, video_id):
    data_dir_key = os.path.join(data_dir, key)
    if not os.path.exists(data_dir_key):
        os.makedirs(data_dir_key)

    ydl_opts = {
        'format': 'mp4[height<=360]',
        'outtmpl': r"{}/{}.%(ext)s".format(data_dir_key, video_id)
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['https://www.youtube.com/watch?v=' + video_id])
    print("Im Done")


def downloadAllVideos(data_dir, video_dict):
    """
    download the video
    :param video_dict: all video ids saved in the dict
    :return:
    """

    # use multiprocessing pool
    pool = multiprocessing.Pool(4)
    for key in video_dict:
        # Extract the words consisting of video_id, start_time, end_time, list of video_tags
        for v_id in video_dict[key]:
            pool.apply_async(download_vid, (data_dir, key, v_id))
    pool.close()
    pool.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', default='./data_all',
                        help="data dir which you want to save")
    parser.add_argument('--duet_json', default='./MUSIC_duet_videos.json',
                        help="path of duet_json")
    parser.add_argument('--solo_json', default='./MUSIC_solo_videos.json',
                        help="path of solo_json")
    args = parser.parse_args()
    # download all video first, without any preprocessing
    duet_json = args.duet_json
    solo_json = args.solo_json
    with open(duet_json, 'r') as fin:
        duet_dict = json.load(fin)
    with open(solo_json, 'r') as fin:
        solo_dict = json.load(fin)
    print(duet_dict.keys())
    video_dict = duet_dict["videos"]
    video_dict.update(solo_dict['videos'])

    print('total number of video:%d' % (sum([len(video_dict[key]) for key in video_dict])))
    # download video
    data_dir = args.data_dir  # path to save data
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    downloadAllVideos(data_dir, video_dict)
