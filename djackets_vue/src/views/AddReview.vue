<template>
    <div class="page-add-review">
        <div class="column is-multiline">
            <div class="column is-12">
                <h1 class="title">Add Review to {{this.product.name}} </h1>
            </div>
            <form @submit.prevent="submitForm">
                <div class="field">
                    <label class="label">Rating</label>
                    <div class="control">
                    <div class="select">
                        <select v-model="rating">
                        <option value="1">1</option>
                        <option value="2">2</option>
                        <option value="3">3</option>
                        <option value="4">4</option>
                        <option value="5">5</option>
                        </select>
                    </div>
                    </div>
                </div>
                <div class="field">
                    <label class="label">Review</label>
                    <div class="control">
                    <textarea class="textarea" v-model="content"></textarea>
                    </div>
                </div>
                <div class="field">
                    <div class="control">
                    <button class="button is-primary" type="submit">Submit</button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'

export default{
  name: 'AddReview',
  data() {
    return {
      product: {},
      content: '',
      rating: '',
      errors: []
    }
  },
  mounted() {
    const { category_slug, product_slug, product } = this.$route.query
    this.product = JSON.parse(product)
    console.log('product id', this.product.id)
    
  },
  methods: {
    async submitForm() {
        console.log('isAuthenticated:', this.$store.state.isAuthenticated)
        this.errors = []
        const product_slug = this.$route.params.product_slug
        const productID = this.product.id
        const formData = {
            content: this.content,
            rating: this.rating,
            //product: productID
        }

      //const product_slug = this.$route.params.product_slug
      console.log('product_slug', product_slug)
      const token = localStorage.getItem('token')
      console.log("print token: ",token)
      await axios
        .post(`/api/v1/reviews/`, formData,)
        .then(response => {
          toast({
            message: 'Review submitted successfully!',
            type: 'is-success',
            dismissible: true,
            pauseOnHover: true,
            duration: 3000
          })
          this.$router.push({ name: 'Product', params: { category_slug, product_slug }})
        })
        .catch(error => {
            if (error.response) {
                for (const property in error.response.data) {
                    this.errors.push(`${property}: ${error.response.data[property]}`)
                }
                console.log(JSON.stringify(error.response.data))
            } else if (error.message) {
                this.errors.push('Something went wrong. Please try again')
                console.log(JSON.stringify(error))
            }
        })
    },
  },
}
</script>
