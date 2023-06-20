<template>
  <v-footer class="bg-grey-lighten-1 v-footer">
    <v-row justify="center" no-gutters>
      <v-btn
        v-for="link in links"
        :key="link"
        class="mx-2"
        color="white"
        rounded="xl"
        variant="text"
      >
        {{ link }}
      </v-btn>
      <v-col class="text-center mt-4" cols="12">
        {{ new Date().getFullYear() }} — <strong>Vuetify</strong>
      </v-col>
    </v-row>
  </v-footer>
</template>

<script>
export default {
  name: "FooterComponent",
  data() {
    return {
      links: [
        'Home',
        'About Us',
        'Team',
        'Services',
        'Blog',
        'Contact Us',
      ],
    }
  }
}

</script>

<style scoped>
.v-footer {
  position: fixed;
  bottom: 0;
  width: 100%;
  height: 64px;
}

body {
  padding-bottom: 64px;
}
</style>
