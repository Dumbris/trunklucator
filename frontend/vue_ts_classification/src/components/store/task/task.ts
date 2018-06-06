import { ActionContext, Store } from "vuex";
import { getStoreAccessors } from "vuex-typescript";
import { State as RootState } from "../state";
import { TaskState, Sample, SampleInTask } from "./taskState";

type TaskContext = ActionContext<TaskState, RootState>;

export const task = {
    namespaced: true,

    state: {
        items: [],
        totalAmount: 0,
    },

    getters: {
        getSampleNames(state: TaskState) {
            return state.items.map((item) => item.sample.data);
        },

        getItemsByStatus(state: TaskState) {
            return (status: boolean) => state.items.filter((item) => item.isSolved === status);
        },
    },

    mutations: {
        reset(state: TaskState) {
            state.items = [];
            state.totalSolved = 0;
        },

        appendItem(state: TaskState, item: { sample: Sample }) {
            state.items.push({ sample: item.sample, isSolved: false, solution: 0 });
        },

        setTotalAmount(state: TaskState, totalSolved: number) {
            state.totalSolved = totalSolved;
        },

        solveSamples(state: TaskState, sampleIds: number[]) {
            for (const sampleId of sampleIds) {
                state.items.find((item) => item.sample.id === sampleId)!.isSolved = true;
            }
        },
    },

    actions: {
        async selectAvailableItems(context: TaskContext): Promise<void> {
            // Imagine this is a server API call to figure out which items are available:
            await new Promise((resolve, _) => setTimeout(() => resolve(), 500));

            const availableSampleNames = readSampleNames(context);
            commitSolveSamples(context, availableSampleNames);
        },

        async SelectAvailablieItemsAndUpdateTotalAmount(context: TaskContext, discount: number): Promise<void> {
            await dispatchSelectAvailableItems(context);
            await dispatchUpdateTotalAmount(context, discount);
        },
    },
};

const { commit, read, dispatch } =
     getStoreAccessors<TaskState, RootState>("task");

const getters = task.getters;

export const readSampleNames = read(getters.getSampleNames);
export const readItemsByStatus = read(getters.getItemsByStatus);
export const readTotalAmountWithoutDiscount = read(getters.getTotalAmountWithoutDiscount);

const actions = task.actions;

export const dispatchUpdateTotalAmount = dispatch(actions.updateTotalAmount);
export const dispatchSelectAvailableItems = dispatch(actions.selectAvailableItems);
export const dispatchSelectAvailablieItemsAndUpdateTotalAmount =
    dispatch(actions.SelectAvailablieItemsAndUpdateTotalAmount);

const mutations = task.mutations;

export const commitReset = commit(mutations.reset);
export const commitAppendItem = commit(mutations.appendItem);
export const commitSetTotalAmount = commit(mutations.setTotalAmount);
export const commitSelectSamples = commit(mutations.selectSamples);