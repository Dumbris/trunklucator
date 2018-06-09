export class MessageRouter {
    private websocket: WebSocket
    constructor(websocket: WebSocket) {
        this.websocket = websocket
    }
}