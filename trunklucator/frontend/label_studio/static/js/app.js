    import ReconnectingWebSocket from './reconnecting-websocket.js';
    const self = window
    const URL = "ws://" + location.host + "/trunklucator/v1.0"

    self.send = function (decision) {
            var sol = {
                "type": "solution",
                "payload": {
                    "task_id": self.data["task_id"],
                    "y": decision
                },
                "reply_id": null,
                "msg_id": "v1"
            }

            const to_send = JSON.stringify(sol);
            self.websocket.send(to_send)
        };

    self.setStatus = function (status) {
        console.log(status)
    }

    window.onload = function () {
            // Label stream mode
            self.ls = new LabelStudio("label-studio", {
                config: `
                    <View>
                    <HyperText name="dialog" value="$html"></HyperText>
                    <Header value="Rate last answer:"></Header>
                    <Choices name="chc-1" choice="single-radio" toName="dialog" showInline="true">
                        <Choice value="Bad answer"></Choice>
                        <Choice value="Neutral answer"></Choice>
                        <Choice value="Good answer"></Choice>
                    </Choices>
                    <Header value="Your answer:"></Header>
                    <TextArea name="answer"></TextArea>
                    </View>
                    `,
                expert: {"pk": 1, "firstName": "Label", "lastName": "Expert"},
                explore: false, // label stream mode (task by task)
                project: { id: 1 },
                interfaces: [
                    "basic",
                    "load",  // load next task automatically (label stream mode)
                    //"panel",  // undo, redo, reset panel
                    "controls",  // all control buttons: skip, submit, update
                    "submit",  // submit button on controls
                    "predictions", // show predictions from task.predictions = [{...}, {...}]
                    "completions",  // show completions
                    //"side-column" // entity
                ],
                apiCalls: false,
                debug: true,
                submitCompletion: function(result) {
                    console.log(result)
                    self.send(result)
                    self.ls.markLoading(false)
                },
                onLabelStudioLoad: function() {

                    //console.log(result)
                    console.log("loaded")
                    ReconnectingWebSocket(self, URL)
                },
                task: {
                    completions: [],
                    predictions: [],
                    id: 1,
                    data: {
                        html: "!!!!"
                    }
                }   
            });
    }
