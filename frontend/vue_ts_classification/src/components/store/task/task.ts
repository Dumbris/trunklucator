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
        getSampleIds(state: TaskState) {
            return state.items.map((item) => item.sample.data);
        },

        getSamplesByStatus(state: TaskState) {
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

        setTotalSolved(state: TaskState, totalSolved: number) {
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

            const availableSampleIds = readSampleIds(context);
            commitSolveSamples(context, availableSampleIds);
        },

        async updateSolvedAmount(context: TaskContext): Promise<void> {
            // Imagine this is a server API call to figure out which items are available:
            await new Promise((resolve, _) => setTimeout(() => resolve(), 500));

            const availableSamples = readSamplesByStatus(context)(true);
            commitSetSolvedAmount(context, availableSamples.length);
        },

        async SelectAvailablieItemsAndUpdateTotalAmount(context: TaskContext, discount: number): Promise<void> {
            await dispatchSelectAvailableItems(context);
            await dispatchUpdateSolvedAmount(context);
        },
    },
};

const { commit, read, dispatch } =
     getStoreAccessors<TaskState, RootState>("task");

const getters = task.getters;

export const readSampleIds = read(getters.getSampleIds);
export const readSamplesByStatus = read(getters.getSamplesByStatus);

const actions = task.actions;

export const dispatchUpdateSolvedAmount = dispatch(actions.updateSolvedAmount);
export const dispatchSelectAvailableItems = dispatch(actions.selectAvailableItems);
export const dispatchSelectAvailablieItemsAndUpdateTotalAmount =
    dispatch(actions.SelectAvailablieItemsAndUpdateTotalAmount);

const mutations = task.mutations;

export const commitReset = commit(mutations.reset);
export const commitAppendItem = commit(mutations.appendItem);
export const commitSetSolvedAmount = commit(mutations.setTotalSolved);
export const commitSolveSamples = commit(mutations.solveSamples);