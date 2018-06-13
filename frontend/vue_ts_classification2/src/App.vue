<template>
  <div id="app">
    <img src="./assets/logo.png">
    <ConnectionStatus/>
    <TaskViewer v-bind:task="store.state.task"/>
  </div>
</template>

<script lang="ts">
import { Component, Watch, Prop, Vue } from 'vue-property-decorator';
import TaskViewer from './components/Task.vue';
import ConnectionStatus from './components/ConnectionStatus.vue';
import { Store, store } from './store'
import { Task } from './protocol/types'

@Component({
  components: {
    TaskViewer,
    ConnectionStatus,
  },
})
export default class App extends Vue {
  // Data property
  @Prop({type: Store}) private store!: Store;

  // Lifecycle hook
  created () {
    this.store = store
  }
  @Watch('store')
  onPropertyChanged(value: Store, oldValue: Store) {
    // Do stuff with the watcher here.
    console.log('!!!',value)
  }
  get taskProp(): Task {
    return this.store.state.task
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
