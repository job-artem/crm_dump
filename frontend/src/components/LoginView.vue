<template>
  <v-container>
    <v-alert
      v-if="error"
      :title="errorTitle"
      dismissible
      type="error"
      variant="tonal"
      style="min-width: 100%"
      @click="error = null"
    >
      {{ error }}
    </v-alert>
  </v-container>
  <v-form fast-fail @submit.prevent="submitForm">
    <v-sheet rounded>
      <v-text-field
        v-model="formData.email"
        prepend-icon="mdi-email"
        :dense="true"
        label="Почта:"
        :outlined="false"
        variant="outlined"
        :placeholder="'your.best.email@example.com'"
        :rules="[rules.requiredField, rules.email, rules.minLengthEmail]"
        :type="'email'"
        clearable
      />
      <v-text-field
        v-model="formData.password"
        prepend-icon="mdi-lock"
        :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
        :dense="true"
        label='Пароль:'
        variant="outlined"
        :rules="[rules.requiredField, rules.minLengthPassword, rules.passwordConfirmEqual, rules.englishLettersOnly]"
        :type="showPassword ? 'text' : 'password'"
        :value="formData.password"
        clearable
        @click:append-inner="showPassword = !showPassword"
      />
    </v-sheet>
    <v-divider
      class="border-opacity-100"
    />
    <v-container>
      <submit-button-ui class="text-caption" :disabled="loading" :loading="loading" color="primary"
                        v-text="'Подтвердить'"/>
    </v-container>
    <div class="d-flex justify-content-center align-items-center">
        <v-divider class="border-opacity-100" style="margin-top: 10px"/>
      <span style="margin-left: 10px; margin-right: 10px">Или</span>
      <v-divider class="border-opacity-100" style="margin-top: 10px"/>
    </div>
    <div class="google-auth-wrapper">
      <google-auth @login-failed="handleLoginFailed" @login-successful="handleLoginSuccessful"/>
    </div>
  </v-form>


</template>

<script>
import {email, minLength, required} from "@vuelidate/validators";
import {useVuelidate} from "@vuelidate/core";
import axios from "axios";
import {mapMutations, useStore} from "vuex";
import {useRouter} from "vue-router";
import GoogleAuth from "@/components/GoogleAuth.vue";
import SubmitButtonUi from "@/components/UI/SubmitButtonUI.vue";

const emailPattern = /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/
const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*? ])[a-zA-Z0-9!@#$%^&*? ]{8,}$/


const emailValidate = (value) => {
  return emailPattern.test(value)
}
const passwordValidate = (value) => {
  return passwordPattern.test(value)
}
export default {
  name: "LoginView",
  components: {SubmitButtonUi, GoogleAuth},
  setup() {
    const store = useStore();
    const router = useRouter();
    setInterval(() => {
      if (store.state.user && router.currentRoute.value.fullPath === '/auth') {
        router.push({name: 'profile'})
      }
    })
    return {
      v$: useVuelidate(),
      MutationCommand: mapMutations(['clearState']),
      store,
      router
    }
  },
  data() {
    return {
      formData: {
        email: '',
        password: '',
      },
      showPassword: false,
      rules: {
        requiredField: value => !!value || 'Обязательное поле.',
        email: value => {
          return emailPattern.test(value) || 'Невалидная почта.'
        },
        minLengthEmail: value => {
          return value.length >= 5 || 'Минимальная длинна почты 5 символов.'
        },
        minLengthPassword: value => {
          return value.length >= 8 || 'Минимальная длинна пароля 8 символов.'
        },
        uppercaseRegex: value => {
          const uppercaseRegex = /[A-Z]+/
          return uppercaseRegex.test(value) || 'Пароль должен содержать хотя бы одну букву верхнего регистра.'
        },
        englishLettersOnly: value => {
          const englishLettersOnlyRegex = /^[a-zA-Z0-9!@#$%^&*()_+\-=[\]{};:\\|,.<>/?]+$/
          return englishLettersOnlyRegex.test(value) || 'Пароль должен содержать только буквы английского алфавита.'
        },
        lowercaseRegex: value => {
          const lowercaseRegex = /[a-z]+/
          return lowercaseRegex.test(value) || 'Пароль должен содержать хотя бы одну букву нижнего регистра.'
        },
        numberRegex: value => {
          const numberRegex = /[0-9]+/
          return numberRegex.test(value) || 'Пароль должен содержать хотя бы одну цифру.'
        },
        specialCharRegex: value => {
          const specialCharRegex = /[^A-Za-z0-9]+/
          return specialCharRegex.test(value) || 'Пароль должен содержать хотя бы один специальный символ.'
        },
      },
      loading: false,
      error: null,
      errorTitle: null,
    }
  },
  validations() {
    return {
      formData: {
        email: {
          required: required,
          email,
          emailValidate
        },
        password: {
          required: required,
          minLengthPassword: minLength(8),
          // passwordValidate
        }
      }
    }
  },
  mounted() {
    this.v$.$touch()
  },
  methods: {
    async submitForm() {
      await this.clearSuccessError()
      this.loading = true
      if (this.v$.$invalid) {
        this.errorTitle = 'Форма не валидна.'
        this.error = 'Проверьте данные в форме.'
        this.loading = false
        return
      }
      axios.defaults.headers['Authorization'] = ''
      try {
        const response = await axios.post('login/', this.formData)
        await this.handleLoginSuccessful(response.data)
      } catch (error) {
        await this.showCatch(error)
      }
    },
    async clearSuccessError() {
      this.error = this.errorTitle = null
    },
    async handleLoginSuccessful(data) {
      this.$store.commit('setAccess', data.access);
      this.$store.commit('setRefresh', data.refresh);
      this.$store.commit('setLogout', true);
      localStorage.setItem('refresh', data.refresh);
      this.loading = false
      await this.router.push({name: 'profile'})
    },
    async handleLoginFailed(error) {
      await this.showCatch(error)
    },
    async showCatch(response) {
      this.errorTitle = 'Ошибка авторизации.'
      if (response.code === 'ERR_NETWORK' || response.request.status === 500) {
        this.errorTitle = 'Ошибка сервера'
        this.error = 'Сервер не отвечает, попробуйте повторить действие позже.'
      } else {
        const status = response.request.status
        const error = response.response.data.error ? response.response.data.error : response.response.data.code
        if ([400, 401].includes(status) && ['UserDoesNotExist', "user_not_found"].includes(error)) {
          this.error = 'Пользователь с таким Email не существует.'
        } else if (status === 400 && error === 'UserInactive') {
          this.error = 'Пользователь не активировал аккаунт, проверьте почту.'
        } else if (status === 400 && error === 'InvalidPassword') {
          this.error = 'Неверный пароль.'
        }
      }
      this.loading = false
    },
  },
}
</script>

<style scoped>


.google-auth-wrapper {
  z-index: 1;
  display: flex;
  justify-content: center;
  margin-top: 1.5rem;
}


@-moz-keyframes loader {
  from {
    transform: rotate(0);
  }
  to {
    transform: rotate(360deg);
  }
}

@-webkit-keyframes loader {
  from {
    transform: rotate(0);
  }
  to {
    transform: rotate(360deg);
  }
}

@-o-keyframes loader {
  from {
    transform: rotate(0);
  }
  to {
    transform: rotate(360deg);
  }
}

@keyframes loader {
  from {
    transform: rotate(0);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
