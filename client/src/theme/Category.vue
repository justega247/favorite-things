<template>
  <div>
    This is the category page
    <router-link
      class="nav-item is-tab"
      to="/"
    >
      Landing
    </router-link>
    <a
      class="button"
      @click="showCategoryModal = true"
    >
      Add Category
    </a>
    <category-modal
      v-show="showCategoryModal"
      @closeCategoryModal="showCategoryModal = false"
    />
  </div>
</template>
<script>
import categoryModal from '../modals/categoryModal.vue'
export default {
  components: {
    'category-modal': categoryModal
  },
  data () {
    return {
      showCategoryModal: false
    }
  }
}
</script>
