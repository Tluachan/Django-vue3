import { createStore } from 'vuex'

export default createStore({
  state: {
    isAuthenticated: false,
    token: '',
    isLoading: false,
    user: {
      username: '',
    }
  },
  mutations: {
    initializeStore(state) {

      if (localStorage.getItem('token')) {
          state.token = localStorage.getItem('token')
          state.isAuthenticated = true
          state.user.username = localStorage.getItem('user')
          //state.user.id = localStorage.getItem('userid')
      } else {
          state.token = ''
          state.isAuthenticated = false
          state.user.id = 0
          state.user.username = ''
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
    setUser(state, user) {
      state.user = user
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