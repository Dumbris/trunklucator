<!-- src/components/ConnectionStatus.vue -->

<template>
    <div>
        <div :class="$style.greeting">{{status}}</div>
    </div>
</template>

<script lang="ts">
import Vue from "vue";

let getStatus = (ws: WebSocket):string => {
    switch (ws.readyState)
    {
        case ws.CLOSED: return "closed";
        case ws.OPEN: return "open";
        case ws.CLOSING: return "closing";
        case ws.CONNECTING: return "connecting";
        default: return "unknown";
    }
}

export default Vue.extend({
    props: ['status1'],
    computed: {
        status(): string {
            const vm = this as Vue
            return getStatus(vm.$socket);
        },
    }
});
</script>

<style  module>
.greeting {
    font-size: 14px;
}
</style>