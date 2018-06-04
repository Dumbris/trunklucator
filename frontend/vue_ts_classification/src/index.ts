import Vue from "vue";
import HelloComponent from "./components/Hello.vue";
import VueNativeSock from './plugins/websocket/Main';

Vue.use(VueNativeSock, 'ws://localhost:9090', { format: 'json' })

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