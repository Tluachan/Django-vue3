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
        <div ref="content" class="column is-multiline is-flex">
            <div ref="leftside" class="column is-6">
                <!--div ref="review" class="column is-12"-->
                    <h2 style="font-size: 24px;">Your Shops</h2>
                    <div class="box">
                        <div 
                            v-for="showproduct in productlist" 
                            v-bind:key="showproduct.id"
                            v-bind:showproduct="showproduct">
                            <p style="margin-bottom: 10px">
                                <router-link v-bind:to="showproduct.get_absolute_url">
                                <strong>{{ showproduct.name }}</strong>
                                
                                </router-link>
                                    <button class="button is-light is-small product-button">
                                        Edit
                                    </button>
                                    <button class="button is-light is-small product-button" @click="deleteProduct(showproduct)">
                                        Delete
                                    </button>
                            </p>
                                        
                        </div>    
                    </div>   

            <!--/div-->           
            </div>
            <div ref="createshop" class="column is-4 is-offset-1">
                <h2 style="font-size: 24px;">Create New Shop (All field is required)</h2>
                <form @submit.prevent="submitForm">
                    <div class="field">
                    <label class="label">Category</label>
                    <div class="control">
                        <div class="select">
                        <select v-model="product.category">
                            <option v-for="category in categories" v-bind:key="category.id" :value="category.id">{{ category.name }}</option>
                        </select>
                        </div>
                    </div>
                    </div>

                    <div class="field">
                    <label class="label">Name</label>
                    <div class="control">
                        <input class="input" type="text" v-model="product.name" required>
                    </div>
                    </div>

                    <div class="field">
                    <label class="label">Description</label>
                    <div class="control">
                        <textarea class="textarea" v-model="product.description"></textarea>
                    </div>
                    </div>

                    <div class="field">
                    <label class="label">Address</label>
                    <div class="control">
                        <input class="input" type="text" v-model="product.address" required>
                    </div>
                    </div>

                    <div class="field">
                    <label class="label">Image</label>
                    <div class="control">
                        <input class="input" type="file" @change="onFileChange">
                    </div>
                    </div>

                    <div class="field">
                    <label class="label">Phone</label>
                    <div class="control">
                        <input class="input" type="text" v-model="product.phone" required>
                    </div>
                    </div>

                    <div class="field">
                    <label class="label">Google Map URL (Optional) </label>
                    <div class="control">
                        <input class="input" type="url" v-model="product.map_url" required>
                    </div>
                    </div>

                    <button class="button is-primary" type="submit">Create Shop</button>

                </form>
            </div>
        </div>
    </div>

</template>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'

export default ({
    name: 'ShowOwner', 
    data(){
        return {
            errors: [],
            product: {
                category: '',
                name: '',
                description:'',
                address:'',
                image: null,
                phone:'',
                map_url:'',
                owner:'',
            },
            categories: [],
            testuser: null,
            productlist: [],

    }
    },
    mounted(){
        this.getCategoryList()
        this.getShopList()
        document.title = 'Show Owner Page | Glasgo'

        axios
            .get('/api/v1/users/me')
            .then(response => {
               this.testuser = response.data
                
            })

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
        onFileChange(event) {
        this.product.image = event.target.files[0];
        },
        async submitForm() {

            this.errors = []

            if (!this.product.category) {
            this.errors.push('Category is required');
            }

            if (!this.product.name) {
            this.errors.push('Name is required');
            }

            if (!this.product.description) {
            this.errors.push('Description is required');
            }

            if (!this.product.address) {
            this.errors.push('Address is required');
            }
            if (!this.product.image) {
            this.errors.push('Image is required');
            }

            if (!this.product.phone) {
            this.errors.push('Phone is required');
            }
            if (!this.product.map_url) {
            this.errors.push('Map URL is required');
            }

            if(!this.errors.length){
            const formData = new FormData();
            formData.append('category', this.product.category);
            formData.append('name', this.product.name);
            formData.append('description', this.product.description);
            formData.append('address', this.product.address);
            formData.append('image', this.product.image);
            formData.append('phone', this.product.phone);
            formData.append('map_url', this.product.map_url);
            formData.append('owner',localStorage.getItem('username'))
            console.log('form',formData)

            await axios.post('/api/v1/products/create/', formData)
                .then(response => {
                    toast({
                        message: 'New shop created successfully!',
                        type: 'is-success',
                        dismissible: true,
                        pauseOnHover: true,
                        duration: 3000
                    })

                   //Redirect bak to shop owner page
                   const toPath = this.$route.query.to || '/my-account'
                   console.log('topath',toPath)
                    //this.$router.push(toPath)

                })
                .catch(error => {
                    if(error.response){
                        console.log(error)
                    }
                })
            } else {
                    toast({
                        message: this.errors.join('<br>'),
                        type: 'is-warning is-light',
                        dismissible: true,
                        pauseOnHover: true,
                        duration: 3000
                    })
            }
    
        },

        getShopList(){
            axios
                .get(`/api/v1/products/getlist`)
                .then(response =>{
                    console.log(response.data)
                    this.productlist = response.data
                })
                .catch(error => {
                    console.log(error)
                })
        },
        
        deleteProduct(showproduct){
            
            if(window.confirm('Are you sure you would like to delete this shop?')){
                console.log('product id',showproduct.id)
                axios
                    .delete(`/api/v1/products/${showproduct.id}`)
                    .then(response =>{
                        console.log('shop deleted')
                        
                    })
                    .catch(error => {
                        console.log(error)
                    })
            }

        },
    
    },
})
</script>

<style scoped>
.product-button {
  margin-top: -3px;
  margin-left: 10px;
}

</style>
