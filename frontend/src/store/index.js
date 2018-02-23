import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import Cookies from 'js-cookie'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    auth: null,
    userInfo: null
  },
  // persist state to cookies
  plugins: [
    createPersistedState({
      getState: (key) => Cookies.getJSON(key),
      // TODO: set secure to true in production mode
      setState: (key, state) => Cookies.set(key, state, { expires: 1, secure: false })
    })
  ],
  getters: {
    authenticated: state => {
      return !(!state.auth)
    },
    isRoot: state => {
      return state.auth == null ? false : state.auth.is_root
    },
    permissionGroups: state => {
      return state.userInfo !== null ? state.userInfo.permissionGroups : []
    }
  },
  mutations: {
    setAuth (state, payload) {
      state.auth = payload
    },

    setUserInfo (state, payload) {
      state.userInfo = payload
    },

    logout (state) {
      state.auth = null
      state.userInfo = null
    }
  }
})
