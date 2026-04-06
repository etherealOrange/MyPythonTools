import os
import json
import requests

url = "https://img-blog.csdnimg.cn/6804157b46ca4506a9fc382c05eb4e58.png"
entry = "./entry.json"

def download_image(url, save_folder):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        os.makedirs(save_folder, exist_ok=True)
        save_path = os.path.join(save_folder, os.path.basename(url))
        if os.path.exists(save_path):
            print(save_path+" already exists, skipping...")
            return
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
    except Exception as ex:
        print(ex)

def retrieve_cover_utl(json_path):
    if os.path.exists(json_path):
        with open(json_path,'r' ,encoding='utf-8') as f:
            data = json.load(f)
            if "cover" in data:
                return data["cover"]
    return None


if __name__ == '__main__':
    cover_url = retrieve_cover_utl(entry)
    if cover_url is None:
        print("Cover url not found")
        exit(1)
    else:
        print("Cover url found")
        download_image(cover_url, "./")

    # download_image(url,"./")
    # image = requests.get(url).content
    # with open("test.jpg", "wb") as f:
    #     f.write(image)
