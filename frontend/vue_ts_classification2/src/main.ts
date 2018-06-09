import Vue from 'vue'
import App from './App.vue'
import { WebSocketPlugin } from '@/plugins/websocket'
import { EventBusPlugin } from '@/plugins/eventbus'
import { store } from './store'
import { EventBus } from './eventbus'

Vue.config.productionTip = false

const apiUrl = 'ws://localhost:8085/echo/v1.0'
//Create connector
Vue.use(new EventBusPlugin(), { eventbus: EventBus })
Vue.use(new WebSocketPlugin(), { connection: apiUrl, eventbus: EventBus })
EventBus.$on('servermsg', (data) => {
  console.log(`Oh, that's nice. It's gotten ${data} ! :)`, data)
});

new Vue({
  render: (h) => h(App),
  data: {
    sharedState: store.state
  }
}).$mount('#app')
