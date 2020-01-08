import ReconnectingWebSocket from './lib/reconnecting-websocket.js';

import 'https://unpkg.com/vue-shortkey'

Vue.use(window.VueShortkey, { prevent: ['input', 'textarea'] })

const wsVue = new Vue({
    el: '#app',
    delimiters: ['[[' , ']]'],
    data: {
        reply: '',
        data: {
            x: {},
            meta: {}
        },
        update: '',
        status: 'not connected'
    },
    computed: {
        buttons: function() {
            return (this.data.meta || {}).buttons || [
                ["Skip", -1, 13]
            ]
        }
    },
    created() {
        const self = this
            // This code will run on startup
        self.websocket = null

        const URL = "ws://" + location.host + "/trunklucator/v1.0"
        ReconnectingWebSocket(self, URL)

        //attache keyup event listener
        /** 
        window.addEventListener('keyup', function(event) {
            self.buttons.forEach(function(element) {
                if (event.keyCode == element[2]) {
                    self.send(element[1])
                }
            })
        });
        */
    },

    methods: {
        send(decision) {
            var sol = {
                "type": "solution",
                "payload": {
                    "task_id": this.data["task_id"],
                    "y": decision
                },
                "reply_id": null,
                "msg_id": "v1"
            }

            const to_send = JSON.stringify(sol);
            this.websocket.send(to_send)
        },
        setStatus(data) {
            this.status = data
        },
        setUpdate(data) {
            this.update = data
        },
        setTask(task_data) {
            this.data = task_data
        }
    },
});