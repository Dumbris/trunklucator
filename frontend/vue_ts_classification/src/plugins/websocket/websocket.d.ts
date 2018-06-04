//import WebSocketPlugin from "./Main";
import Vue, { ComponentOptions } from 'vue'

declare module 'vue/types/vue' {
  interface Vue {
    $socket: WebSocket;
  }
}

declare module 'vue/types/options' {
  interface ComponentOptions<V extends Vue> {
    sockets?: {[key:string]: () => void};
  }
}