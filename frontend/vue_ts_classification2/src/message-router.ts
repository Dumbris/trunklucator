import Vue from 'vue'
import { Task, ServerMsg } from './protocol/types'
import { Store } from './store'


export class MessageRouter {
    private eventbus: Vue
    private store: Store
    constructor(eventbus: Vue, store: Store) {
        this.eventbus = eventbus
        this.eventbus.$on('servermsg', (data: any) => this.onservermsg(data));
        this.store = store
    }
    private onservermsg(msg: ServerMsg) {
        if ('type' in msg && (msg.type === 'task')) {
            this.store.setTaskAction(msg.payload, msg.reply_id)
            return this
        }
        if ('type' in msg && (msg.type === 'stop')) {
            this.store.clearTaskAction()
            return this
        }

    }
}