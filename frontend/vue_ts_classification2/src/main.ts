import Vue from 'vue'
import App from './App.vue'
import { WebSocketPlugin } from '@/plugins/websocket'
import { EventBusPlugin } from '@/plugins/eventbus'
import { StorePlugin } from '@/plugins/store'
import { store } from './store'
import { EventBus } from './eventbus'
import { MessageRouter } from './message-router'

Vue.config.productionTip = false

const apiUrl = 'ws://localhost:8085/echo/v1.0'
//Create connector
const msgRouter = new MessageRouter(EventBus, store)
Vue.use(new EventBusPlugin(), { eventbus: EventBus })
Vue.use(new StorePlugin(), { store: store })
Vue.use(new WebSocketPlugin(), { connection: apiUrl, eventbus: EventBus })

new Vue({
  render: (h) => h(App),
  data: {
    sharedState: store.state
  }
}).$mount('#app')
