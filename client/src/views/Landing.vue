<template>
  <div class="landing__image">
    <nav
      class="navbar"
      role="navigation"
      aria-label="main navigation"
    >
      <div class="navbar-brand">
        <h1>FAVORITE THINGS</h1>
      </div>

      <div
        id="navbarBasicExample"
        class="navbar-menu"
      >
        <div class="navbar-end">
          <div class="navbar-item">
            <div class="buttons">
              <router-link
                to="/categories"
                class="button is-primary"
              >
                <strong>Get Started</strong>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </nav>
  </div>
</template>

<script>
export default {
  name: 'Landing'
}
</script>

<style scoped>
  h1 {
    margin-left: 15px;
  }
</style>
