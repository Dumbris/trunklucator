import * as Vuex from "vuex";
import { basket } from "./task";
import { State } from "./state";

export const createStore = () => new Vuex.Store<State>({
    modules: {
        basket,
    },
});