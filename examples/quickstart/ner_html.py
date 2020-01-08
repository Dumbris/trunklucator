import urllib.request
import json
from trunklucator import WebUI

#Get wiki pages from internet
urls = [
    'https://en.wikipedia.org/w/index.php?title=Alphabet_Inc.&printable=yes',
    'https://en.wikipedia.org/w/index.php?title=Facebook&printable=yes',
    'https://en.wikipedia.org/w/index.php?title=Amazon_(company)&printable=yes'
]

def get_html(url):
    with urllib.request.urlopen(url) as f:
        return f.read().decode('utf-8')

htmls = [get_html(url) for url in urls]        

CONFIG ='''
<View>
  <Labels name="ner" toName="text">
    <Label value="Person"></Label>
    <Label value="Organization"></Label>
    <Label value="Date"></Label>
    <Label value="Location"></Label>
  </Labels>
  <HyperText name="text" value="$text"></HyperText>
</View>
'''
INTERFACES = ["basic", "load", "controls", "submit", "completions", "side-column"]

with WebUI(frontend_dir='label_studio', context={"label_studio":{"config":CONFIG, "interfaces":INTERFACES}}) as tru: # start http server in background
    for html in htmls:
        completions = tru.ask({"data": {"text": html}})
        print("{}".format(json.dumps(completions, ensure_ascii=False)), flush=True) #output result
