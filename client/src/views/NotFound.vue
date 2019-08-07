<template>
  <div>
    <heading />
    <h1>Oops, Page not found!</h1>
  </div>
</template>

<script>
import Header from '../components/Header.vue'

export default {
  name: 'NotFoundPage',
  components: {
    heading: Header
  }
}
</script>
