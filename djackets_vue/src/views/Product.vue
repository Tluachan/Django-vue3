<template>
    <div class="page-product">
        <div class="columns is-multiline">
            <div class="column is-9" style="margin-bottom: 50px;">
                <div class="is-flex is-justify-content-space-between">
                    <h1 class="title">{{ product.name }}</h1>
                    <i class="fa fa-heart" :class="{ 'favorite': isFavorite }" @click="toggleFavorite"></i>
                </div>
                <div class="button-wrapper">
                    <button @click="goToReviewPage" class="button is-rounded" style="background-color: #FFDFD3;">Add Review</button>
                </div>
                <p><strong>{{ product.address }}</strong> <a :href="product.map_url" target="_blank">(Map direction)</a></p>
                <p><strong>Phone: </strong> {{product.phone}}</p>
                <p><strong>Description: </strong>{{ product.description }}</p>
                <p><strong>Rating: </strong> {{ product.avg_rating ? product.avg_rating.toFixed(2) : '' }} / 5</p>
            </div>

            <div class="column is-3">
                <figure class="image mb-3">
                <img :src="product.get_image" style="width: 500px; height: auto;">
                </figure>
            </div>

            <div class="column is-12 mt-6">
                <h2 class="review" style="font-size: 24px">Customer Reviews</h2>
                <!--TEST-->
                <div class="column is-12">
                    <div>
                        <div v-for="review in reviews" :key="review.id" class="column is-6">
                        <div class="box">
                            <p><strong>{{ review.user.username }}</strong></p>
                            <!--p><strong>{{ review.product }}</strong></p>-->
                            <p>{{ review.content }}</p>
                            <p>Rating: {{ review.rating }}/5</p>
                            <p>{{ review.datetime }}</p>
                        </div>
                        </div>
                    </div>

                </div>
                    </div>


        </div>         
    </div>
</template>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast';

export default {
    name: 'Product',
    components: {
        //ReviewBox
    },
    data(){
        return{
            product:{},
            reviews: [],
            product_slug: '',
            //favorite status for product
            isFavorite: false,
            //button status
            favorite: false,
        }
    },
    mounted(){
        this.getProduct()
        this.getReviewList()
    },
    methods: {
        toggleFavorite() {
            this.isFavorite = !this.isFavorite;
            const product_slug = this.$route.params.product_slug
            const user = localStorage.getItem('user')
          
            //if heart is red, favorite
            if(this.isFavorite){
                const favoriteData = {
                    product: product_slug,
                    user: user,
                }                        
                console.log('posting favorite')
                axios
                    .post(`/api/v1/favorite-shops/`, favoriteData)
                    .then(response => {
                    })
                    .catch(error => {
                        console.log(error)
                    })
            }


                        //if heart is black, remove favorite
            if(!this.isFavorite){
                const favoriteData = {
                    product: product_slug,
                    user: user,
                }    
                console.log('deleting favorite')
                console.log('favorite data to delete', favoriteData)
                axios
                    .delete(`/api/v1/favorite-shops/delete/`, {data: {user: user,product: product_slug}})
                    .then(response => {
                    })
                    .catch(error => {
                        console.log(error)
                        // handle error response
                        if (error.response.status === 404) {
                        console.error('Favorite shop not found!');
                        } else {
                        console.error('Error deleting favorite shop:', error);
                        }
                    })
            }


        },
        async getProduct(){
            this.$store.commit('setIsLoading',true)

            const category_slug = this.$route.params.category_slug
            const product_slug = this.$route.params.product_slug

            await axios
                .get(`/api/v1/products/${category_slug}/${product_slug}`)
                .then(response => {
                    this.product = response.data
                    document.title = this.product.name + ' | Glasgo'
                })
                .catch(error => {
                    console.log(error)
                })
                this.$store.commit('setIsLoading',false)
                this.product_slug = product_slug
        },
        getReviewList(){
            const product_slug = this.$route.params.product_slug
            axios
                .get(`/api/v1/products/${product_slug}/reviews`)
                .then(response => {
                    this.reviews = response.data
                })
                .catch(error => {
                    console.log(error)
                })                
        },
        goToReviewPage() {
            const category_slug = this.$route.params.category_slug
            const product_slug = this.$route.params.product_slug
            this.$router.push({
                name: 'Review',
                /*query: { 
                    category_slug,
                    product_slug,
                    product: JSON.stringify(this.product) // convert to string to pass as query param
                    }*/
            })
        }        
    }    
}
</script>

<style scoped>
.button-wrapper {
    margin-top: 10px;
    margin-bottom: 10px;
}
.favorite {
  color: red;
}
.product-header {
  display: flex;
  justify-content: space-between;
}
.fa-heart{
    font-size: 24px
}
</style>