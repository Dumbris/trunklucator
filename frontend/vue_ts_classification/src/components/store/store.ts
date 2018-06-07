import * as Vuex from "vuex";
import { task } from "./task";
import { State } from "./state";

export const createStore = () => new Vuex.Store<State>({
    modules: {
        task,
    },
});