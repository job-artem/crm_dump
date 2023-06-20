<template>
  <v-list-item
    :subtitle="user.type"
    :title="user.full_name"
  />

  <v-divider></v-divider>

  <v-list density="compact" nav>
    <v-list-item v-if="['Оператор', 'Администратор'].includes(user.type)"
                 prepend-icon="mdi-view-dashboard-outline" title="Таблица клиентов"
                 value="Таблица клиентов" @click="this.$router.push({name: 'clients-all-list'})"/>

    <v-list-item v-if="['Тренер', 'Старший тренер'].includes(user.type)"
                 prepend-icon="mdi-view-dashboard-outline" title="Таблица новых клиентов"
                 value="Таблица новых клиентов" @click="this.$router.push({name: 'couch-new-client'})"/>


    <v-list-item v-if="['Тренер', 'Старший тренер'].includes(user.type)"
                 prepend-icon="mdi-view-dashboard" title="Отметить посещение"
                 value="Таблица" @click="this.$router.push({name: 'couch-table'})"/>
    <v-list-item v-if="['Тренер', 'Старший тренер'].includes(user.type)"
                 prepend-icon="mdi-view-dashboard" title="Таблица посещений"
                 value="Таблица" @click="this.$router.push({name: 'visit-table'})"/>

    <v-list-item v-if="['Оператор', 'Администратор'].includes(user.type)"
                 prepend-icon="mdi-view-dashboard" title="Таблица новых клиентов"
                 value="Таблица новых клиентов" @click="this.$router.push({name: 'client-list'})"/>

    <v-list-item prepend-icon="mdi-form-select" title="Форма" value="Форма" @click="this.$router.push({name: 'form'})"/>

    <v-list-item prepend-icon="mdi-account-circle" title="Профиль" value="Профиль"
                 @click="this.$router.push({name: 'profile'})"/>

  </v-list>
</template>

<script>

import {useStore} from "vuex";

export default {
  name: "LeftMenuAuth",
  setup() {
    return {
      store: useStore(),
    }
  }
  ,
  data() {
    return {
      user: this.store.state.user,
    }
  },
  mounted() {
    setInterval(() => {
      if (this.user.image !== this.store.state.user.image) {
        this.user = this.store.state.user
      }
    })
  }


}
</script>

<style scoped>

</style>
