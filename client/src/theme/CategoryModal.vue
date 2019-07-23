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
          @click="$emit('closeCategoryModal')"
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
          class="button is-success"
          @click="addCategory()"
        >
          Save
        </button>
        <button
          class="button"
          @click="$emit('closeCategoryModal')"
        >
          Cancel
        </button>
      </footer>
    </div>
  </div>
</template>

<script>
import Errors from '../helpers/errors'
export default {
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
          this.categoryName = ''
        })
        .catch((err) => this.errors.record(err.response.data))
    }
  }
}
</script>
