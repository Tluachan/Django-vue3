<template>
  <div class="home">
    <section class="hero is-medium is-dark mb-6" style="background-color: #FFDFD3;">
      <div class="hero-body">
        <div class="container has-text-centered">
          <p class="title mb-6 has-text-black">
            Start your Glasgow Adventure
          </p>
          <form method="get" action="/search" class="mt-6">
            <div class="field has-addons">
              <div class="control is-expanded">
                <input type="text" class="input" placeholder="Start exploring" name="query">
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
    </section>

    <div class="columns is-multiline">
      <div class="column is-12">
        <h2 class="is-size-2 has-text-centered">Explore These Categories</h2>
      </div>

      <div 
        class="column is-3"
        v-for="category in categories"
        v-bind:key="category.id"
        >
        <router-link v-bind:to="category.get_absolute_url">
          <div class = "box">
              <figure class="image mb-4">
              <img :src="category.get_thumbnail">
            </figure>
              <h3 class="is-size-4">{{ category.name }}</h3>
          </div>
        </router-link>
      </div> 
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Home',
  data() {
    return {
      categories: []
    };
  },
  components: {

  },
  mounted() {
    this.getCategoryList()
    document.title = 'Home | Djackets'
  },
  methods: {
    getCategoryList() {
      axios 
        .get('/api/v1/categories/')
        .then(response => {
          this.categories = response.data
        })
        .catch(error => {
          console.log(error)
        })
    }
  }
};
</script>

<style scoped>
.hero-body {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.hero-body form {
  width: 100%;
}

.box {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>