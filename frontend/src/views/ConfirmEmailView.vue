<template>
  <v-container class="confirmPage" fluid>
    <v-form class="confirm-body">
      <v-col>
        <v-card class="mx-auto">
          <v-card-title class="text-center">Активация аккаунта</v-card-title>
          <v-card-text class="text-center">
            <v-container>
              <v-row>
                <v-col v-if="message" cols="12">
                  <p>{{ message }} </p>
                  <br/>
                  <v-btn class="" @click="$router.push({name: 'auth'})" v-text="'На страницу авторизации'"/>
                </v-col>
                <v-col v-if="error" cols="12">
                  <p>{{ error }}</p>
                  <br/>
                  <v-btn class="" @click="$router.push({name: 'auth'})" v-text="'На страницу авторизации'"/>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
        </v-card>
      </v-col>
    </v-form>
  </v-container>
</template>

<script>
import axios from "axios";
import InputUi from "../components/UI/InputUI.vue";
import LoginView from "../components/LoginView.vue";
import RegistrationView from "../components/RegistrationView.vue";

export default {
  name: "ConfirmEmailView",
  components: {RegistrationView, LoginView, InputUi},
  data() {
    return {
      message: '',
      error: ''
    }
  },
  mounted() {
    const confirmationToken = window.location.pathname.split('/')[2];
    const confirmResponse = async () => {
      try {
        await axios.post(`confirm/`, {token: confirmationToken})
        this.message = 'Аккаунт успешно активирован!'
      } catch (_) {
        this.error = 'Невалидный токен активации аккаунта!'
      }
    }
    confirmResponse()
  },
}

</script>

<style scoped>
.confirmPage {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 50vh;
}

.confirm-body {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  max-width: 100%;
  position: relative;
}

</style>