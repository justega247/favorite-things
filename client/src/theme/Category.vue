<template>
  <div>
    <heading />
    <div class="container">
      <div class="columns">
        <div
          v-for="category in categories"
          :key="category.id"
          class="column is-one-quarter"
        >
          <app-category :link="category.created_at">
            <h3
              slot="category"
            >
              {{ category.category.toUpperCase() }}
            </h3>
            <router-link
              slot="favorite"
              class="nav-item is-tab button is-primary is-outlined"
              to="/"
            >
              View all favorite {{ category.category }}
            </router-link>
          </app-category>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import Header from './Header.vue'
import SingleCategory from './CategoryItem.vue'
import { mapGetters } from 'vuex'
export default {
  components: {
    'app-category': SingleCategory,
    heading: Header
  },
  data () {
    return {
      showCategoryModal: false
    }
  },
  computed: {
    ...mapGetters({
      categories: 'categoryModule/categories'
    })
  },
  created () {
    this.loadCategories()
  },
  methods: {
    loadCategories () {
      this.$store.dispatch('categoryModule/getCategories')
    }
  }
}
</script>
<style scoped>
  .columns {
    display: flex;
    flex-wrap: wrap;
  }
  .container {
    padding: 20px;
  }
  h3 {
    font-size: 90%;
    font-weight: normal;
  }
</style>
