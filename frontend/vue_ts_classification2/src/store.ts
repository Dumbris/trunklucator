import { Task, ServerMsg } from './protocol/types'

export interface State {
    task: Task | null
    reply_id: string | null
}


export interface Store {
    debug: boolean
    readonly state: State
    setTaskAction(task: Task, reply_id: string | null): void
    clearTaskAction(): void
}

export const store: Store = {
  debug: true,
  state: {
    task: null,
    reply_id: null,
  },
  setTaskAction(newValue: Task, reply_id: string) {
    if (this.debug) {console.log('setTaskAction triggered with', newValue)};
    this.state.reply_id = reply_id;
    this.state.task = newValue;
  },
  clearTaskAction() {
    if (this.debug) {console.log('clearTaskAction triggered')};
    this.state.task = null;
  },
};