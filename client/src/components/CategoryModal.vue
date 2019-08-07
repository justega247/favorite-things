<template>
  <div class="modal is-active">
    <div class="modal-background" />
    <div class="modal-card">
      <header class="modal-card-head">
        <p
          class="modal-card-title"
        >
          Create Category
        </p>
        <button
          class="delete"
          aria-label="close"
          @click="clearInput()"
        />
      </header>
      <section class="modal-card-body">
        <div class="field">
          <label class="label">Category</label>
          <div class="field-body">
            <div class="field">
              <p class="control">
                <input
                  v-model="categoryName"
                  class="input"
                  type="text"
                  placeholder="Category Name"
                  @keydown="errors.clear('category')"
                >
              </p>
            </div>
          </div>
        </div>
        <span
          class="help is-danger"
          v-text="errors.get('category')"
        />
      </section>
      <footer class="modal-card-foot">
        <button
          class="button is-primary"
          @click="addCategory()"
        >
          Save
        </button>
        <button
          class="button"
          @click="clearInput()"
        >
          Cancel
        </button>
      </footer>
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
import VueToast from 'vue-toast-notification'
import 'vue-toast-notification/dist/index.css'
import Errors from '../helpers/errors'

Vue.use(VueToast)

export default {
  name: 'CreateCategoryModal',
  data () {
    return {
      categoryName: '',
      errors: new Errors()
    }
  },
  methods: {
    addCategory () {
      this.$store.dispatch('categoryModule/addCategory', { category: this.categoryName })
        .then(() => {
          Vue.$toast.open({
            message: 'New Category created Successfully',
            type: 'success',
            position: 'top-right'
          })
          this.categoryName = ''
          this.$emit('closeCategoryModal')
          this.$router.push({ name: 'categories' })
        })
        .catch((err) => this.errors.record(err.response.data))
    },
    clearInput () {
      this.categoryName = ''
      this.$emit('closeCategoryModal')
    }
  }
}
</script>
