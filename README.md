## InteractiveLabeler (Work in progress)

This repository is a prototype of a component for interaction with the user during an active learning session.


## Example of usage

```

X = data()
y = labels()

with InteractiveLabeler(label_name, type=MULTYCLASS) as labeler: #localhost:8085 become available here
    for i in range(10):
        X_ = UncertaintySampling(X,y_pred)
        y_ = labeler.ask(X_) #ask human here
        model.fit(X_,y_)
```

See `examples\20newsgroups.py` for detailed example.

### Back-end <-> Frontend protocol

#### Common structure

{"type": [ task | solution | update | stop ]
"id": uuid
"data": [X, y, label_name]
"version": "1.0"
}

#### Types
* task, id (push from server, or reply to update request)
* solution, id (client post)
* update (client request)
* stop (push from server, user pressed ctrl+C)


#### TODO

1) Figure out how to test current aiohttp version (latest in pip 3.0.0b1) - Upgrade to Python 3.6 (Done)

2) Do we need a json-schema for validation?
http://json-schema.org/implementations.html#validator-python
https://www.jsonschema.net/
https://github.com/aromanovich/jsl
https://github.com/Julian/jsonschema