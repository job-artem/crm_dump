<template>
  <v-btn prepend-icon="mdi-google-plus" variant="outlined" class="text-caption">
    {{ buttonText }}
  </v-btn>
</template>

<script>
import SubmitButtonUi from "@/components/UI/SubmitButtonUI.vue";

export default {
  name: "gb-ui",
  components: {SubmitButtonUi},
  props: ['buttonText']
}
</script>

<style scoped>
</style>
