<template>
        <div class="box product-box">
            <figure class="image mb-4">
                <img v-bind:src="product.get_thumbnail">
            </figure>

            <h3 class="is-size-6">{{ product.name }}</h3>

            <router-link v-bind:to="product.get_absolute_url" class="button is-dark mt-4">View details</router-link>
        </div>

</template>

<script>
export default {
    name: 'ProductBox',
    props: {
        product: Object
    }
}
</script>

<style scoped>
.image {
    height: 200px;
    object-fit: cover;
  }

.product-box {
    height: 350px;
    width: 250px;
    margin-top: 1.25rem;
    margin-left: 1.25rem;
    margin-right: 1.25rem;
  }
</style>