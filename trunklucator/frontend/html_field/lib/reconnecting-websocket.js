import OnMessage from './onmessage.js';

export default function(self, url, protocols, options) {
    var reconnectAttempts = 0;
    var timer_id;
    const reconnectInterval = 3000;
    const reconnectDecay = 1.5;
    const maxReconnectInterval = 60000;

    function connect() {
        if ('WebSocket' in window) {
            self.websocket = new WebSocket(url, protocols, options);
        } else {
            alert('Sorry, websocket not supported by your browser.')
        }
        //Error callback
        self.websocket.onerror = function(event) {
            console.error("error!", event.reason);
            self.setStatus('Not connected.')
            self.opened = false;
        };
        //socket opened callback
        self.websocket.onopen = function(event) {
            clearTimeout(timer_id)
            self.setStatus('Connected.')
            self.opened = true;
        };
        //message received callback
        self.websocket.onmessage = OnMessage(self)
            //socket closed callback
        self.websocket.onclose = function(event) {
            clearTimeout(timer_id);
            self.opened = false;
            var timeout = reconnectInterval * Math.pow(reconnectDecay, reconnectAttempts);
            timeout = timeout > maxReconnectInterval ? maxReconnectInterval : timeout;
            console.log('Socket is closed. Reconnect will be attempted in ' + timeout + ' second.', event);
            self.setStatus('Reconnecting...');
            timer_id = setTimeout(function() {
                reconnectAttempts++;
                connect();

            }, timeout);
        };
        //when browser window closed, close the socket, to prevent server exception
        window.onbeforeunload = function() {
            self.websocket.close();
        };
    };
    connect();
}