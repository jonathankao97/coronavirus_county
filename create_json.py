import re
import json

file = open('uszips.csv', 'r')
dict = {}
for index, line in enumerate(file):
    if index != 0:
        info = re.split(",", line)
        obj = [int(info[10][1:-1]), int(info[0][1:-1]), info[3][1:-1], int(info[8][1:-1])]
        if info[11][1:-1] in dict:
            dict.get(info[11][1:-1]).append(obj)
        else:
            dict[info[11][1:-1]] = [obj]
file.close()
f = open("dict.json", "w+")
f.write(json.dumps(dict))
f.close()
