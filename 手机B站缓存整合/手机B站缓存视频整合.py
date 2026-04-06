import os
import subprocess as sp
import json
import shutil
import zipfile
import requests
from pathlib import Path

root = Path("./")
name_subXML = Path("danmaku.xml")
name_messageJSON = Path("entry.json")
name_indexJSON = Path("index.json")
name_audioM4S = Path("audio.m4s")
name_videoM4S = Path("video.m4s")
name_cover = Path("cover.jpg")
name_folder_dirs: list[Path] = [name_videoM4S, name_audioM4S, name_indexJSON]


def PJoin2(path1: Path, path2: Path) -> Path:
    return path1 / path2


def generate_mix_audio_video_cover_command(video_path: Path, audio_path: Path, cover_path: Path,
                                           out_video_path: Path) -> list[str]:
    video_path = video_path.absolute()
    audio_path = audio_path.absolute()
    cover_path = cover_path.absolute()
    out_video_path = out_video_path.absolute()
    return [
        "ffmpeg", "-loglevel", "quiet",
        "-i", os.fspath(video_path),
        "-i", os.fspath(audio_path),
        "-i", os.fspath(cover_path),
        "-c", "copy",
        "-map", "0", "-map", "1", "-map", "2",
        "-disposition:v:1", "attached_pic",
        "-y", os.fspath(out_video_path)
    ]


def search_danmaku(ls):
    if name_subXML in ls:
        return True
    else:
        return False


def folder_legality(folder_path: Path) -> list[Path]:
    ls: list[str] = os.listdir(folder_path)
    if name_videoM4S in ls and name_audioM4S in ls and name_indexJSON in ls:
        return [PJoin2(folder_path, name) for name in name_folder_dirs]
    else:
        return []


def retrieve_message(json_path:Path)->list[str]:
    if json_path.exists():
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
            trans_table = str.maketrans(illegal_chars, '_' * len(illegal_chars))
            title = title.translate(trans_table)
            return [cover, title]
    return []


def download_image(url:str, root_path:Path)->bool:
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        save_path = PJoin2(root_path, name_cover)
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        return True
    except Exception as ex:
        print(ex)
        return False


def zip_files(files_path:list[Path], title):
    with zipfile.ZipFile(title + '.zip', "w") as zip_ref:
        for file in files_path:
            zip_ref.write(file, file.name)


def do_mix_video(root_path:Path, root_dirs:list[Path]):
    folder_count = sum(path.is_dir() for path in root_dirs)
    if folder_count != 1:
        print(root_dirs)
        print("出现的文件夹数量不为1")
        return
    entry_path = PJoin2(root_path, name_messageJSON)
    if entry_path not in root_dirs:
        print(root_dirs)
        print("中缺少：")
        print(name_messageJSON)
        return
    [cover_url, title] = retrieve_message(entry_path)
    if cover_url is None:
        print(entry_path)
        print("提取图片地址失败")
        return
    if not download_image(cover_url, root_path):
        print(cover_url + "\n下载失败")
        return
    cover_path = PJoin2(root_path, name_cover)

    folder_path:Path = Path("")
    for path in root_dirs:
        if path.is_dir():
            folder_path = path
            break
    folder_context = folder_legality(folder_path)
    if not folder_context:
        print(folder_path)
        print("中的文件不符合标准")
        return

    [video_path, audio_path, index_path] = folder_context
    index_new_path = PJoin2(root_path, name_indexJSON)
    shutil.move(index_path, index_new_path)

    out_video_path = PJoin2(root, Path(title + ".mp4"))
    try:
        sp.run(generate_mix_audio_video_cover_command(video_path, audio_path, cover_path, out_video_path), check=True)
        zip_files([cover_path, entry_path, PJoin2(root_path, name_subXML), index_new_path], title)
    except Exception as ex:
        print(ex)
        return


def search_dirs(root_path:Path):
    ls:list[str] = os.listdir(root_path)
    if search_danmaku(ls):
        root_dirs:list[Path] = [PJoin2(root_path, Path(d)) for d in ls]
        do_mix_video(root_path, root_dirs)
    else:
        for l in ls:
            path = PJoin2(root_path, Path(l))
            if path.is_dir():
                search_dirs(path)


if __name__ == '__main__':
    search_dirs(root)
    print("结束按任意键退出。")
    input()
