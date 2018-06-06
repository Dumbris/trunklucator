import Emitter from './Emitter'

type Opts = {[key:string]: string | number | boolean | WebSocket}

export default class {
  format: string = '';
  connectionUrl: string;
  opts: Opts;
  reconnection: boolean = false
  reconnectionAttempts: number = Infinity
  reconnectionDelay: number = 1000
  reconnectTimeoutId: number = 0
  reconnectionCount: number = 0
  store: any
  websocket!: WebSocket;

  constructor (connectionUrl: string, opts: Opts = {}) {
    if (opts.format) {
        this.format = String(opts.format).toLowerCase()
    }
    this.connectionUrl = connectionUrl
    this.opts = opts

    this.reconnection = Boolean(this.opts.reconnection) || false
    this.reconnectionAttempts = Number(this.opts.reconnectionAttempts) || Infinity
    this.reconnectionDelay = Number(this.opts.reconnectionDelay) || 1000
    this.reconnectTimeoutId  = 0
    this.reconnectionCount = 0

    this.connect(connectionUrl, opts)

    if (opts.store) { this.store = opts.store }
    this.onEvent()
  }

  connect (connectionUrl: string, opts: Opts = {}) {
    this.websocket = new WebSocket(connectionUrl)
    if (this.format === 'json') {
      if (!('sendObj' in this.websocket)) {
        (this.websocket as any as WebSocket).sendObj = (obj: Object): void => this.websocket.send(JSON.stringify(obj)) //WTF as any?
      }
    }

    return this.websocket
  }

  reconnect () {
    if (this.reconnectionCount <= this.reconnectionAttempts) {
      this.reconnectionCount++
      clearTimeout(this.reconnectTimeoutId)

      this.reconnectTimeoutId = window.setTimeout(() => {
        //if (this.store) { this.passToStore('SOCKET_RECONNECT', this.reconnectionCount) }
        console.log("RECONNECT")

        this.connect(this.connectionUrl, this.opts)
        this.onEvent()
      }, this.reconnectionDelay)
    } else {
      //if (this.store) { this.passToStore('SOCKET_RECONNECT_ERROR', true) }
        console.error("RECONNECT_ERROR")
    }
  }

  onEvent () {
    this.websocket.onmessage = (event: MessageEvent) => {
      Emitter.emit('onmessage', event)
    }
    this.websocket.onopen = (event: Event) => {
        if (this.reconnection) { this.reconnectionCount = 0 }
    }
    this.websocket.onclose = (event: Event) => {
        if (this.reconnection) { this.reconnect() }
    }
    this.websocket.onerror = (event: Event) => {
      console.error(event)
    }
  }

  //TODO Refactoring
  /*
  passToStore (eventName: string, event: MessageEvent) {
    if (!eventName.startsWith('SOCKET_')) { return }
    let method = 'commit'
    let target = eventName.toUpperCase()
    let msg = event as MessageEvent
    if (this.format === 'json' && event.data) {
      msg = JSON.parse(event.data)
      if (msg.mutation) {
        target = [msg.namespace || '', msg.mutation].filter((e) => !!e).join('/')
      } else if (msg.action) {
        method = 'dispatch'
        target = [msg.namespace || '', msg.action].filter((e) => !!e).join('/')
      }
    }
    this.store[method](target, msg)
  }
  */
}