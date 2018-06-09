import Vue, { ComponentOptions } from 'vue'

declare module 'vue/types/vue' {
  interface Vue {
    $sharedState: object;
  }
}