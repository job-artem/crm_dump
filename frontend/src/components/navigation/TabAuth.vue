<template>
  <v-list-item
    :subtitle="user.type"
    :title="user.full_name"
  />
  <v-divider class="border-opacity-100 mr-1" vertical/>
  <v-tabs>
    <v-tab value="5"
           @click="router.push({name: 'profile'})">
      Профиль
    </v-tab>
    <v-tab value="4" @click="router.push({name: 'form'})">Форма</v-tab>
    <v-tab v-if="['Оператор', 'Администратор'].includes(user.type)"
           value="0" @click="router.push({name: 'clients-all-list'})">
      Таблица клиентов
    </v-tab>
    <v-tab v-if="['Тренер', 'Старший тренер'].includes(user.type)"
           value="1" @click="router.push({name: 'couch-new-client'})">
      Таблица новых клиентов
    </v-tab>
    <v-tab v-if="['Тренер', 'Старший тренер'].includes(user.type)"
           value="2" @click="router.push({name: 'couch-table'})">
      Отметить посещение
    </v-tab>
    <v-tab v-if="['Тренер', 'Старший тренер'].includes(user.type)"
           value="6" @click="router.push({name: 'visit-table'})">
      Таблица посещений
    </v-tab>
    <v-tab v-if="['Оператор', 'Администратор'].includes(user.type)"
           value="3" @click="router.push({name: 'client-list'})">
      Таблица новых клиентов
    </v-tab>
  </v-tabs>
  <v-spacer/>
  <v-divider class="border-opacity-100" vertical/>
  <v-tabs>
    <v-tab class="text-caption" @click="logout">
      Выйти из учетной записи
    </v-tab>
  </v-tabs>

</template>

<script setup>
import {ref} from "vue";
import {useStore} from "vuex";
import {useRouter} from "vue-router";

const router = useRouter()
const store = useStore()
const user = ref(store.state.user)
setInterval(() => {
  user.value = store.state.user
})
const logout = () => {
  localStorage.clear();
  store.commit('clearState')
}
</script>

<style scoped>

</style>
