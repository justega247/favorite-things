<template>
  <div>
    <nav
      class="navbar nav__bottom"
      role="navigation"
      aria-label="main navigation"
    >
      <div class="navbar-brand">
        <div class="navbar-start">
          <router-link
            class="nav-item is-tab"
            to="/"
          >
            <h1>Favorite Things App</h1>
          </router-link>
        </div>
      </div>

      <div
        id="navbarBasicExample"
        class="navbar-menu"
      >
        <div class="navbar-end">
          <div class="navbar-item">
            <div class="buttons">
              <router-link
                class="button is-primary is-outlined"
                :to="{ name: 'favorite' }"
              >
                Add Favorite
              </router-link>
              <a
                class="button is-primary is-outlined"
                @click="showCategoryModal = true"
              >
                Add Category
              </a>
            </div>
          </div>
        </div>
      </div>
    </nav>
    <category-modal
      v-show="showCategoryModal"
      @closeCategoryModal="showCategoryModal = false"
    />
  </div>
</template>
<script>
import categoryModal from './CategoryModal.vue'
export default {
  name: 'Header',
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
<style lang="scss" scoped>
  .navbar-brand {
    padding: 0 0.8125rem;
  }
  a {
    color: lighten($color: #000000, $amount: 40%)
  }
</style>
