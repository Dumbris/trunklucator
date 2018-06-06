import Vue from "vue";
import HelloComponent from "./components/Hello.vue";
import VueNativeSock from './plugins/websocket/Main';

const api_url = 'ws://localhost:8085/echo/v1.0';
Vue.use(VueNativeSock, api_url, { format: 'json' })

let v = new Vue({
    el: "#app",
    template: `
    <div>
        <div>Hello {{name}}!</div>
        Name: <input v-model="name" type="text">
        <hello-component :name="name" :initialEnthusiasm="5" />
    </div>`,
    data: {
        name: "World"
    },
    components: {
        HelloComponent
    }
});