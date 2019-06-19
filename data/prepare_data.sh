#!/usr/bin/env bash
# download data first
python download_video_audio.py
# extract videos
python extract_videos.py
# create index files
cd ..
python data/create_index_files.py