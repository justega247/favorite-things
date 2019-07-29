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
            <th><abbr title="Created Date">Created</abbr></th>
            <th><abbr title="Modified Date">Modified</abbr></th>
            <th><abbr title="View Details">Details</abbr></th>
            <th><abbr title="Edit">Edit</abbr></th>
            <th><abbr title="Delete">Delete</abbr></th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="favorite in categoryFavorites.results"
            :key="favorite.id"
          >
            <td>{{ favorite.ranking }}</td>
            <td>{{ favorite.title }}</td>
            <td>{{ favorite.description.substring(0, 18).concat('...') }}</td>
            <td>{{ formatDate(favorite.created_at) }}</td>
            <td>{{ formatDate(favorite.modified_at) }}</td>
            <td>
              <router-link
                :to="{ name: 'favorite-detail', params: { favoriteId: favorite.id }}"
              >
                Details
              </router-link>
            </td>
            <td>
              <router-link
                :to="{ name: 'favorite-edit', params: { favoriteId: favorite.id }}"
              >
                Edit
              </router-link>
            </td>
            <td><a @click="openDeleteModal(favorite)">Delete</a></td>
          </tr>
        </tbody>
      </table>
      <div class="pager">
        <paginate
          :page-count="Math.ceil(categoryFavorites.count/limit)"
          :page-range="3"
          :margin-pages="2"
          :click-handler="paginator"
          :prev-text="'Prev'"
          :next-text="'Next'"
          :container-class="'pagination'"
          :page-class="'page-item'"
        />
      </div>
    </div>
    <delete-modal
      v-show="showDeleteModal"
      :favorite-id="selectedFavoriteId"
      :favorite-name="selectedFavoriteName"
      @closeDeleteFavoriteModal="showDeleteModal = false"
      @loadFavorite="()=>loadCategoryFavorites()"
    />
  </div>
</template>

<script>
import DeleteModal from './FavoriteDeleteModal.vue'
import Header from './Header.vue'
import { mapGetters, mapState } from 'vuex'
import moment from 'moment'
export default {
  name: 'CategoryFavorites',
  components: {
    heading: Header,
    deleteModal: DeleteModal
  },
  data () {
    return {
      showDeleteModal: false,
      selectedFavoriteId: 0,
      selectedFavoriteName: '',
      limit: 10
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
      const limit = this.limit
      const offset = 0
      this.$store.dispatch('categoryModule/getCategoryFavorites', { categoryId, limit, offset })
    },
    getCategory () {
      const categoryId = this.$route.params.categoryId
      this.$store.dispatch('categoryModule/getCategory', categoryId)
    },
    formatDate (date) {
      return moment(date).format('L')
    },
    paginator (num) {
      const categoryId = this.$route.params.categoryId
      const pageLimit = this.limit
      const offset = (num - 1) * pageLimit
      this.$store.dispatch('categoryModule/getCategoryFavorites', { categoryId, pageLimit, offset })
    }
  }
}
</script>

<style scoped>
  .container {
    display: flex;
    justify-content: center;
    flex-direction: column;
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
  .pager {
    margin: 0px 500px;
    max-width: 100%;
  }

</style>
