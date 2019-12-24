export default function(self) {
    return function(event) {
        const msg = JSON.parse(event.data)
        if (("type" in msg) && (msg["type"] == "task")) {
            self.data = msg["payload"]
            var task = {
                    "id": msg["payload"]["task_id"],
                    "data": JSON.stringify(msg["payload"]["x"]["data"]),
                    //"predictions": msg["payload"]["x"]["completions"],
                    "completions": [],
                    //"predictions": msg["payload"]["x"]["predictions"],
                    "predictions": [],
            }
            self.ls.addTask(task)
        }
        if (("type" in msg) && (msg["type"] == "update")) {
            //self.ls.setUpdate(msg["payload"])
            console.log(msg)    
        }
        if (("type" in msg) && (msg["type"] == "stop")) {
            self.ls.addTask({
                "x": {
                    "html": "<h6>No more data on the server.</h6>"
                }
            })
        }
    };
}