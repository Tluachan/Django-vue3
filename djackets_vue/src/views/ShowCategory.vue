<template>
  <div class="page-categories">
    <div class="columns is-multiline">
      <div v-for="category in categories" :key="category.id" class="column is-4">
        <div class="card">
          <div class="card-image">
            <figure class="image is-4by3">
              <img :src="category.image" alt="Category image">
            </figure>
          </div>
          <div class="card-content">
            <div class="media">
              <div class="media-content">
                <p class="title is-4">{{ category.name }}</p>
              </div>
            </div>
            <div class="content">
              {{ category.description }}
            </div>
      
            <router-link :to="{ name: 'category', params: { category_slug: category.slug }}" class="button is-primary">View category</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios'

export default {
  name: 'Categories',
  data() {
    return {
      categories: []
    }
  },
  async mounted() {
    await this.getCategories()
  },
  methods: {
    async getCategories() {
      try {
        const response = await axios.get('/api/v1/categories/')
        this.categories = response.data
      } catch (error) {
        console.log(error)
      }
    }
  }
}
</script>
<style scoped>
.card {
  margin-bottom: 2rem;
}

.card-image {
  border-radius: 4px 4px 0 0;
  overflow: hidden;
}

.card-content {
  padding: 1.5rem;
}
</style>
