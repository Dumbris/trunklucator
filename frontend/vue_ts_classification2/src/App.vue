<template>
  <div id="app">
    <img src="./assets/logo.png">
    <ConnectionStatus/>
    <TaskViewer task="store.state.task"/>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import TaskViewer from './components/Task.vue';
import ConnectionStatus from './components/ConnectionStatus.vue';
import { Store, store } from './store'

@Component({
  components: {
    TaskViewer,
    ConnectionStatus,
  },
})
export default class App extends Vue {
  // Data property
  store: Store;

  // Lifecycle hook
  mounted () {
    this.store = store
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
