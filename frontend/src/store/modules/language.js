import VueI18n from "../../i18n";

const state = {
  lang: "en",
  allLangs: [
    {
      name: "English",
      value: "en",
    },
    {
      name: "Danish",
      value: "da",
    },
    {
      name: "French",
      value: "fr",
    },
    {
      name: "Swedish",
      value: "sv",
    },
    {
      name: "简体中文",
      value: "zh-CN",
    },
    {
      name: "繁體中文",
      value: "zh-TW",
    },
  ],
};

const mutations = {
  setLang(state, payload) {
    VueI18n.locale = payload;
    state.lang = payload;
  },
};

const actions = {
  initLang({ getters }) {
    VueI18n.locale = getters.getActiveLang;
  },
};

const getters = {
  getActiveLang: (state) => state.lang,
  getAllLangs: (state) => state.allLangs,
};

export default {
  state,
  mutations,
  actions,
  getters,
};
