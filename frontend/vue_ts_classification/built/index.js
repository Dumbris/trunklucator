import Vue from "vue";
import HelloComponent from "./components/Hello.vue";
var v = new Vue({
    el: "#app",
    template: "\n    <div>\n        <div>Hello {{name}}!</div>\n        Name: <input v-model=\"name\" type=\"text\">\n        <hello-component :name=\"name\" :initialEnthusiasm=\"5\" />\n    </div>",
    data: {
        name: "World"
    },
    components: {
        HelloComponent: HelloComponent
    }
});
//# sourceMappingURL=index.js.map