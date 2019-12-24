export default function(self) {
    return function(decision) {
            var sol = {
                "type": "solution",
                "payload": {
                    "task_id": self.data["task_id"],
                    "y": decision
                },
                "reply_id": null,
                "msg_id": "v1"
            }
            self.websocket.send(JSON.stringify(sol))
    }
}
