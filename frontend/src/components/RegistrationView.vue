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
    <v-alert
      v-if="success"
      :title="successTitle"
      dismissible
      type="success"
      variant="tonal"
      style="min-width: 100%"
      @click="success = null"
    ></v-alert>
  </v-container>
  <v-form fast-fail @submit.prevent="submitForm" >
    <v-sheet rounded>
      <v-text-field
        v-model="formData.first_name"
        :dense="true"
        :label="'Имя:'"
        prepend-icon="mdi-account-outline"
        :maxlength="50"
        :minlength="5"
        variant="outlined"
        :placeholder="'Stepan'"
        :rules="[rules.requiredField, rules.minLengthUsername]"
        :type="'text'"
        clearable
      />
      <v-text-field
        v-model="formData.last_name"
        :counter="true"
        :dense="true"
        :label="'Фамилия:'"
        prepend-icon="mdi-account"
        :maxlength="50"
        :minlength="5"
        variant="outlined"
        :placeholder="'Bandera'"
        :rules="[rules.requiredField, rules.minLengthUsername]"
        :type="'text'"
        clearable
      />
      <v-text-field
        v-model="formData.email"
        :dense="true"
        :label="'Почта:'"
        :maxlength="50"
        :minlength="5"
        variant="outlined"
        prepend-icon="mdi-email"
        :placeholder="'your.best.email@example.com'"
        :rules="[rules.requiredField, rules.minLengthEmail, rules.email]"
        :type="'email'"
        clearable
      />
      <v-text-field
        v-model="formData.password"
        :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
        :counter="true"
        :dense="true"
        :label="'Пароль:'"
        :maxlength="50"
        :minlength="8"
        variant="outlined"
        prepend-icon="mdi-lock-outline"
        :rules="[rules.requiredField, rules.minLengthPassword, rules.passwordConfirmEqual, rules.englishLettersOnly]"
        :type="showPassword ? 'text' : 'password'"
        :value="formData.password"
        clearable
        @click:append-inner="showPassword = !showPassword"
      />
      <v-text-field
        v-model="formData.confirm_password"
        :append-inner-icon="showConfirmPassword ? 'mdi-eye' : 'mdi-eye-off'"
        :dense="true"
        :label="'Подтверждение пароля:'"
        :maxlength="50"
        :minlength="8"
        variant="outlined"
        prepend-icon="mdi-lock"
        :rules="[rules.requiredField, rules.minLengthPassword, rules.passwordConfirmEqual, rules.englishLettersOnly]"
        :type="showConfirmPassword ? 'text' : 'password'"
        :value="formData.confirm_password"
        clearable
        @click:append-inner="showConfirmPassword = !showConfirmPassword"
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
    <div class="google-reg-wrapper">
      <google-registration @registration-failed="handleRegistrationFailed"
                           @registration-successful="handleRegistrationSuccessful"/>
    </div>
  </v-form>
</template>

