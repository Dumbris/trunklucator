import json
from trunklucator import WebUI

texts = ["""Alphabet Inc. is an American multinational conglomerate headquartered in Mountain View, California. It was created through a corporate restructuring of Google on October 2, 2015,[2] and became the parent company of Google and several former Google subsidiaries.[3][4][5] The two founders of Google assumed executive roles in the new company, with Larry Page serving as CEO and Sergey Brin as president.[6] Alphabet is the world's fifth-largest technology company by revenue and one of the world's most valuable companies.[7][8]
The establishment of Alphabet was prompted by a desire to make the core Google internet services business "cleaner and more accountable" while allowing greater autonomy to group companies that operate in businesses other than Internet services.[4][9] Page and Brin announced their resignation from their executive posts in December 2019, with the CEO role to be filled with Sundar Pichai, also the CEO of Google. Page and Brin will remain controlling shareholders of Alphabet, Inc.[10]
""",
"""On August 10, 2015, Google Inc. announced plans to create a new public holding company, Alphabet Inc. Google CEO Larry Page made this announcement in a blog post on Google's official blog.[11] Alphabet would be created to restructure Google by moving subsidiaries from Google to Alphabet, narrowing Google's scope. The company would consist of Google as well as other businesses including X Development, Calico, Nest, Verily, Malta, Fiber, Makani, CapitalG, and GV.[6][12][13] Sundar Pichai, Product Chief, became the new CEO of Google, replacing Larry Page, who transitioned to the role of running Alphabet, along with Google co-founder Sergey Brin.[14][15]
"""
]

CONFIG ='''
<View>
  <Labels name="ner" toName="text">
    <Label value="Person"></Label>
    <Label value="Organization"></Label>
    <Label value="Date"></Label>
    <Label value="Location"></Label>
  </Labels>
  <Text name="text" value="$text"></Text>
</View>
'''
INTERFACES = ["basic", "load", "controls", "submit", "completions", "side-column"]

with WebUI(frontend_dir='label_studio', context={"label_studio":{"config":CONFIG, "interfaces":INTERFACES}}) as tru: # start http server in background
    for data in texts:
        completions = tru.ask({"data": {"text": data}})
        print("{}".format(json.dumps(completions, ensure_ascii=False)), flush=True) #output result
