from trunklucator import WebUI

title = "News classification"

news_titles = [
    "Half of all older adults are worried about dementia, survey says",
    "Telus invests $500,000 to bring wireless service to First Nation’s community in B.C.",
    "Asteroid Bigger Than the Eiffel Tower Approaching Earth at 20 Times the Speed of Sound",
    "Night shift: Bottas beats Vettel by 0.012s for pole as Hamilton starts in P5",
    "Exclusive: John Barnes discusses Liverpool FC’s January transfer plans",
    "Maharashtra: Balasaheb, Pawar relation beyond politics",
    "Which words has Collins Dictionary included in its Brexicon?",
    "Paralympics: Australian cycling champion Modra killed in road collision",
    "Multistate salmonella outbreak causes one death: CDC",
]


#You can change this format in frontend part.
controls = [
        {'label':'economy (s)', 'value':'economy', 'shortcut':"['s']"}, 
        {'label':'technology (d)', 'value':'technology', 'shortcut':"['d']"}, 
        {'label':'sports (f)', 'value':'sports', 'shortcut':"['f']"}, 
        {'label':'other (k)', 'value':'other', 'shortcut':"['k']"},
        {'label':'skip (enter)', 'value':'skip', 'shortcut':"['enter']"},
        ]


with WebUI(context={'buttons':controls, 'title':title}) as tru: # start http server in background
    for item in news_titles:
        label = tru.ask({"html": item})
        print("data: {}, label: {}".format(item, label.y)) #output result