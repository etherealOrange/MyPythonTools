# Windows Python小工具
这里存放一些我的Python小工具，不一定适合所有人，希望你喜欢。
### **注意：所有工具均只有.py代码，可以使用cmd运行（本文不提供任何python安装教程）**

### **[ACG命名统计](#ACG命名统计)**
### **[手机B站美图分类](#手机B站美图分类)**
### **[文件夹开罐器](#文件夹开罐器)**

## ACG命名统计
- 这是我为了管理我下载的番剧，为了能不把重复的番剧放在磁盘中设计的小工具
- 功能：把将要放入存储磁盘的ACG文件夹和存储磁盘中已经分好类的文件夹进行比较，输出是否存在，存在位置
- 我使用import：`import os` `import json`
- 注意：其实它并不是那么智能只能区分 **文件夹名字** （但我觉得目前来说足够了）
- 注意：Search2.py是最新的可用版本，main.py为以前的版本
- Search2.py配合ACG_Sum_config.json运行
- 讲解json文件内容：
- ACG_srt ---》你需要储存到的ACG根目录
- Search_srt ---》你目前的ACG根目录
- ACG_sort_names ---》分类方法和分类文件夹
- "T0": "ACG T0" ---》Key为分类的级别，value为这个分类的文件夹
- Filter ---》为加快遍历，防止意外发生，检测到value内的后缀会结束遍历
- Result_name ---》结果输出文件名

## 手机B站美图分类
- 为了存储手机里日益增多的B站图片，我要把他们分类存储
- 功能:把图片分类到(gif,长高宽矮,宽高长矮,长宽相等)四个文件夹中👇
- 其中(长高宽矮,宽高长矮,长宽相等)内又分为"小于1000", "小于2000", "小于3000", "小于4000", "大于4000",这里数字指的是图片最长边
- **B站美图分类** 为最新工具，带有（old）的不可靠
- 我是使用的import：
```python
from datetime import datetime
import os
import json
import shutil
import threading
from PIL import Image
Image.MAX_IMAGE_PIXELS = None # 我禁用了PIL的像素大小限制,不要读取太大的文件哦!(你的电脑爆炸了我不管)
```
- 你可以使用Apache然后用ConextMenuManager(右键管理器)添加一个右键cmd指令`"你的Apache的python.exe位置" "%1"
- 然后就可以直接右键启动.py文件


## 文件夹开罐器
- 为解决测试时文件夹嵌套问题
- 功能:把当前文件夹处理它自己意外的所有文件,从文件夹中提出放到"./开罐结果"文件夹内
- 会在重复文件加上后缀为"-重复 0"
- 注意:提取界面cmd提示框就是什么都没有,提取完自动关闭
- 我的import:`import os ` `import shutil`
