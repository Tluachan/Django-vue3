<template>
    <div class="page-add-review">
        <div class="column is-multiline">
            <div class="column is-12">
                <h1 class="title">Add Review to {{product.name}} </h1>
            </div>
            <form @submit.prevent="submitForm" class=box>
                <div class="field">
                    <label class="label">Rating (Required) </label>
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
                    <label class="label">Review (Required) </label>
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
      errors: [],
      favorite: false,
    }
  },
  computed: {
    isFavorite() {
        return this.favorite
    }
  },
  mounted() {

  },
  watch: {
    $route(to, from) {
        if (to.name === 'AddReview') {
            this.submitForm()
        }
    }
  },
    created() {
    console.log('getproduct')
    const category_slug = this.$route.params.category_slug
    console.log('catslug', category_slug)
    const product_slug = this.$route.params.product_slug
    console.log('prodslug', product_slug)
    axios
      .get(`/api/v1/products/${category_slug}/${product_slug}/`)
      .then(response => {
        this.product = response.data
        console.log(this.product)
        document.title = this.product.name + ' | Glasgo'
      })
      .catch(error => {
        console.log(error)
      })
  },
  methods: {
    async submitForm() {
        console.log('isAuthenticated:', this.$store.state.isAuthenticated)
        this.errors = []

        if(!this.rating){
            this.errors.push('You need to select rating')
        }
        if(this.content === ''){
            this.errors.push('You need to input the review')

        }

        const category_slug = this.$route.params.category_slug
        const product_slug = this.$route.params.product_slug

        console.log('category_slug', category_slug)
        const user = localStorage.getItem('user')
        console.log('storage user', user)
        console.log('print outside')
        const token = localStorage.getItem('token')
        console.log("print token: ",token)

        if(!this.errors.length){
        const formData = {
            content: this.content,
            rating: this.rating,
            //pass product_slug to product attribute in review serializer
            product: product_slug,
            user: user
        }

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

          //Redirect bak to shop page
          this.$router.push({ name: 'Product', params: { category_slug, product_slug }})

        })
        .catch(error => {
            if (error.response) {
                for (const property in error.response.data) {
                    this.errors.push(`${property}: ${error.response.data[property]}`)
                }
                console.log(JSON.stringify(error.response.data))
                toast({
                    message: 'Something went wrong. Please try again',
                    type: 'is-danger',
                    dismissible: true,
                    pauseOnHover: true,
                    duration: 3000
                })
            } else if (error.message) {
                this.errors.push('Something went wrong. Please try again')
                console.log(JSON.stringify(error))
            }
        })
        }

    },
  },
  //above is method bracket
}
</script>
