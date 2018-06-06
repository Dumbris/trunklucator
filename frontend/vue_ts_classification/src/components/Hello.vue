<!-- src/components/Hello.vue -->

<template lang="pug">
    <div>
        <div :class="$style.greeting">Hello {{name}}{{exclamationMarks}}</div>
        <button @click="decrement">-</button>
        <button @click="increment">+</button>
    </div>
</template>

<script lang="ts">
import Vue from "vue";
import * as basket from "./store/task"; // Or better import specific accessor to be explicit about what you use

getterResult = basket.readProductNames(this.$store); // This returns Product[] 
//basket.dispatchUpdateTotalAmount(this.$store, 0.5); // This accepts number (discount) - you'd normally use an object as arguments. Returns promise.
//basket.commitAppendItem(this.$store, newItem); // This will give compilation error if you don't pass { product: Product; atTheEnd: boolean } in

export default Vue.extend({
    props: ['name', 'initialEnthusiasm'],
    data() {
        return {
            enthusiasm: this.initialEnthusiasm,
        }
    },
    methods: {
        increment() { this.enthusiasm++; },
        decrement() {
            if (this.enthusiasm > 1) {
                this.enthusiasm--;
            }
        },
    },
    computed: {
        exclamationMarks(): string {
            return Array(this.enthusiasm + 1).join('!');
        }
    }
});
</script>

<style  module>
.greeting {
    font-size: 30px;
}
</style>