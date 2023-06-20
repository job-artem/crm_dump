<template>
  <v-card rounded elevation="15" class="v-card">
    <v-card-title class="text-center">{{ showLogin ? 'Авторизация' : 'Регистрация' }}</v-card-title>
    <v-card-text>

      <v-sheet border rounded class="v-sheet-form">
        <login-view v-if="showLogin"/>
        <registration-view v-else/>
      </v-sheet>

    </v-card-text>
    <v-card-actions class="justify-center text-center" style="margin-bottom: 20px">
      <v-card-text>
        {{ showLogin ? 'Нет аккаунта?' : 'Есть аккаунт?' }}
        <v-btn class="text-caption" variant="tonal" @click="toggleLogin">
          {{ showLogin ? 'Зарегистрироваться' : 'Войти' }}
        </v-btn>
      </v-card-text>
    </v-card-actions>
  </v-card>
</template>

<script setup>
import {useStore} from 'vuex'
import {useRouter} from 'vue-router'
import LoginView from '@/components/LoginView.vue'
import RegistrationView from '@/components/RegistrationView.vue'
import {ref} from "vue";

const store = useStore()
const router = useRouter()
const showLogin = ref(true)

function toggleLogin() {
  showLogin.value = !showLogin.value
}

if (store.state.user) {
  router.push({name: 'profile'})
}
</script>


<style scoped>
.v-card {
  margin-top: 2%;
  margin-bottom: 20px;
  min-width: 100%;
}

@media screen and (min-width: 800px) {
  .v-card {
    min-width: 30%;
  }
}

.v-sheet-form {
  padding: 10px;
}
</style>