<script>
import {email, minLength, required, sameAs} from "@vuelidate/validators";
import {useVuelidate} from "@vuelidate/core";
import axios from "axios";
import {useRouter} from "vue-router";
import GoogleRegistration from "@/components/GoogleRegistration.vue";
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
  name: "RegistrationView",
  components: {SubmitButtonUi, GoogleRegistration},
  setup() {
    const v$ = useVuelidate()
    const router$ = useRouter()

    return {
      v$,
      router$,
    }
  },
  data() {
    return {
      formData: {
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        confirm_password: '',
      },
      error: null,
      errorTitle: null,
      success: null,
      successTitle: null,
      showPassword: false,
      showConfirmPassword: false,
      rules: {
        requiredField: value => !!value || 'Обязательное поле.',
        email: value => {
          return emailPattern.test(value) || 'Невалидная почта.'
        },
        minLengthUsername: value => {
          return value.length >= 3 || 'Минимальная длинна поля 3 символов.'
        },
        minLengthEmail: value => {
          return value.length >= 5 || 'Минимальная длинна почты 5 символов.'
        },
        englishLettersOnly: value => {
          const englishLettersOnlyRegex = /^[a-zA-Z0-9!@#$%^&*()_+\-=[\]{};:\\|,.<>/?]+$/
          return englishLettersOnlyRegex.test(value) || 'Пароль должен содержать только буквы английского алфавита.'
        },
        minLengthPassword: value => {
          return value.length >= 8 || 'Минимальная длинна пароля 8 символов.'
        },
        uppercaseRegex: value => {
          const uppercaseRegex = /[A-Z]+/
          return uppercaseRegex.test(value) || 'Пароль должен содержать хотя бы одну букву верхнего регистра.'
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
        passwordConfirmEqual: value => {
          if (this.formData.password) {
            return this.formData.password === value || 'Пароли не совпадают.'
          }
        }
      },
      loading: false
    }
  },
  validations() {
    return {
      formData: {
        first_name: {
          required: required,
          minLength: minLength(5)
        },
        last_name: {
          required: required,
          minLength: minLength(5)
        },
        email: {
          required: required,
          email: email,
          minLength: minLength(5),
          emailValidate
        },
        password: {
          required: required,
          minLength: minLength(8),
          // passwordValidate
        },
        confirm_password: {
          required: required,
          minLength: minLength(8),
          // passwordValidate,
          sameAs: sameAs(this.formData.password)
        }
      }
    }
  }
  ,
  methods: {
    async submitForm() {
      this.loading = true
      await this.clearSuccessError()
      this.v$.$touch()
      if (this.v$.$invalid) {
        this.errorTitle = 'Форма не валидна.'
        this.error = 'Проверьте данные в форме.'
        this.loading = false
        return
      }
      try {
        await axios.post("registration/", this.formData)
        await this.showThen()
      } catch (error) {
        await this.showCatch(error)
      }

    },
    async clearForm() {
      this.formData = {
        first_name: null,
        last_name: null,
        email: null,
        password: null,
        confirm_password: null,
      }
    },
    async showThen() {
      await this.clearSuccessError()
      this.successTitle = 'Регистрация успешна!'
      this.success = 'Вы успешно зарегистрировались, сейчас вам на почту было отправлено письмо для активации вашего аккаунта на сайте.'
      await this.clearForm()
      this.loading = false
    },
    async clearSuccessError() {
      this.error = this.errorTitle = null
      this.successTitle = this.success = null
    },
    async showCatch(response) {
      await this.clearSuccessError()
      this.errorTitle = 'Ошибка регистрации.'
      if (response.code === 'ERR_NETWORK' || response.request.status === 500) {
        this.errorTitle = 'Ошибка сервера'
        this.error = 'Сервер не отвечает, попробуйте повторить действие позже.'
      } else {
        const status = response.request.status
        const error = response.response.data.error
        if (status === 400 && error === 'UserExist') {
          this.error = 'Пользователь с таким Email уже существует.'
        } else if (status === 400 && error === 'InvalidPassword') {
          this.error = 'Введен некорректный пароль.'
        }
      }
      this.loading = false
    },
    async handleRegistrationSuccessful() {
      await this.showThen()
    },
    async handleRegistrationFailed(error) {
      await this.showCatch(error)
    },


  }
}
</script>

<style scoped>

.input-wrapper {
  min-width: 90%;
  margin-bottom: 1.5rem;
}

.submit-button-wrapper {
  z-index: 2;
  text-align: center;
}

.divider-wrapper {
  display: flex;
  align-items: center;
  margin: 0.5rem 0;
}

.divider {
  flex: 1;
  margin: 0 0.25rem;
  min-width: 150px;
}

.divider-text {
  margin: 0;
  font-size: 0.875rem;
  font-weight: 600;
  color: #6c757d;
  text-transform: uppercase;
}

.google-reg-wrapper {
  z-index: 1;
  display: flex;
  justify-content: center;
  margin-top: 1.5rem;
}


.custom-loader {
  animation: loader 1s infinite;
  display: flex;
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
