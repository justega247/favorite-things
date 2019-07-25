<template>
  <div>
    <heading />
    <h1>FAVORITE {{ category.category }}</h1>
    <div class="container">
      <table class="table is-hoverable is-fullwidth">
        <thead>
          <tr>
            <th>Ranking</th>
            <th><abbr title="Title">Title</abbr></th>
            <th><abbr title="Description">Description</abbr></th>
            <th><abbr title="View Details">Details</abbr></th>
            <th><abbr title="Edit">Edit</abbr></th>
            <th><abbr title="Delete">Delete</abbr></th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="favorite in categoryFavorites"
            :key="favorite.id"
          >
            <td>{{ favorite.ranking }}</td>
            <td>{{ favorite.title }}</td>
            <td>{{ favorite.description }}</td>
            <td><a>Details</a></td>
            <td><a>Edit</a></td>
            <td><a @click="openDeleteModal(favorite)">Delete</a></td>
          </tr>
        </tbody>
      </table>
    </div>
    <delete-modal
      v-show="showDeleteModal"
      :favoriteId="selectedFavoriteId"
      :favoriteName="selectedFavoriteName"
      @closeDeleteFavoriteModal="showDeleteModal = false"
      @loadFavorite="()=>loadCategoryFavorites()"
    />
  </div>
</template>
<script>
import DeleteModal from './FavoriteDeleteModal.vue'
import Header from './Header.vue'
import { mapGetters, mapState } from 'vuex'
export default {
  components: {
    heading: Header,
    deleteModal: DeleteModal
  },
  data () {
    return {
      showDeleteModal: false,
      selectedFavoriteId: 0,
      selectedFavoriteName: ''
    }
  },
  computed: {
    ...mapGetters({
      categoryFavorites: 'categoryModule/categoryFavorites'
    }),
    ...mapState({
      category: state => state.categoryModule.category
    })
  },
  created () {
    this.getCategory()
    this.loadCategoryFavorites()
  },
  methods: {
    openDeleteModal (favorite) {
      this.selectedFavoriteId = favorite.id
      this.selectedFavoriteName = favorite.title
      this.showDeleteModal = true
    },
    loadCategoryFavorites () {
      const categoryId = this.$route.params.categoryId
      this.$store.dispatch('categoryModule/getCategoryFavorites', categoryId)
    },
    getCategory () {
      const categoryId = this.$route.params.categoryId
      this.$store.dispatch('categoryModule/getCategory', categoryId)
    }
  }
}
</script>
<style scoped>
  .container {
    display: flex;
    justify-content: center;
  }
  a {
    color: #1426bd;
  }
  abbr[title] {
    border-bottom: none;
    text-decoration: none;
  }
  h1 {
    text-align: center;
  }
</style>
