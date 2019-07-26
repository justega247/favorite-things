<template>
  <div>
    <heading />
    <div class="container">
      <h1>Create Favorite</h1>
      <div class="field">
        <label class="label">Title</label>
        <div class="control">
          <input
            v-model="title"
            class="input"
            type="text"
            placeholder="Favorite thing name"
            @keydown="errors.clear('title')"
          >
        </div>
        <span
          class="help is-danger"
          v-text="errors.get('title')"
        />
      </div>

      <div class="field">
        <label class="label">Ranking</label>
        <div class="control">
          <input
            v-model="ranking"
            class="input"
            type="email"
            placeholder="Favorite thing ranking"
            @keydown="errors.clear('ranking')"
          >
        </div>
        <span
          class="help is-danger"
          v-text="errors.get('ranking')"
        />
      </div>

      <div class="field">
        <label class="label">Category</label>
        <div class="control">
          <div
            class="select"
            @keydown="errors.clear('category')"
          >
            <select v-model="category">
              <option value="0">
                Select dropdown
              </option>
              <option
                v-for="categoryItem in categories"
                :key="categoryItem.id"
                :value="categoryItem.id"
              >
                {{ categoryItem.category }}
              </option>
            </select>
          </div>
          <span
            class="help is-danger"
            v-text="errors.get('category')"
          />
        </div>
      </div>

      <div class="field">
        <label class="label">Description</label>
        <div class="control">
          <textarea
            v-model="description"
            class="textarea"
            placeholder="Favorite thing description"
            @keydown="errors.clear('description')"
          />
        </div>
        <span
          class="help is-danger"
          v-text="errors.get('description')"
        />
      </div>
      <div class="field">
        <label class="label">Metadata</label>
        <div
          v-for="(data,k) in metadata"
          :key="k"
          class="form-group"
        >
          <div class="meta">
            <div class="meta meta-input">
              <input
                v-model="data.key"
                type="text"
                class="input meta-input"
                placeholder="key"
              >
              <input
                v-model="data.value"
                type="text"
                class="input"
                placeholder="value"
              >
            </div>
            <div>
              <span class="meta">
                <font-awesome-icon
                  v-show="k || ( !k && metadata.length > 1)"
                  icon="minus-square"
                  class="has-text-danger icon is-medium"
                  @click="remove(k)"
                />
                <font-awesome-icon
                  v-show="k == metadata.length-1"
                  icon="plus-square"
                  class="has-text-success icon is-medium"
                  @click="add(k)"
                />
              </span>
            </div>
          </div>
        </div>
        <span
          class="help is-danger"
          v-text="errors.get('metadata')"
        />
      </div>
      <br>
      <div class="field">
        <div class="control">
          <button
            class="button is-success"
            @click="addFavorite()"
          >
            Create Favorite
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import Vue from 'vue'
import VueToast from 'vue-toast-notification'
import 'vue-toast-notification/dist/index.css'
import { mapState } from 'vuex'
import Header from './Header.vue'
import Errors from '../helpers/errors'

Vue.use(VueToast)

export default {
  name: 'CreateFavorite',
  components: {
    heading: Header
  },
  data () {
    return {
      isEdit: false,
      title: '',
      description: '',
      category: 0,
      ranking: null,
      metadata: [
        {
          key: '',
          value: ''
        }
      ],
      errors: new Errors()
    }
  },
  computed: {
    ...mapState({
      categories: state => state.categoryModule.categories
    })
  },
  created () {
    this.loadCategories()
  },
  methods: {
    add (index) {
      this.metadata.push({
        key: '',
        value: ''
      })
    },
    remove (index) {
      this.metadata.splice(index, 1)
    },
    loadCategories () {
      this.$store.dispatch('categoryModule/getCategories')
    },
    addFavorite () {
      const metadata = {}
      const title = this.title
      const description = this.description
      const category = this.category
      const ranking = parseInt(this.ranking)
      this.metadata.forEach(entry => {
        metadata[entry.key] = entry.value
      })
      this.$store.dispatch('favoriteModule/addFavorite', {
        title,
        description,
        category,
        ranking,
        metadata
      }).then(() => {
        Vue.$toast.open({
          message: 'New Favorite created Successfully',
          type: 'success',
          position: 'top-right'
        })
        this.title = ''
        this.description = ''
        this.category = 0
        this.ranking = null
        this.metadata = [
          {
            key: '',
            value: ''
          }
        ]
      }).catch((err) => {
        console.log(err.response.data)
        if (err.response.data.status) {
          Vue.$toast.open({
            message: err.response.data.message,
            type: 'error',
            position: 'top-right'
          })
        }
        this.errors.record(err.response.data)
      })
    }
  }
}
</script>
<style scoped>
  .container {
    width: 30%;
  }
  .meta {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    margin-bottom: 5px;
  }
  .meta-input {
    margin-right: 15px;
  }
  .icon:hover {
    cursor: pointer;
  }
</style>
