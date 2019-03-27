import sys
import trunklucator
import json

#You can change this format in frontend part.
#Current format - (label text, returning value, key code for shortcut)
META = {"buttons":[('Cat (A)', 1, 65), ('Dog (X)', 0, 88), ('Skip (Enter)', -1, 13)]}


with trunklucator.WebUI(data_dir="./data") as tru: # start http server in background
    for data in map(json.loads, sys.stdin): #read json data from standart input
        y = tru.ask(data, META) #<- wait for user action on web page
        print("{}".format(json.dumps({"file":data["file"], "is_cat": y}))) #output result

