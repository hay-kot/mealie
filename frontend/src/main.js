import Vue from "vue";
import App from "./App.vue";
import vuetify from "./plugins/vuetify";
import store from "./store";
import VueRouter from "vue-router";
import { routes } from "./routes";
import i18n from "./i18n";
import FlashMessage from "@smartweb/vue-flash-message";
import "@mdi/font/css/materialdesignicons.css";
import "typeface-roboto/index.css";

Vue.use(FlashMessage);
Vue.config.productionTip = false;
Vue.use(VueRouter);

const router = new VueRouter({
  routes,
  mode: process.env.NODE_ENV === "production" ? "history" : "hash",
});

const DEFAULT_TITLE = 'Mealie';
const TITLE_SEPARATOR = '🍴';
const TITLE_SUFFIX = " " + TITLE_SEPARATOR + " " + DEFAULT_TITLE;
router.afterEach( (to) => {
  Vue.nextTick( async () => {
    if(typeof to.meta.title === 'function' ) {
      const title  = await to.meta.title(to);
      document.title = title + TITLE_SUFFIX;
    } else {
      document.title = to.meta.title ? to.meta.title + TITLE_SUFFIX : DEFAULT_TITLE;
    }
  });
});  

const vueApp = new Vue({
  vuetify,
  store,
  router,
  i18n,
  render: h => h(App),
}).$mount("#app");

// Truncate
let truncate = function(text, length, clamp) {
  clamp = clamp || "...";
  let node = document.createElement("div");
  node.innerHTML = text;
  let content = node.textContent;
  return content.length > length ? content.slice(0, length) + clamp : content;
};

let titleCase = function(value) {
  return value.replace(/(?:^|\s|-)\S/g, x => x.toUpperCase());
};

Vue.filter("truncate", truncate);
Vue.filter("titleCase", titleCase);

export { vueApp };
export { router };
