Trunklucator is a python module for data scientists and ML practitioners for quick creating annotation projects and testing your ideas. It acts like a python's native input() function, but support displaying rich content and advance interaction with the user (using a web browser). Trunklucator lets you easily plug interaction with a human to your model prototype.

## Example
```python
from trunklucator import WebUI

with WebUI() as webui: # start http server in background
    for item in data: 
        y = webui.ask(item) #<- wait for user action on web page
        print(y) 
```

For full example see `examples/images` directory

Trunklucator is the best when you need to represent complex data like image, formatted text, video or sound to the user and ask the user to label/annotate this data. After a user's action, you immediately are able to use this data in your pipeline.  Trunklucator works well together with active learning (see `examples/active_learning`).

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
with WebUI(host='192.168.0.30', port=8080, data_dir='./data', fronend_dir='./myfront')
```

## API methods

For instance of WebUI class:

* `.ask(data, meta(optional))` - by calling this method you will stop the execution of your code until the user action in a web browser. 
* `.update(data)` - asynchronously publish information to the frontend part.

## Running examples

1. clone github repo
1. cd to examples/
1. run start.sh, open browser on http://localhost:8086


## How to display complex data

Trunklucator contains two parts: python module which runs a small HTTP server in the background thread and simple javascript single page application (frontend). These parts interact with each other using WebSocket. You don't need to change the python part it's ready to use abstraction.
JavaScript part designed like hackable part, you can adjust it for your specific data format.  The default implementation of frontend can load arbitrary HTML code. UI controls can be configured in python code. 

To customize frontend part: 

1. clone github repo
1. Make a copy of trunklucator/frontend/html_field directory. Implementation is simple and doesn't use tools like npm, webpack, etc.
1. You can edit it on disk and after refreshing web page, you will see the results. Use FRONTEND_DIR environment variable to setup path to your custom frontend.


