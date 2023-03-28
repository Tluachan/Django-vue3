<template>
  <div class="column is-3">
    <div class="box">
      <h3 class="is-size-4">Review {{ review.id }}</h3>
      <p><strong>User ID:</strong> {{ review.user_id }}</p>
      <p><strong>Shop ID:</strong> {{ review.shop_id }}</p>
      <p><strong>Rating:</strong> {{ review.rating }}</p>
      <p><strong>Content:</strong> {{ review.content }}</p>
    </div>
  </div>
</template>

<script>
export default {
    name: 'ReviewBox',
    props: {
        review: Object
    }
}
</script>

<style scoped>
  .image {
    margin-top: -1.25rem;
    margin-left: -1.25rem;
    margin-right: -1.25rem;
  }
</style>