import { baseURL } from "./api-utils";
import { apiReq } from "./api-utils";
import i18n from '@/i18n.js';
const groupPrefix = baseURL + "groups";

const groupsURLs = {
  groups: `${groupPrefix}`,
  create: `${groupPrefix}`,
  delete: id => `${groupPrefix}/${id}`,
  current: `${groupPrefix}/self`,
  update: id => `${groupPrefix}/${id}`,
};

function deleteErrorText(response) {
  console.log(response.data);
  switch(response.data.detail) {
    case 'GROUP_WITH_USERS':
      return i18n.t('user.cannot-delete-group-with-users');
      
    case 'GROUP_NOT_FOUND':
      return i18n.t('user.group-not-found');
      
    case 'DEFAULT_GROUP':
      return i18n.t('user.cannot-delete-default-group');

    default:
      return i18n.t('user.group-deletion-failed');
  }
}

export const groupAPI = {
  async allGroups() {
    let response = await apiReq.get(groupsURLs.groups);
    return response.data;
  },
  create(name) {
    return apiReq.post(
      groupsURLs.create,
      { name: name },
      function() { return i18n.t('user.user-group-creation-failed'); },
      function() { return i18n.t('user.user-group-created'); }
    );
  },
  delete(id) {
     return apiReq.delete(
       groupsURLs.delete(id), 
       null, 
       deleteErrorText,
       function() { return i18n.t('user.group-deleted'); }
     );
  },
  async current() {
    let response = await apiReq.get(groupsURLs.current);
    return response.data;
  },
  update(data) {
    return apiReq.put(
      groupsURLs.update(data.id), 
      data, 
      function() { return i18n.t('user.error-updating-group'); },
      function() { return i18n.t('settings.group-settings-updated'); }
    );
  },
};
