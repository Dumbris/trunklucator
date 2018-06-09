export interface Task {
    task_id: string
    x: any
    label_name: string[]
    title: string
    label_type: string
    y: any
}

export interface ServerMsg {
    type: string
    payload: any
    reply_id: string | null
    msg_id: string | null
}
