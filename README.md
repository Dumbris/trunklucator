Trunklucator is a python module for data scientists and ML practitioners for quick creating annotation projects and testing your ideas. It acts like a python's native input() function, but support displaying rich content and advance interaction with the user (using a web browser). Trunklucator lets you easily plug interaction with a human to your model prototype.

## Example
```python
from trunklucator import WebUI

with WebUI() as webui: # start http server in background
    for item in data: 
        y = webui.ask(item) #<- wait for user action on web page
        print(y) 
```

For full examples see `examples/quickstart` directory


| Task | Screenshot | Example code |
| :---         |     :---:      |          :--- |
| binary classification   | <a href="/screenshots/images_classification.png?raw=true"><img src="/screenshots/images_classification.png?raw=true" align="left" height="48" width="48"></a><br><a href="/screenshots/binary_class_text.png?raw=true"><img src="/screenshots/binary_class_text.png?raw=true" align="left" height="48" width="48"></a>    | For images - [examples/quickstart/binary_class_image.py](examples/quickstart/binary_class_image.py)<br>For text - [examples/quickstart/binary_class_text.py](examples/quickstart/binary_class_text.py)    |
| multiclass classification  | <a href="/screenshots/multi_class_text.png?raw=true"><img src="/screenshots/multi_class_text.png?raw=true" align="left" height="48" width="48"></a>       | [examples/quickstart/multi_class_text.py](examples/quickstart/multi_class_text.py)      |
| multilabel classification  | <a href="/screenshots/multi_label_text2.png?raw=true"><img src="/screenshots/multi_label_text2.png?raw=true" align="left" height="48" width="48"></a>       | [examples/quickstart/multi_label_text.py](examples/quickstart/multi_label_text.py)      |
| Named Entity Recognition (NER)  | <a href="/screenshots/ner_text.png?raw=true"><img src="/screenshots/ner_text.png?raw=true" align="left" height="48" width="48"></a>       | [examples/quickstart/ner_text.py](examples/quickstart/ner_text.py)      |
| HTML page annotation | <a href="/screenshots/ner_html.png?raw=true"><img src="/screenshots/ner_html.png?raw=true" align="left" height="48" width="48"></a>       | [examples/quickstart/ner_html.py](examples/quickstart/ner_html.py)      |


Trunklucator is the best when you need to represent complex data like image, formatted text, video or sound to the user and ask the user to label/annotate this data. After a user's action, you immediately are able to use this data in your pipeline.  Trunklucator works well together with active learning (see example [examples/pytorch_active_learning/](examples/pytorch_active_learning/)).

## Installation

```
pip install trunklucator
```

## Settings

You can use environmet variable to change default parameters
* HOST - bind to host (default 127.0.0.1)
* PORT - use port number (default 8086)
* DATA_DIR - directory will be available through HTTP by path /data 
* FRONTEND_DIR - directory path to your custom frontend

```bash
PORT=8080 python3 main.py
```

Also, you can use similar parameters in code then instanciate trunklucator.WebUI class.

```bash
with WebUI(host='0.0.0.0', port=8080, data_dir='./data', frontend_dir='./myfront')
```

## API methods

For instance of WebUI class:

* `.ask(data, meta(optional))` - by calling this method you will stop the execution of your code until the user action in a web browser. 
* `.update(data)` - asynchronously publish information to the frontend part.

## Running examples

1. clone github repo
1. cd to examples/
1. run python3 filename.py, open browser on http://localhost:8086


## How to display complex data

Trunklucator contains two parts: python module which runs a small HTTP server in the background thread and frontend - it could be any javascript single page application that supports simple protocol for fetching task data. 
These parts interact with each other using HTTP  or WebSocket. You don't need to change the python part it's ready to use abstraction. 
You can select which frontend part to use by setting `frontend_dir` WebUI init parameter or using environment variable FRONTEND_DIR
You can set path to your custom frontend directory or use predefined names for frontends integrated into python package.

In the current version there are two frontend integrated:

1. Default `WebUI(frontend_dir='html_field')` designed like hackable part, you can adjust it for your specific data format. The default implementation is able to load arbitrary HTML text. UI controls can be configured in python code.
1. `WebUI(frontend_dir='label_studio')` - advanced frontend with a support a lot of data types. For more information check the official site https://labelstud.io/ and example/quickstart/ner_text.py


To customize default frontend part: 

1. clone github repo
1. Make a copy of trunklucator/frontend/html_field directory. Implementation is simple and doesn't use tools like npm, webpack, etc.
1. You can edit it on disk and after refreshing web page, you will see the results. Use FRONTEND_DIR environment variable to setup path to your custom frontend.


