import sys
import json
import codecs
import trunklucator
from jinja2 import Template


#You can change this format in frontend part.
controls = [
        {'label':'society (a)', 'value':'society', 'shortcut':"['a']"}, 
        {'label':'economy (s)', 'value':'economy', 'shortcut':"['s']"}, 
        {'label':'technology (d)', 'value':'technology', 'shortcut':"['d']"}, 
        {'label':'sports (f)', 'value':'sports', 'shortcut':"['f']"}, 
        {'label':'entertainment (h)', 'value':'entertainment', 'shortcut':"['h']"}, 
        {'label':'science (j)', 'value':'science', 'shortcut':"['j']"}, 
        {'label':'other (k)', 'value':'other', 'shortcut':"['k']"},
        {'label':'skip (enter)', 'value':'', 'shortcut':"['enter']"},
        ]


HTML_TEMPLATE = '''
<style type="text/css">
</style>
<div class="columns is-centered content">
    <div class="column is-half">
    <table class="table is-bordered">
      {% for field in fields %}
      <tr>
        <td class="tg-0pky">{{ field }}</td>
        <td class="tg-0pky">{{ data[field] }}</td>
      </tr>
      {% endfor %}
    </table>
    </div>
</div>
'''

template = Template(HTML_TEMPLATE)

filter_fields = set(["article:published_time", "lang", "filename"])

with trunklucator.WebUI(context={'buttons':controls}) as tru: # start http server in background
    for data in map(json.loads, sys.stdin): #read json data from standart input
        fields = [k for k in data.keys() if k not in filter_fields]
        data["label"] = tru.ask({"html": template.render(fields=fields, data=data)})
        print("{}".format(json.dumps(data, ensure_ascii=False)), flush=True) #output result