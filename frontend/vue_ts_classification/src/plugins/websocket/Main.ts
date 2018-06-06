import Observer from './Observer'
import Emitter from './Emitter'
//import _Vue, { PluginObject } from "vue";
import Vue, { PluginObject, VueConstructor } from 'vue';

interface IOptions {
  name?: string
}

const WebSocketPlugin: PluginObject<any> = {

 install (vue: VueConstructor, connection: string, opts = {}) {
    if (!connection) { throw new Error('[vue-native-socket] cannot locate connection') }

    let observer: Observer

    if (opts.connectManually) {
      Vue.prototype.$connect = () => {
        observer = new Observer(connection, opts)
        Vue.prototype.$socket = observer.websocket
      }

      Vue.prototype.$disconnect = () => {
        if (observer && observer.reconnection) { observer.reconnection = false }
        if (Vue.prototype.$socket) {
          Vue.prototype.$socket.close()
          delete Vue.prototype.$socket
        }
      }
    } else {
      observer = new Observer(connection, opts)
      Vue.prototype.$socket = observer.websocket
    }

    Vue.mixin({
      created () {
        //let vm = this
        const vm: Vue = this as Vue;
        let sockets = vm.$options.sockets

        vm.$options.sockets = new Proxy({} as any, {
          set (target, key, value) {
            Emitter.addListener(key, value, vm)
            target[key] = value
            return true
          },
          deleteProperty (target, key) {
            if ((vm.$options.sockets) && (key in vm.$options.sockets)) {
              Emitter.removeListener(key, vm.$options.sockets[key], vm)
            }
            delete target.key
            return true
          }
        })

        if (sockets) {
          Object.keys(sockets).forEach((key) => {
            if ((vm.$options.sockets) && (sockets)) {//WTF required to fix error message in ts
              vm.$options.sockets[key] = sockets[key]
            }
          })
        }
      },
      beforeDestroy () {
        const vm: Vue = this as Vue;
        let sockets = vm.$options['sockets']

        if (sockets) {
          Object.keys(sockets).forEach((key) => {
            if (vm.$options.sockets) {//WTF required to fix error message in ts
              delete vm.$options.sockets[key]
            }
          })
        }
      }
    })
  }
}

export default WebSocketPlugin;