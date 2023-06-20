<template>
  <v-list-item
    :title="`Гость`"
  />
  <v-divider class="border-opacity-100 mr-1" vertical/>
  <v-tabs v-model="base_tab">
    <v-tab value="0"
           @click="router.push({name: 'auth'})">
      Авторизация
    </v-tab>
    <v-tab value="1"
           @click="router.push({name: 'form'})">
      Форма
    </v-tab>
  </v-tabs>
</template>

<script setup>
import {ref, watch} from "vue";
import {useRouter} from "vue-router";

const base_tab = ref(localStorage.getItem('base_tab') || null)
watch(base_tab, async (newValue) => {
  localStorage.setItem('base_tab', newValue)
})
const router = useRouter()
</script>

<style scoped>

</style>
