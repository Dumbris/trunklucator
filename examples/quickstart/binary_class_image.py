from trunklucator import WebUI

title = "Dog / Cat"

images = [
    "10005.jpg",
    "10006.jpg",
    "10038.jpg",
    "10039.jpg",
    "10082.jpg",
    "10083.jpg",
    "10127.jpg",
    "10128.jpg",
    "10172.jpg",
    "10173.jpg",
]

controls = [
            {'label':'Cat (a)', 'value':'cat', 'shortcut':"['a']"}, 
            {'label':'Dog (x)', 'value':'dog', 'shortcut':"['x']"}, 
            {'label':'Skip (enter)', 'value':'', 'shortcut':"['enter']"}, 
        ]

def img_tag(filename):
    return "<img src=\"/data/{}\">".format(filename)

with WebUI(data_dir='./images', context={'buttons':controls, 'title':title}) as tru: # start http server in background
    for item in images:
        label = tru.ask({"html": img_tag(item)})
        print("image: {}, label: {}".format(item, label.y)) #output result
