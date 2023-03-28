<template>
        <div class="page-my-account">
            <div class="columns is-multiline">
                <div class="column is-10">
                    <h1 class="title">My account</h1>
                </div>
                <template v-if="$store.state.user.shop_owner">
                    <router-link to="/user/shop-owner-view">
                <div calss="column is-1">
                    <button class="button is-light">
                    Shop Owner View
                    </button>
                </div>
                </router-link>
                </template>

            </div>
            <div class="column is-multiline is-flex">
                <div ref = "leftside" class="column is-6">
                <h2 style="font-size: 24px;">Your Reviews</h2>
                    <div
                        v-for="review in reviews"
                        v-bind:key="review.id"
                        v-bind:review="review"
                        class="column is-10">
                        <div class="box" >
                            <router-link v-bind:to="review.product.get_absolute_url">
                            <p><strong>{{ review.product.name }}</strong></p>
                            </router-link>
                            <p><strong>Content: </strong>{{ review.content }}</p>
                            <p><strong>Rating: </strong>{{ review.rating }}/5</p>
                            <p>Reviewed on: {{ review.datetime }}</p>
                        </div>
                    </div>
                </div>

                <div class="column is-5">
                <h2 style="font-size: 24px; margin-bottom:12px">Your Favorite Shops</h2>
                    <div class="box">
                        <div
                            v-for="favshop in favshops"
                            v-bind:key="favshop.product"
                            v-bind:favshop="fav-shop"
                            >
                                <router-link v-bind:to="favshop.product.get_absolute_url">
                                <p><strong>{{ favshop.product.name }}</strong></p>
                                </router-link>
                        </div>
                    </div>
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
            console.log('get user review list')
            const user = localStorage.getItem('user')
            console.log('username: ',user)
            axios
                .get(`/api/v1/reviews/user/${user}/`)
                .then(response =>{
                    console.log('review response', response.data)
                    this.reviews = response.data
                })
                .catch(error => {
                    console.log(error)
                })

        },

        getUserFavoriteShopList(){
            console.log('get user favorite shop list')
            const token = localStorage.getItem('token')
            console.log('token', token)
            axios.defaults.headers.common["Authorization"] = "Token " + token
            axios
                .get(`/api/v1/favorite-shops/`)
                .then(response =>{
                    console.log('favorite shop response', response.data)
                    this.favshops = response.data
                })
                .catch(error => {
                    console.log(error)
                })
        },

    },
})
</script>
