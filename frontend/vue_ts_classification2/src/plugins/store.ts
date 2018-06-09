import Vue, { PluginObject, VueConstructor } from 'vue';

interface IStoreOptions {
  store?: any;
}

export class StorePlugin implements PluginObject<{}> {
  private store: object = {}

  public install(vue: VueConstructor<Vue>, options?: IStoreOptions) {
    if (!this.store) {
      this.store = options && options.store ? options.store : {}
    }
    if (!this.store) { throw new Error('Cannot store') }
    vue.prototype.$store = this.store
  }
}
