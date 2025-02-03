import os
import sys
from datetime import datetime
# !!!!!!!!!!修改位置!!!!!!!!!!
ARCH_src = "ARCH"
diary_src = "diary"
Ignore_Month = False

def loadYuml():
    global addI
    global fileTime
    global DocType
    global summary
    global feelings
    global mentioned

    addI = 1
    while i + addI < len(lines) and lines[i + addI] != "---":
        splited = lines[i + addI].split(":", 1)
        if "Date" == splited[0]:
            fileTime = splited[1][1:]
        elif "文档类型" == splited[0]:
            DocType = splited[1][1:]
        elif "摘要" == splited[0]:
            summary = splited[1][1:]
        elif "心情" == splited[0]:
            addI += 1
            while "- " in lines[i + addI]:
                feelings.append(lines[i + addI].split("- ", 1)[1])
                addI += 1
            continue
        elif "提及内容" == splited[0]:
            addI += 1
            while "- " in lines[i + addI]:
                mentioned.append(lines[i + addI].split("- ", 1)[1])
                addI += 1
            continue
        else:
            print("你的元数据类型名称有错误！！")
            input()
            exit(-100)
        addI += 1
    return addI


if __name__ == '__main__':
    MdList = os.listdir(diary_src)
    now = datetime.now()
    year = now.year
    month = (now.month - 2) % 12 + 1
    filtered_list = []
    for i in MdList:
        if not os.path.isfile(diary_src + "/" + i):
            continue
        if "md" != i.split(".")[-1].lower():
            continue
        filestat = os.stat(diary_src + "/" + i)
        createdTime = filestat.st_ctime
        createdTime = datetime.fromtimestamp(createdTime)
        if createdTime.year != year:
            continue
        if not Ignore_Month and createdTime.month != month:
            continue
        filtered_list.append(i)
    MdList = filtered_list
    print(MdList)
    year = str(now.year)

    if month < 10:
        month = "0" + str(month)
    else:
        month = str(month)
    diarys_info = []
    for j in range(len(MdList)):
        with open(diary_src + "/" + MdList[j], "r", encoding="utf-8") as f:
            # 去除结尾\n
            lines = [l.rstrip() for l in f.readlines()]
            #时间
            fileTime = ""
            # 文档类型
            DocType = ""
            # 摘要
            summary = ""
            # 心情
            feelings = []
            # 提及内容
            mentioned = []
            # 内容
            content = []
            FirstInYuml = True
            i = 0
            while i < len(lines):
                if FirstInYuml and "---" == lines[i]:
                    InYuml = False
                    addI = loadYuml()
                    i += addI
                else:
                    if "-" != lines[i]:
                        content.append(lines[i])
                i += 1
        diarys_info.append([fileTime, DocType, summary, feelings, mentioned,content])
    diarys_info.sort(key=lambda x: x[0][:10])
    for i in diarys_info:
        print(i)
    YumHead = (f"---\nDate: {now.strftime("%Y-%m-%d %H:%M")}\n文档类型: "
               f"日记\n摘要: 总结{year}-{month}的全部日记和吐槽\n心情: \n提及内容:\n - 日记总结\n---\n\n")

    with open(ARCH_src+'/'+year+'-'+month+'日记总结.md','w',encoding="utf-8") as f:
        f.write(YumHead)
        for j in range(len(MdList)):
            CallOutContent = (f"> [!Document]- {diarys_info[j][0]} {diarys_info[j][1]} {diarys_info[j][2]}\n"
                          f"> 心情::{','.join(diarys_info[j][3])}\n"
                          f"> 提及内容::{','.join(diarys_info[j][4])}\n"
                          f"> ")+'\n> '.join(diarys_info[j][5])+'\n\n'
            f.write(CallOutContent)
    print("成功完成日记归档!")
    input()