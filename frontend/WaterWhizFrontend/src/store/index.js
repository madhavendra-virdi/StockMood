import Vue from 'vue'
import Vuex from 'vuex'
import modules from './modules'
Vue.use(Vuex)

const state = {
  
  userInfo: null,

  menuData: {
    list: [
      {
        index: 'workbench',
        label: 'workbench',
        url: '/workbench',
        icon: 'el-icon-s-data'
      }
    ],
    collapse: false
  }
}

const mutations = {
  
  switchCollapseMenu (state, value) {
    if (value != null) {
      state.menuData.collapse = value
    } else {
      state.menuData.collapse = !state.menuData.collapse
    }
    window.localStorage.setItem('MENU_STATUS', state.menuData.collapse)
  },
  
  setUserInfo: (state, data) => {
    state.userInfo = data
  }
}
const actions = {}
const getters = {}
export default new Vuex.Store({
  modules,
  state,
  mutations,
  actions,
  getters
})
