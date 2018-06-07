import Vue from "vue";

import Vuex, { Store, ActionContext } from "vuex"
import { createStore } from "./components/store/store"
import HelloComponent from "./components/Hello.vue";
import VueNativeSock from './plugins/websocket/Main';

const api_url = 'ws://localhost:8085/echo/v1.0';
Vue.use(VueNativeSock, api_url, { format: 'json' })
Vue.use(Vuex)


export interface RootState { basket: TaskState }
export interface TaskState { items: Item[] }
export interface Item { id: string, name: string }


let v = new Vue({
    el: "#app",
    template: `
    <div>
        <div>Hello {{name}}!</div>
        Name: <input v-model="name" type="text">
        <hello-component :name="name" :initialEnthusiasm="5" />
    </div>`,
    store: createStore(),
    data: {
        name: "World"
    },
    components: {
        HelloComponent
    }
});