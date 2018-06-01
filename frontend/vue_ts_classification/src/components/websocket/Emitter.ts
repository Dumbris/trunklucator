import { Statement } from "babel-types";

type Callback = () => void;

type ListenerType = {
    callback: Callback;
    vm: any;
}

type Listeners = ListenerType[]



class Emitter {
  public listeners: Map<string, Listeners>; 
  constructor () {
    this.listeners = new Map<string, Listeners>();
  }

  addListener (label: string, callback: Callback, vm: any) {
    if (typeof callback === 'function') {
      let listener =  this.listeners.get(label)
      if (listener) {
            listener.push({callback: callback, vm: vm})
      } else {
        this.listeners.set(label, [{callback: callback, vm: vm}])
      } 
      return true
    }
    return false
  }

  removeListener (label: string, callback: Callback, vm: any) {
    let listeners = this.listeners.get(label)
    let index

    if (listeners && listeners.length) {
      index = listeners.reduce((i, listener, index) => {
        if (typeof listener.callback === 'function' && listener.callback === callback && listener.vm === vm) {
          i = index
        }
        return i
      }, -1)

      if (index > -1) {
        listeners.splice(index, 1)
        this.listeners.set(label, listeners)
        return true
      }
    }
    return false
  }

  emit (label: string, ...args: any[]) {
    let listeners = this.listeners.get(label)

    if (listeners && listeners.length) {
      listeners.forEach((listener) => {
        listener.callback.call(listener.vm, ...args)
      })
      return true
    }
    return false
  }
}

export default new Emitter()