<template>
  <div class="home">
    <div class="columns is-multiline">
      <div class="column is-12">
        <h2 class="is-size-2 has-text-centered">Explore These Categories</h2>
      </div>
    </div>

      <div 
        class="column is-12"
        v-for="category in categories"
        v-bind:key="category.id"
        >
        <router-link v-bind:to="category.get_absolute_url">
          <div class>
            <div class="column is-12">
              <h3 class="is-size-4 has-text-left ">{{ category.name }}</h3>
              
            </div>
            
          </div>
        </router-link>

        <div
          v-for="product in category.products"
          v-bind:key="product.id"
          v-bind:product="product">
          <div>
              <div class="box">
                  <figure class="image mb-1">
                      <img v-bind:src="product.get_thumbnail">
                  </figure>
                  <router-link v-bind:to="product.get_absolute_url">
                  <h3 class="is-size-4">{{ product.name }}</h3>
                  </router-link>
                  Current Rating: {{ product.avg_rating ? product.avg_rating.toFixed(2) : '' }} / 5
              </div>
          </div>
        </div>
      </div> 

  </div>
</template>

<script>
import axios from 'axios';
import { toast } from 'bulma-toast'

import ProductBox from '@/components/ProductBox'

export default {
  name: 'CategoriesPage',
  components: {
    ProductBox
  },
  data() {
    return {
      categories: [],
      products: [],
    }
  },
  components: {

  },
  mounted() {
    this.getCategoryList()
    this.categories.forEach(category => {
    this.getCategory(category)
})

    document.title = 'All Categories | Glasgo'
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
    },

    async getCategory(category) {
      const categorySlug =category.slug;
      console.log('slug', categorySlug)
        axios
            .get(`/api/v1/products/${categorySlug}/`)
            .then(response => {
                this.category = response.data

            })
            .catch(error => {
                console.log(error)

                toast({
                    message: 'Something went wrong. Please try again.',
                    type: 'is-danger',
                    dismissible: true,
                    pauseOnHover: true,
                    duration: 2000,
                    position: 'bottom-right',
                })
            })

        this.$store.commit('setIsLoading', false)
    }



  },
}
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