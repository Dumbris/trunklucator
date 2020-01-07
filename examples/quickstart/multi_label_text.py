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



LABEL_STUDIO_CONFIG ='''<View>
                    <Text name="post" value="$text"></Text>
                    <Choices name="label" toName="title" choice="multiple">
                        <Choice value="Economy"></Choice>
                        <Choice value="Technology"></Choice>
                        <Choice value="Sports"></Choice>
                        <Choice value="Science"></Choice>
                        <Choice value="Entertainment"></Choice>
                        <Choice value="Other"></Choice>
                    </Choices>
                    </View>'''

with WebUI(frontend_dir='label_studio', context={"label_studio":{"config":LABEL_STUDIO_CONFIG}, 'title':title}) as tru: # start http server in background
    for item in news_titles:
        label = tru.ask({"data": {"text": item}})
        print("data: {}, label: {}".format(item, label)) #output result