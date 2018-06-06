import Vue from "vue";

import { getStoreBuilder } from "vuex-typex"
import Vuex, { Store, ActionContext } from "vuex"
import HelloComponent from "./components/Hello.vue";
import VueNativeSock from './plugins/websocket/Main';

const api_url = 'ws://localhost:8085/echo/v1.0';
Vue.use(VueNativeSock, api_url, { format: 'json' })
Vue.use(Vuex)


export interface RootState { basket: TaskState }
export interface TaskState { items: Item[] }
export interface Item { id: string, name: string }

const storeBuilder = getStoreBuilder<RootState>()
const moduleBuilder = storeBuilder.module<TaskState>("task", { items: [] })

namespace basket
{
    const appendItemMutation = (state: BasketState, payload: { item: Item }) => state.items.push(payload.item)
    const delayedAppendAction = async (context: ActionContext<BasketState, RootState>) =>
    {
        await delay(1000)
        basket.commitAppendItem({ item: { id: "abc123", name: "ABC Item" } })
    }

    export const commitAppendItem = moduleBuilder.commit(appendItemMutation)
    export const dispatchDelayedAppend = moduleBuilder.dispatch(delayedAppendAction)
}
export default basket

/// in the main app file
const storeBuilder = getStoreBuilder<RootState>()


let v = new Vue({
    el: "#app",
    template: `
    <div>
        <div>Hello {{name}}!</div>
        Name: <input v-model="name" type="text">
        <hello-component :name="name" :initialEnthusiasm="5" />
    </div>`,
    store: storeBuilder.vuexStore(),
    data: {
        name: "World"
    },
    components: {
        HelloComponent
    }
});