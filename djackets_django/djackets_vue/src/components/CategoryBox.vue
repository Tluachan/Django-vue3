<template>
  <div>
    <h3 class="is-size-3">{{ category.name }}</h3>
    <div class="columns is-multiline">
      <ProductBox 
        v-for="product in category.products"
        v-bind:key="product.id"
        v-bind:product="product" />
    </div>
  </div>
</template>

<script>
import ProductBox from '@/components/ProductBox'

export default {
  name: 'CategoryBox',
  components: {
    ProductBox
  },
  props: {
    category: Object
  }
}
</script>
