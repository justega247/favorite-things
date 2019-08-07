<template>
  <div>
    <heading />
    <div class="back">
      <a
        class="button is-link"
        @click="goBack"
      >
        {{ back }}
      </a>
    </div>
    <div class="container has-background-light">
      <div class="detail has-background-white-ter">
        <h1><strong>{{ favorite.title }}</strong></h1>
        <h2><strong>Description:</strong> {{ favorite.description }}</h2>
        <hr>
        <h2><strong>Ranking:</strong> {{ favorite.ranking }}</h2>
        <hr>
        <h2><strong>Category:</strong> {{ favorite.category_name | capitalize }}</h2>
        <hr>
        <h2><strong>Created:</strong> {{ formatDate(favorite.created_at) }}</h2>
        <hr>
        <h2><strong>Modified:</strong> {{ formatDate(favorite.modified_at) }}</h2>
        <hr>
        <h2><strong>Metadata:</strong></h2>
        <div
          v-if="checkIsEmpty(favorite.metadata)"
        >
          <p>No metadata for this favorite</p>
        </div>
        <div
          v-else
          v-for="(data, index) in Object.entries(favorite.metadata)"
          :key="index"
        >
          <h4>{{ data[0] | capitalize }}: {{ data[1] }}</h4>
        </div>
      </div>
      <div
        v-if="audit[0]"
        class="container audit has-background-white-ter"
      >
        <h1>Audit-Log</h1>
        <ol
          v-for="(singleAudit,index) in audit"
          :key="index"
          type="1"
        >
          <li
            class="has-text-primary"
          >
            {{ singleAudit }}
          </li>
        </ol>
      </div>
      <div
        v-else
      >
        <h1>Audit-Log</h1>
        <h2>No audit log for this favorite yet, edit it to see the logs</h2>
      </div>
    </div>
  </div>
</template>

<script>
import moment from 'moment'
import isEmpty from 'lodash.isempty'
import { mapGetters } from 'vuex'
import Header from '../components/Header.vue'

export default {
  name: 'FavoriteDetailView',
  components: {
    heading: Header
  },
  data () {
    return {
      back: '<< Back'
    }
  },
  computed: {
    ...mapGetters({
      favorite: 'favoriteModule/favorite',
      audit: 'favoriteModule/historyLog'
    })
  },
  watch: {
    '$route' (to, from) {
      this.readMeta()
    }
  },
  created () {
    this.getFavorite()
    this.getFavoriteLog()
  },
  methods: {
    getFavorite () {
      const favoriteId = this.$route.params.favoriteId
      this.$store.dispatch('favoriteModule/getFavorite', favoriteId)
    },
    getFavoriteLog () {
      const favoriteId = this.$route.params.favoriteId
      this.$store.dispatch('favoriteModule/getFavoriteAudit', favoriteId)
    },
    goBack () {
      this.$router.push({ name: 'category-favorites', params: { categoryId: this.favorite.category } })
    },
    formatDate (date) {
      return moment(date).format('L')
    },
    checkIsEmpty (obj) {
      return isEmpty(obj)
    }
  }
}
</script>

<style scoped>
  .container {
    width: 50%;
    padding: 15px;
  }
  .audit {
    width: 100%;
    padding: 0px 10px 5px 10px;
    max-height: 500px;
    overflow: scroll;
  }
  .detail {
    padding: 0px 15px 5px 15px;
    width: 90%;
  }
  .back {
    padding-left: 250px;
  }
</style>
