<template>
  <div id="wrapper">
    <nav class="navbar" style="background-color: #FFDFD3;">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-item"><strong>Glasgo</strong></router-link>
        <!-- for mobile
        <a class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbar-menu" @click="showMobileMenu = !showMobileMenu">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>-->
      </div>

      <div class="navbar-menu">
      <!--div class="navbar-menu" id="navbar-menu" v-bind:class="{'is-active': showMobileMenu }"-->
        <div class="navbar-start">
          <div class="navbar-item">
            <form method="get" action="/search">
              <div class="field has-addons">
                <div class="control">
                  <input type="text" class="input" placeholder="Explore Glasgow" name="query">
                </div>

                <div class="control">
                  <button class="button">
                      <span class="icon">
                      <i class="fas fa-search"></i>
                      </span>
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>

        <div class="navbar-end">
          <!--this is currently link to category slug-->
          <router-link to="/category" class="navbar-item">Category</router-link>
          <router-link to="/about" class="navbar-item">About us</router-link>

          <div class="navbar-item">
            <div class="buttons">
              <template v-if="$store.state.isAuthenticated">

                <router-link to="/my-account" class="button is-info is-light">My account</router-link>
                <button @click="logout()" class="button is-danger is-dark">Log out</button>
              </template>

              <template v-else>
                <router-link to="/log-in" class="button is-light">Log in</router-link>
                <router-link to="/sign-up" class="button is-primary">Sign up</router-link>
              </template>
            </div>

          </div>
        </div>
      </div>
    </nav>

    <div class="is-loading-bar has-text-centered" v-bind:class="{'is-loading': $store.state.isLoading }">
      <div class="lds-dual-ring"></div>
    </div>

    <section class="section">
      <router-view/>
    </section>

    <footer class="footer">
      <p class="has-text-centered">Copyright (c) 2023</p>
      <router-link to="/contact"><p class="has-text-centered">Contact Us</p></router-link>
    </footer>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      showMobileMenu: false,
    }
  },
  beforeCreate() {
    this.$store.commit('initializeStore')
    console.log('user at initialize', this.$store.state.user)
    const token = this.$store.state.token

    if (token) {
        axios.defaults.headers.common['Authorization'] = "Token " + token
    } else {
        axios.defaults.headers.common['Authorization'] = ""
    }
  },
  mounted() {
    this.cart = this.$store.state.cart
  },
  methods: {
    logout() {
        axios.defaults.headers.common["Authorization"] = ""

        localStorage.removeItem("token")
        localStorage.removeItem("user")

        this.$store.commit('removeToken')
        this.$store.commit('removeUser')

        this.$router.push('/')
    }
    
},
}
</script>

<style lang="scss">
@import '../node_modules/bulma';


.lds-dual-ring {
  display: inline-block;
  width: 80px;
  height: 80px;
}
.lds-dual-ring:after {
  content: " ";
  display: block;
  width: 64px;
  height: 64px;
  margin: 8px;
  border-radius: 50%;
  border: 6px solid #ccc;
  border-color: #ccc transparent #ccc transparent;
  animation: lds-dual-ring 1.2s linear infinite;
}
@keyframes lds-dual-ring {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.is-loading-bar {
  height: 0;
  overflow: hidden;

  -webkit-transition: all 0.3s;
  transition: all 0.3s;

  &.is-loading {
    height: 80px;
  }
}
</style>