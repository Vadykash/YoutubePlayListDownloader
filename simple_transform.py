import moviepy.editor as mpe
import os
import argparse
import moviepy.editor as mpe

from multiprocessing import Process

def getName(dir_name):
    name_file = os.path.join(dir_name, "name.txt")
    name = None
    with open(name_file) as f:
        name = f.read()

    return name

def doTransform(dir_name, out_dir):
    tmp_name = os.path.join(dir_name, "video.mp4")
    real_name = getName(dir_name)
    real_name_path = os.path.join(out_dir, "%s.mp4" % real_name)

    print("TRN: ", tmp_name, real_name_path)
    #return
    if not real_name:
        print("Error:", "cant find real name")
        return
    
    video = mpe.VideoFileClip(tmp_name)

    
    src_audio_path = os.path.join(dir_name, "audio.mp4")
    tmp_audio_path = os.path.join(dir_name, "audio.mp4")

    #os.rename(real_name_path, tmp_audio_path)
    audio = mpe.AudioFileClip(tmp_audio_path)
    final = video.set_audio(audio)
    final.write_videofile(real_name_path)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", action='store', dest="dir_path", required = True)
    parser.add_argument("-o", action='store', dest="out_path", required = True)

    args = parser.parse_args()
    work_path = args.dir_path
    out_path = args.out_path

    if not os.path.exists(out_path):
        print("No out path")
        exit(-1)

    if not os.path.isdir(out_path):
        print("Out not dir")
        exit(-2)

    num_progs = 8
    proc_idx = 0
    progs = []

    for cur_dir_path in [os.path.join(work_path, f) for f in os.listdir(work_path)]:
        print (cur_dir_path)
      
        p = Process(target=doTransform, args = (cur_dir_path, out_path, ) )
        p.start()
        progs.append(p)

        proc_idx += 1
        if proc_idx == num_progs:
            print("Start waiting")
            for p in progs:
                p.join()

            proc_idx = 0
            progs = []


    if progs:
        for p in progs:
            p.join()


    print("Done")


if __name__ == "__main__":
    main()
