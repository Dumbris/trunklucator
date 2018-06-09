import Vue, { PluginObject, VueConstructor } from 'vue';

interface ISocketOptions {
  connection?: string
  eventbus?: Vue
}

export class WebSocketPlugin implements PluginObject<{}> {
  private connection: string = ''
  private eventbus?: Vue
  private opened: boolean = false

  public install(vue: VueConstructor<Vue>, options?: ISocketOptions) {
    if (!this.connection) {
      this.connection = options && options.connection ? options.connection : '';
    }
    if (!this.connection) { throw new Error('Cannot locate connection') }

    if (!this.eventbus && (options && options.eventbus)) {
        this.eventbus = options.eventbus
    }
    if (!this.eventbus) {throw new Error('Cannot locate event bus object')}

    vue.prototype.$socket = this.bindWebSocket()
    vue.prototype.$socketplugin = this
  }

  private bindWebSocket(): WebSocket {
    let websocket: WebSocket
    if ('WebSocket' in window) {
        websocket = new WebSocket(this.connection)
    } else {
        throw new Error('Sorry, websocket not supported by your browser.')
    }
    websocket.onerror = (event) => {
        console.error("error!", event)
        this.opened = false
    }

    websocket.onopen = () => {
        this.opened = true
    }
      //socket opened callback
    websocket.onopen = (event) => {
        console.log("websocket opened")
        this.opened = true
    }
      //message received callback
    websocket.onmessage = (event) => {
      let msg: any = JSON.parse(event.data)
      if (("type" in msg) && (msg["type"] == 'task')) {
        console.log(msg["payload"])
        if (this.eventbus) {
            this.eventbus.$emit('servermsg', msg)
        } else {
            throw new Error("Eventbus required")
        }
      }
      if (("type" in msg) && (msg["type"] == "stop")) {
        console.log(msg)
        //websocket.close();
      }
      };
      //socket closed callback
    websocket.onclose = () => {
        console.log("websocket closed");
        this.opened = false;
      };
      // when browser window closed, close the socket, to prevent server exception
    (window as any as Window).onbeforeunload = () => {
        websocket.close()
      };
    return websocket
  }
}
