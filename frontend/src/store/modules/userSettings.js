import api from "@/api";
import Vuetify from "../../plugins/vuetify";
import axios from "axios";

function inDarkMode(payload) {
  let isDark;

  if (payload === "system") {
    //Get System Preference from browser
    const darkMediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
    isDark = darkMediaQuery.matches;
  } else if (payload === "dark") isDark = true;
  else if (payload === "light") isDark = false;

  return isDark;
}

const state = {
  activeTheme: {},
  darkMode: "system",
  isDark: false,
  isLoggedIn: false,
  token: "",
};

const mutations = {
  setTheme(state, payload) {
    Vuetify.framework.theme.themes.dark = payload.colors;
    Vuetify.framework.theme.themes.light = payload.colors;
    state.activeTheme = payload;
  },
  setDarkMode(state, payload) {
    let isDark = inDarkMode(payload);

    if (isDark !== null) {
      Vuetify.framework.theme.dark = isDark;
      state.isDark = isDark;
      state.darkMode = payload;
    }
  },
  setIsLoggedIn(state, payload) {
    state.isLoggedIn = payload;
  },
  setToken(state, payload) {
    state.isLoggedIn = true;
    axios.defaults.headers.common["Authorization"] = `Bearer ${payload}`;
    state.token = payload;
  },
};

const actions = {
  async resetTheme({ commit }) {
    const defaultTheme = await api.themes.requestByName("default");
    if (defaultTheme.colors) {
      Vuetify.framework.theme.themes.dark = defaultTheme.colors;
      Vuetify.framework.theme.themes.light = defaultTheme.colors;
      commit("setTheme", defaultTheme);
    }
  },


  async initTheme({ dispatch, getters }) {
    //If theme is empty resetTheme
    if (Object.keys(getters.getActiveTheme).length === 0) {
      await dispatch("resetTheme");
    } else {
      Vuetify.framework.theme.dark = inDarkMode(getters.getDarkMode);
      Vuetify.framework.theme.themes.dark = getters.getActiveTheme.colors;
      Vuetify.framework.theme.themes.light = getters.getActiveTheme.colors;
    }
  },
};

const getters = {
  getActiveTheme: state => state.activeTheme,
  getDarkMode: state => state.darkMode,
  getIsDark: state => state.isDark,
  getIsLoggedIn: state => state.isLoggedIn,
  getToken: state => state.token,
};

export default {
  state,
  mutations,
  actions,
  getters,
};
