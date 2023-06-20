<template>
  <v-list-item
    :title="`Гость`"
  />

  <v-divider></v-divider>

  <v-list density="compact" nav>
    <v-list-item prepend-icon="mdi-account-plus" title="Авторизация" value="Авторизация"
                 @click="this.$router.push({name: 'auth'})"/>
    <v-list-item prepend-icon="mdi-form-select" title="Форма" value="Форма" @click="this.$router.push({name: 'form'})"/>
  </v-list>
</template>

<script>
export default {
  name: "LeftMenuBase"
}
</script>

<style scoped>

</style>
