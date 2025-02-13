import os
import subprocess as sp
import json
import shutil

root = "./"
name_subXML = "danmaku.xml"
name_messageJSON = "entry.json"
name_indexJSON = "index.json"
name_audioM4S = "audio.m4s"
name_videoM4S = "video.m4s"

def PJoin2(path1, path2):
    return os.path.join(path1, path2)
def MakeCommand(ALL_Path,output_name):
    abs_path = os.path.abspath(ALL_Path)
    return  [
        "ffmpeg","-loglevel","quiet",
        "-i", PJoin2(abs_path,name_audioM4S),
        "-i", PJoin2(abs_path,name_videoM4S),
        "-c", "copy", "-y",
        PJoin2(abs_path,output_name + ".mp4"),
    ]


def Start_Process(path):
    ls = os.listdir(path)
    if name_subXML in ls and name_messageJSON in ls:
        next_folder = ""
        for i in ls:
            if os.path.isdir(PJoin2(path,i)):
                next_folder = PJoin2(path,i)
                # 请确保你在entry.json的文件夹只有一个，因为默认应该只有一个
                break
        if next_folder == "":
            print("你的文件夹不存在")
            input()
            exit(-1)
        next_ls = os.listdir(next_folder)

        with open(PJoin2(path, name_messageJSON), 'r', encoding='utf-8') as f:
            data = json.load(f)
            title = data["title"]
            page_data = data["page_data"]
            if "part" in page_data.keys():
                part = page_data["part"]
            if part == "":
                fixed_output_name = part
            else:
                fixed_output_name = title
        if name_audioM4S in next_ls and name_videoM4S in next_ls and name_indexJSON in next_ls:
            shutil.move(PJoin2(next_folder,name_audioM4S),PJoin2(path,name_audioM4S))
            shutil.move(PJoin2(next_folder,name_videoM4S),PJoin2(path,name_videoM4S))
            shutil.move(PJoin2(next_folder,name_indexJSON),PJoin2(path,name_indexJSON))
            try:
                sp.run(MakeCommand(path, fixed_output_name), check=True)
            except sp.CalledProcessError as e:
                print(e)
                input()
                exit(-100)
            before_folder = os.path.abspath(path).rsplit("\\",1)[0]
            shutil.move(path,PJoin2(before_folder,fixed_output_name))

    else:
        for i in ls:
            if os.path.isdir(PJoin2(path,i)):
                Start_Process(PJoin2(path,i))


if __name__ == '__main__':
    first_Folder = os.listdir(root)
    for path in first_Folder:
        if os.path.isdir(path):
            Start_Process(path)


