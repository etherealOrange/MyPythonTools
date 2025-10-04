import os
import subprocess as sp
import json
import shutil
import zipfile

import requests

root = "./"
name_subXML = "danmaku.xml"
name_messageJSON = "entry.json"
name_indexJSON = "index.json"
name_audioM4S = "audio.m4s"
name_videoM4S = "video.m4s"
name_cover = "cover.jpg"
name_folder_dirs = [name_videoM4S, name_audioM4S, name_indexJSON]

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

def generate_mix_audio_video_cover_command(video_path,audio_path,cover_path,out_video_path):
    video_path = os.path.abspath(video_path)
    audio_path = os.path.abspath(audio_path)
    cover_path = os.path.abspath(cover_path)
    out_video_path = os.path.abspath(out_video_path)
    return [
        "ffmpeg","-loglevel","quiet",
        "-i", video_path,
        "-i", audio_path,
        "-i", cover_path,
        "-c", "copy",
        "-map","0", "-map","1", "-map","2",
        "-disposition:v:1","attached_pic",
        "-y",out_video_path
    ]

def search_danmaku(ls):
    if name_subXML in ls:
        return True
    else:
        return False

def folder_legality(folder_path):
    ls = os.listdir(folder_path)
    if name_videoM4S in ls and name_audioM4S in ls and name_indexJSON in ls:
        return [PJoin2(folder_path,name) for name in name_folder_dirs]
    else:
        return []

def retrieve_message(json_path):
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

            if "cover" in data and "title" in data:
                cover = data["cover"]
                title = data["title"]
            else:
                return []

            if "page_data" in data and "part" in data["page_data"]:
                part = data["page_data"]["part"]
                if part != "":
                    title = part
            illegal_chars = '《》、“”‘’\'*?/\\|<>:\"'
            title = title.replace(illegal_chars,'_')
            return [cover,title]
    return []

def download_image(url,root_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        save_path = os.path.join(root_path, name_cover)
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        return True
    except Exception as ex:
        print(ex)
        return False

def zip_files(files_path,title):
    with zipfile.ZipFile(title+'.zip', "w") as zip_ref:
        for file in files_path:
            zip_ref.write(file,os.path.basename(file))

def do_mix_video(root_path,root_dirs):
    folder_count = sum(os.path.isdir(path) for path in root_dirs)
    if folder_count != 1:
        print(root_dirs+"\n出现的文件夹数量不为1")
        return
    entry_path = PJoin2(root_path,name_messageJSON)
    if entry_path not in root_dirs:
        print(root_dirs+"\n中缺少："+name_messageJSON)
        return
    [cover_url,title] = retrieve_message(entry_path)
    if cover_url is None:
        print(entry_path+"\n提取图片地址失败")
        return
    if not download_image(cover_url, root_path):
        print(cover_url+"\n下载失败")
        return
    cover_path = PJoin2(root_path,name_cover)

    folder_path = ""
    for path in root_dirs:
        if os.path.isdir(path):
            folder_path = path
            break
    folder_context = folder_legality(folder_path)
    if folder_context == []:
        print(folder_path + "\n中的文件不符合标准")
        return

    [video_path,audio_path,index_path] = folder_context
    index_new_path = PJoin2(root_path,name_indexJSON)
    shutil.move(index_path,index_new_path)

    out_video_path = PJoin2(root,title+".mp4")
    try:
        sp.run(generate_mix_audio_video_cover_command(video_path, audio_path,cover_path,out_video_path), check=True)
        zip_files([cover_path, entry_path, PJoin2(root_path, name_subXML), index_new_path], title)
    except Exception as ex:
        print(ex)
        return


def search_dirs(root_path):
    ls = os.listdir(root_path)
    if search_danmaku(ls):
        root_dirs = [PJoin2(root_path,d) for d in ls]
        do_mix_video(root_path, root_dirs)
    else:
        for l in ls:
            path = PJoin2(root_path,l)
            if os.path.isdir(path):
                search_dirs(path)

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
    # first_Folder = os.listdir(root)
    # for path in first_Folder:
    #     if os.path.isdir(path):
    #         Start_Process(path)

    search_dirs(root)
    print("结束按任意键退出。")
    input()


