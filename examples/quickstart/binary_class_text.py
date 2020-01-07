from trunklucator import WebUI

title = "Twitter sentiment"

data = [
    "Feeeling like shit right now. I really want to sleep, but nooo I have 3 hours of dancing and an art assignment to finish.", 
    "i get off work sooooon! i miss cody booo. haven't seen him in foreverr!", 
    "I miss New Jersey",
    "I wanted to sleep in this morning but a mean kid through a popsicle stick at me head. I wish I could fly away like those squirrels"
    ]        

controls = [
            {'label':'Positive (a)', 'value':1, 'shortcut':"['a']"}, 
            {'label':'Negative (x)', 'value':0, 'shortcut':"['x']"}, 
            {'label':'Skip (enter)', 'value':-1, 'shortcut':"['enter']"}, 
        ]


with WebUI(context={'buttons':controls, 'title':title}) as tru: # start http server in background
    for item in data:
        label = tru.ask({"html": item})
        print("data: {}, label: {}".format(item, label.y)) #output result