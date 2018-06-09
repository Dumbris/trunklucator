import Vue, { ComponentOptions } from 'vue'

declare type Bus = Vue //TODO make it visiable in eventbus.ts

declare module 'vue/types/vue' {
  interface Vue {
    $bus: Bus;
  }
}