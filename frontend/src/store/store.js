import Vue from "vue";
import Vuex from "vuex";
import api from "../api";
import createPersistedState from "vuex-persistedstate";
import userSettings from "./modules/userSettings";

Vue.use(Vuex);

const store = new Vuex.Store({
  plugins: [
    createPersistedState({
      paths: ["userSettings"],
    }),
  ],
  modules: {
    userSettings,
  },
  state: {
    // Snackbar
    snackActive: false,
    snackText: "",
    snackType: "warning",

    // All Recipe Data Store
    recentRecipes: [],
    allRecipes: [],
  },

  mutations: {
    setSnackBar(state, payload) {
      state.snackText = payload.text;
      state.snackType = payload.type;
      state.snackActive = true;
    },
    setSnackActive(state, payload) {
      state.snackActive = payload;
    },

    setRecentRecipes(state, payload) {
      state.recentRecipes = payload;
    },
  },

  actions: {
    async requestRecentRecipes() {
      const keys = [
        "name",
        "slug",
        "image",
        "description",
        "dateAdded",
        "rating",
      ];
      const payload = await api.recipes.allByKeys(keys);

      this.commit("setRecentRecipes", payload);
    },
  },

  getters: {
    //
    getSnackText: (state) => state.snackText,
    getSnackActive: (state) => state.snackActive,
    getSnackType: (state) => state.snackType,

    getRecentRecipes: (state) => state.recentRecipes,
  },
});

export default store;
export { store };
