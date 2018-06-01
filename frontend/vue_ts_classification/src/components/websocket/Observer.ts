import Emitter from './Emitter'

type Opts = {[key:string]: string | number | boolean | WebSocket}

export default class {
  format: string = '';
  connectionUrl: string;
  opts: Opts;
  reconnection: boolean = false
  reconnectionAttempts: number = Infinity
  reconnectionDelay: number = 1000
  reconnectTimeoutId: NodeJS.Timer
  reconnectionCount: number = 0
  store: any
  WebSocket: WebSocket | undefined;

  constructor (connectionUrl: string, opts: Opts = {}) {
    if (opts.format) {
        this.format = String(opts.format).toLowerCase()
    }
    this.connectionUrl = connectionUrl
    this.opts = opts

    this.reconnection = Boolean(this.opts.reconnection) || false
    this.reconnectionAttempts = Number(this.opts.reconnectionAttempts) || Infinity
    this.reconnectionDelay = Number(this.opts.reconnectionDelay) || 1000
    //this.reconnectTimeoutId  = 0
    this.reconnectionCount = 0

    this.connect(connectionUrl, opts)

    if (opts.store) { this.store = opts.store }
    this.onEvent()
  }

  connect (connectionUrl: string, opts: Opts = {}) {
    let protocol: string = String(opts.protocol) || ''
    this.WebSocket = opts.WebSocket || (protocol === '' ? new WebSocket(connectionUrl) : new WebSocket(connectionUrl, protocol))
    if (this.format === 'json') {
      if (!('sendObj' in this.WebSocket)) {
        this.WebSocket.sendObj = (obj) => this.WebSocket.send(JSON.stringify(obj))
      }
    }

    return this.WebSocket
  }

  reconnect () {
    if (this.reconnectionCount <= this.reconnectionAttempts) {
      this.reconnectionCount++
      clearTimeout(this.reconnectTimeoutId)

      this.reconnectTimeoutId = setTimeout(() => {
        if (this.store) { this.passToStore('SOCKET_RECONNECT', this.reconnectionCount) }

        this.connect(this.connectionUrl, this.opts)
        this.onEvent()
      }, this.reconnectionDelay)
    } else {
      if (this.store) { this.passToStore('SOCKET_RECONNECT_ERROR', true) }
    }
  }

  onEvent () {
    ['onmessage', 'onclose', 'onerror', 'onopen'].forEach((eventType) => {
      this.WebSocket[eventType] = (event) => {
        Emitter.emit(eventType, event)

        if (this.store) { this.passToStore('SOCKET_' + eventType, event) }

        if (this.reconnection && eventType === 'onopen') { this.reconnectionCount = 0 }

        if (this.reconnection && eventType === 'onclose') { this.reconnect() }
      }
    })
  }

  passToStore (eventName, event) {
    if (!eventName.startsWith('SOCKET_')) { return }
    let method = 'commit'
    let target = eventName.toUpperCase()
    let msg = event
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
}