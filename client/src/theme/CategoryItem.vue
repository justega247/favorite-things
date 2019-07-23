<template>
  <div class="card">
    <div class="card-content">
      <p class="title is-centered">
        <slot name="category" />
      </p>
    </div>
    <footer class="card-footer">
      <a
        class="card-footer-item"
        :href="link"
      >
        <slot name="favorite" />
      </a>
    </footer>
  </div>
</template>
<script>
export default {
  props: ['link']
}
</script>
<style scoped>
  .card {
    padding-bottom: 40px;
    height: 100%;
    box-shadow: 2px 4px 10px rgba(0,0,0, .2);
    border-radius: 0.3125rem;
  }
  footer {
    position: absolute;
    bottom: 0;
    width: 100%;
    left: 0;
  }
  .card-content {
    background-color: transparent;
    padding: 1.5rem;
    text-align: center;
  }
  .card-footer a {
    font-size: small;
  }
</style>
