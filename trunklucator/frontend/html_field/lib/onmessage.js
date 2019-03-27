export default function(self) {
    return function(event) {
        const msg = JSON.parse(event.data)
        if (("type" in msg) && (msg["type"] == "task")) {
            self.setTask(msg["payload"])
        }
        if (("type" in msg) && (msg["type"] == "update")) {
            self.setUpdate(msg["payload"])
        }
        if (("type" in msg) && (msg["type"] == "stop")) {
            self.setTask({
                "x": {
                    "html": "<h6>No more data on the server.</h6>"
                }
            })
        }
    };
}