import { createStore } from 'vuex'

export default createStore({
  state: {
    isAuthenticated: false,
    token: '',
    isLoading: false,
    user: {
      username: null,
      shop_owner: false,
    }
  },
  mutations: {
    initializeStore(state) {

      if (localStorage.getItem('token')) {
          state.token = localStorage.getItem('token')
          state.isAuthenticated = true
          state.user.username = localStorage.getItem('user')
          state.user.shop_owner = localStorage.getItem('shop_owner')
      } else {
          state.token = ''
          state.isAuthenticated = false
          //state.user.username = ''
      } 
    },
    setIsLoading(state, status) {
      state.isLoading = status
    },
    setToken(state, token) {
        state.token = token
        state.isAuthenticated = true
        //console.log('isAuthenticate',state.isAuthenticated)
        //console.log('token set:', token)

    },  
    removeToken(state) {
        state.token = ''
        state.isAuthenticated = false
    },
    setUser(state, { username, shop_owner }) {
      if (!state.user) {
        state.user = {
          username: username,
          shop_owner: shop_owner
        };
      } else {
        state.user.username = username;
        state.user.shop_owner = shop_owner;
      }
    },
    removeUser(state, user) {
      state.user = ''
    },

  },
  getters: {
    user: state => state.user // add user getter
  },
  actions: {
  },
  modules: {
  }
})