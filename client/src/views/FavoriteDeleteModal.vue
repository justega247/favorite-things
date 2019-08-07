<template>
  <div class="modal is-active">
    <div class="modal-background" />
    <div class="modal-card">
      <header class="modal-card-head">
        <p
          class="modal-card-title"
        >
          Delete Favorite
        </p>
        <button
          class="delete"
          aria-label="close"
          @click="$emit('closeDeleteFavoriteModal')"
        />
      </header>
      <section class="modal-card-body">
        <div class="field">
          <div class="field-body">
            <div class="field">
              <p class="control">
                <strong>Are you sure you want to delete {{ favoriteName }}?</strong>
              </p>
            </div>
          </div>
        </div>
      </section>
      <footer class="modal-card-foot">
        <button
          class="button is-danger"
          @click="deleteFavorite()"
        >
          Delete
        </button>
        <button
          class="button"
          @click="$emit('closeDeleteFavoriteModal')"
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

Vue.use(VueToast)

export default {
  name: 'DeleteFavoriteModal',
  props: {
    favoriteId: {
      type: Number,
      required: true
    },
    favoriteName: {
      type: String,
      required: true
    }
  },
  methods: {
    deleteFavorite () {
      this.$store.dispatch('categoryModule/deleteFavorite', this.favoriteId)
        .then(() => {
          Vue.$toast.open({
            message: 'Favorite deleted Successfully',
            type: 'success',
            position: 'top-right'
          })
          this.$emit('closeDeleteFavoriteModal')
          this.$emit('loadFavorite')
        })
    }
  }
}
</script>
