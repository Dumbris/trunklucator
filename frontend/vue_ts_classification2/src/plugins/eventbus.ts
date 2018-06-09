import Vue, { PluginObject, VueConstructor } from 'vue';

interface IEventBusOptions {
  eventbus?: Vue
}

export class EventBusPlugin implements PluginObject<{}> {
  private eventbus?: Vue

  public getInstance(): Vue {
    if (!this.eventbus) {throw new Error('Cannot locate event bus object')}
    return this.eventbus
  }

  public install(vue: VueConstructor<Vue>, options?: IEventBusOptions) {
    if (!this.eventbus && (options && options.eventbus)) {
        this.eventbus = options.eventbus
    }
    if (!this.eventbus) {throw new Error('Cannot locate event bus object')}
    vue.prototype.$bus = this.eventbus
  }
}