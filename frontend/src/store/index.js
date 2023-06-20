import {createStore} from 'vuex'

export default createStore({
  state: {
    access: "",
    refresh: "",
    user: "",
    logout: true,
  },
  getters: {},
  mutations: {
    clearState(state) {
      state.access = ""
      state.refresh = ""
      state.user = ""
      state.logout = false
    },
    setAccess(state, access) {
      state.access = access
    },
    setRefresh(state, refresh) {
      state.refresh = refresh
    },
    setUser(state, user) {
      state.user = user
    },
    setLogout(state, logout) {
      state.logout = logout
    },
  },
  actions: {
    initializeStore() {
      this.state.refresh = localStorage.getItem("refresh") ? localStorage.getItem("refresh") : ''
    },
  },
  modules: {}
})
