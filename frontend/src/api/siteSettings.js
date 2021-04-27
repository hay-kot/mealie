import { baseURL } from "./api-utils";
import { apiReq } from "./api-utils";
import { store } from "@/store";

const settingsBase = baseURL + "site-settings";

const settingsURLs = {
  siteSettings: `${settingsBase}`,
  updateSiteSettings: `${settingsBase}`,
  testWebhooks: `${settingsBase}/webhooks/test`,
  customPages: `${settingsBase}/custom-pages`,
  customPage: id => `${settingsBase}/custom-pages/${id}`,
};

export const siteSettingsAPI = {
  async get() {
    let response = await apiReq.get(settingsURLs.siteSettings);
    return response.data;
  },

  async update(body) {
    let response = await apiReq.put(settingsURLs.updateSiteSettings, body);
    store.dispatch("requestSiteSettings");
    return response;
  },

  async getPages() {
    let response = await apiReq.get(settingsURLs.customPages);
    return response.data;
  },

  async getPage(id) {
    let response = await apiReq.get(settingsURLs.customPage(id));
    return response.data;
  },

  async createPage(body) {
    return await apiReq.post(settingsURLs.customPages, body);
  },

  async deletePage(id) {
    return await apiReq.delete(settingsURLs.customPage(id));
  },

  async updatePage(body) {
    return await apiReq.put(settingsURLs.customPage(body.id), body);
  },

  async updateAllPages(allPages) {
    let response = await apiReq.put(settingsURLs.customPages, allPages);
    return response;
  },
};
