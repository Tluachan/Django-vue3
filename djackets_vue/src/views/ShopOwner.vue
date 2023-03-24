<template>

        <div class="page-my-account">
            <div class="columns is-multiline">
                <div class="column is-10">
                    <h1 class="title">Shop Owner Account</h1>
                </div>
                <template v-if="$store.state.user.shop_owner">
                    <router-link to="/my-account">
                <div calss="column is-1">
                    <button class="button is-light">
                    User View
                    </button>
                </div> 
                </router-link>
                </template>

            </div>
                <div class="column is-7">
                    <h2 style="font-size: 24px;">Your Reviews</h2>
                </div>

                <div 
                    v-for="review in reviews" 
                    v-bind:key="review.id"
                    v-bind:review="review" 
                    class="column is-6">
                    <div class="box has-background-white" >
                        <router-link v-bind:to="review.product.get_absolute_url">
                        <p><strong>{{ review.product.name }}</strong></p>
                        </router-link>
                        <!--p><strong>{{ review.product }}</strong></p>-->
                        <p><strong>Content: </strong>{{ review.content }}</p>
                        <p><strong>Rating: </strong>{{ review.rating }}/5</p>
                        <p>Reviewed on: {{ review.datetime }}</p>
                    </div>
                </div>

                <h2 style="font-size: 24px;">Your Favorite Shops</h2>
                <div class="box">
                <div 
                    v-for="favshop in favshops" 
                    v-bind:key="favshop.product"
                    v-bind:favshop="fav-shop">
                        <router-link v-bind:to="favshop.product.get_absolute_url">
                        <p><strong>{{ favshop.product.name }}</strong></p>
                        </router-link>
                </div>    
        </div>            


        </div>

</template>

<script>
import axios from 'axios'

export default ({
    name: 'MyAccount', 
    data(){
        return {
            reviews: [],
            favshops: [],
            fav:{},
            shop: {},

    }
    },
    mounted(){
        this.getUserAllReviewList()
        this.getUserFavoriteShopList()
    },
    methods: {
        getUserAllReviewList(){
            const user = localStorage.getItem('user')
            console.log('username: ',user)
            axios
                .get(`/api/v1/reviews/user/${user}/`)
                .then(response =>{
                    console.log(response.data)
                    this.reviews = response.data
                })
                .catch(error => {
                    console.log(error)
                })

        },

        getUserFavoriteShopList(){
            axios
                .get(`/api/v1/favorite-shops`)
                .then(response =>{
                    console.log(response.data)
                    this.favshops = response.data
                })
                .catch(error => {
                    console.log(error)
                })
        },
    
    },
})
</script>
