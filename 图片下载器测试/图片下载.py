import requests

url = "https://img-blog.csdnimg.cn/92fb30f4b5c040a59cb4d82d4a37d41e.png"
image = requests.get(url).content

with open("test.jpg", "wb") as f:
    f.write(image)
