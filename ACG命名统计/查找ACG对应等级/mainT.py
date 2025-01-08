import os

src_dir = "G:\统计.txt"
lines = []
srclines = []
list = []
result=[]

def select_lvl(s):
    if s == "ACG T0":
        return "T0"
    elif s == "ACG T1":
        return "T1"
    elif s == "ACG T2":
        return "T2"
    elif s == "ACG T3":
        return "T3"
    elif s == "ACG T4":
        return "T4"
    elif s == "ACG T5":
        return "T5"
    else:
        return 0


if __name__ == '__main__':
    ls = os.listdir()
    if "统计.txt" in ls:
        with open("统计.txt", "r", encoding="utf-8") as f:
            for line in f:
                lines.append(line.strip())
            with open(src_dir, "r", encoding="utf-8") as src:
                for line in src:
                    srclines.append(line.strip())
                lvl = ""
                for l in lines:
                    flag = 0
                    one = l[0]
                    for sl in srclines:
                        if select_lvl(sl) != 0:
                            lvl = select_lvl(sl)
                        if one == sl[0]:
                            # print(l + "     " + sl)
                            if l == sl:
                                flag = 1
                                list.append(lvl)
                                break
                    if flag == 0:
                        list.append("不存在")
        t = 0
        for name in lines:
            result.append((name,list[t]))
            t += 1
        result.sort(key=lambda x: x[1])
        with open("比较结果.txt", "w", encoding="utf-8") as f:
            for l in result:
                f.write(l[0]+"  "+l[1] +"\n")
