<template>
  <v-btn :text="textButton" variant="outlined"  type="submit">
  </v-btn>
</template>

<script>
export default {
  name: "submit-button-ui",
  props: {
    textButton: {
      String,
    }
  }
}
</script>

<style scoped>

</style>
