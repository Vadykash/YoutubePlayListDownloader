from pytube import YouTube
from pytube import Playlist

import sys
import os
import shutil

import argparse
import datetime as dt

def selectVideo(streams):
    resolutions = ["1080p", "720p"]
    for r in resolutions:
        res = streams.filter(subtype='mp4', res=r).first()
        if res:
            break
    return res

def selectAudio(streams):
    bpms = [ "128kbps", "128kbps"]
    res = None
    for bpm in bpms:
        res = video.streams.filter(only_audio=True, abr=bpm).first()
        if res:
            break

    return res

def printDict(d):
    for k, v in d.items():
        print("%s\t:\t%s" % (str(k), str(v)))

#=================================================================================
parser = argparse.ArgumentParser()
parser.add_argument("-p", action='store', dest="plist", required = True)
parser.add_argument("-d", action='store', dest="up_dir", required = False)

args = parser.parse_args()
pl_adr = args.plist
up_dir = args.up_dir

print (pl_adr)

p = Playlist(pl_adr)

cur_date = dt.datetime.now()
date_str = cur_date.strftime("%Y_%m_%d_%H_%M_%S")
if up_dir is None:
    up_dir = os.path.join(".", "work_" + date_str)

print(up_dir)

if not os.path.exists(up_dir):
    os.mkdir(up_dir)

print("Date: ", date_str)

videos = list(p.videos)

def downloadObj(obj, out_path, to_rename, url):
    commit_file = os.path.join(cur_dir, "commin_%s.txt" % to_rename)
    if os.path.exists(commit_file):
        print("Already download for <%s> url: <%s>" % (to_rename, url))
        return;
    v_name = videoObj.download(output_path = out_path)
    #tmp_name = os.path.join(out_path, "video.mp4")
    tmp_name = os.path.join(out_path, "%s.mp4" % to_rename)
    os.rename(v_name, tmp_name)
    with open(commit_file, "w") as f:
        f.write(url)

print(len(videos))
for idx, video in enumerate(videos):
    print(video.__dict__)
    print("Captions", video.captions)
    print("Streams")
    for s in video.streams:
        print("\t", s)

    #debug purposes
    if not True:
        videoObj = selectVideo(video.streams)
        printDict(videoObj.__dict__)
        video_name = video.streams[0].title
        print("TT: ", video.streams[0].title)
        cur_dir = os.path.join(up_dir, str(idx))
        title_file = os.path.join(cur_dir, "name.txt")
        with open(title_file, "w") as f:
            f.write(video_name)
        continue

    watch_url = video.watch_url
    cur_dir = os.path.join(up_dir, str(idx))
    if not os.path.exists(cur_dir):
        os.mkdir(cur_dir)
        
    title_file = os.path.join(cur_dir, "name.txt")
    video_name = video.streams[0].title
    print("TT: ", video.streams[0].title)
    with open(title_file, "w") as f:
        f.write(video_name)


    videoObj = selectVideo(video.streams)
    if not videoObj:
        print("Error no video obj for: idx: <%d>, url: <%s>" % (idx, wathc_url))
        continue

    print("WU: ", watch_url)
    try:
        downloadObj(videoObj, cur_dir, "video", watch_url)
    except Exception as ex:
        print("Error video: idx: %d, url: %s, error: %s" % (idx, watch_url, str(ex))) 

    has_audio = hasattr(videoObj, "acodec")
    if not has_audio:
        audioObj = selectAudio(video.streams)
        if not audioObj:
            print("Error no audio for: idx <%d> url: <%s>" % (idx, watch_url))
            continue
        try:
            downloadObj(audioObj, cur_dir, "audio", watch_url)
        except Exception as ex:
            print("Error audio: idx: %d, url: %s, error: %s" % (idx, watch_url, str(ex))) 
            pass
    #v_name = video.streams.filter(subtype='mp4', res="1080p").first().download(output_path = tmp_dir)

