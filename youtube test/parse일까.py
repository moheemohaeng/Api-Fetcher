import json
import pandas as pd


path = r"D:\file.json"
file = open(path)
json_file = json.load(file)
level = 4
#don't have to put the column names, but it will make the excel in nicer order
df = pd.DataFrame(columns = ["key0", "dt0", "key1", "dt1", "key2", "dt2", "key3", "dt3", "key4", "dt4"])
def parse_json(key, value,curent_level,massage):
    global df
    global level
    if curent_level == level:
        df = df.append(massage,ignore_index = True)
        return
    t = type(value)
    if t == str:
        try:
            tmp = json.loads(value)
            massage["key"+str(curent_level)] = key
            massage["dt"+str(curent_level)] = "json"
            for k in tmp:
                parse_json(k,tmp[k],curent_level+1,massage)
        except:
            massage["key"+str(curent_level)] = key
            massage["dt"+str(curent_level)] = "str"
            df = df.append(massage,ignore_index = True)
            return
    else:
        if t == list:
            massage["key"+str(curent_level)] = key
            massage["dt"+str(curent_level)] = "list"
            for li in value:
                parse_json(key,li,curent_level+1,massage)
        if t == dict:
            massage["key"+str(curent_level)] = key
            massage["dt"+str(curent_level)] = "dict"
            for k in value:
                parse_json(k,value[k],curent_level+1,massage)
        if t == set:
            massage["key"+str(curent_level)] = key
            massage["dt"+str(curent_level)] = "set"
            for li in value:
                parse_json(key,li,curent_level+1,massage)

        massage["key"+str(curent_level)] = key
        massage["dt"+str(curent_level)] = "simple"
        df = df.append(massage,ignore_index = True)


parse_json("json_file", json_file,0,{})
df.to_excel(r"D:\out.xlsx")