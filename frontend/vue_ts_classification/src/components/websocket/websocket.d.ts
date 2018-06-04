import { WebSocketPlugin } from "./Main";

declare module 'vue/types/vue' {
  interface Vue {
    $options2: WebSocket;
  }
}