<!-- src/components/Task.vue -->

<template>
    <div><SampleViewer v-bind:x="task.x"/>{{task.title}}</div>
</template>

<script lang="ts">
import { Task } from './../protocol/types'
import SampleViewer from './SampleViewer.vue';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({
  name: 'TaskViewer',
  components: {
    SampleViewer
  }
})
export default class TaskViewer extends Vue {
  @Prop({type: Task}) private task!: Task;

  mounted() {
      console.log(this)
  }
}
</script>

<style  module>
.greeting {
    font-size: 30px;
}
</style>