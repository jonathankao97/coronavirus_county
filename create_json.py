import re
import json

file = open('uszips.csv', 'r')
dict = {}
for index, line in enumerate(file):
    if index != 0:
        info = re.split(",", line)
        key_value = info[11][1:-1] + "," + info[5][1:-1]
        obj = [int(info[10][1:-1]), int(info[0][1:-1]), info[3][1:-1], int(info[8][1:-1])]
        if key_value in dict:
            dict.get(key_value).append(obj)
        else:
            dict[key_value] = [obj]
file.close()
f = open("dict.json", "w+")
f.write(json.dumps(dict))
f.close()
