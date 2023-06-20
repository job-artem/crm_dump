<template>
  <v-card class="v-form" elevation="20">
    <v-alert
      v-if="error"
      dismissible
      type="error"
      @click="error = null"
    >
      {{ error }}
    </v-alert>
    <v-form>
      <v-card-title class="text-center v-title">Редактор профиля</v-card-title>
      <v-sheet border class="v-sheet">
        <v-text-field
          v-model="updatedUserData.first_name"
          :counter="true"
          :dense="true"
          variant="outlined"
          :maxlength="50"
          :outlined="false"
          :placeholder="'Степан'"
          :rules="[rules.minLength]"
          :type="'text'"
          clearable
          label="Имя^"
          prepend-icon="mdi-rename"

        />
        <v-text-field
          v-model="updatedUserData.last_name"
          :counter="true"
          variant="outlined"
          :dense="true"
          :maxlength="50"
          :outlined="false"
          :placeholder="'Бандера'"
          :rules="[rules.minLength]"
          :type="'text'"

          clearable
          label="Фамилия:"
          prepend-icon="mdi-rename-box-outline"
        />
        <v-text-field
          v-model="updatedUserData.phone_number"
          :counter="true"
          :dense="true"
          :maxlength="15"
          variant="outlined"
          :outlined="false"
          :placeholder="'380998877666'"
          :rules="[rules.isNumber,rules.minLengthNumber]"
          :type="'text'"
          clearable

          label="Номер телефона:"
          prepend-icon="mdi-card-account-phone"
        />
        <v-file-input
          v-model="updatedUserData.image"
          :show-size="1000"
          accept="image/*"
          label="Фото:"
          variant="outlined"
          prepend-icon="mdi-paperclip"
          clearable
        />
        <div v-if="updatedUserData.image.length > 0" style="display: grid; place-items: center">
          <v-img
            :width="150"
            aspect-ratio="16:9"
            :height="150"
            cover
            :src="imageSrc"
          />
        </div>
      </v-sheet>
    </v-form>
    <v-alert
      v-if="infoActiv"
      dense
      type="info"
    >
      Поля неизмененны. Для обновления профиля измените поля.
    </v-alert>
    <v-card-text>
      <v-row>
        <v-col cols="6">
          <v-btn variant="outlined" block @click="router.push({name: 'profile'})" class="text-caption">Назад к профилю
          </v-btn>
        </v-col>
        <v-col cols="6">
          <v-btn variant="outlined" :disabled="isActiv || isLoading" class="text-caption" block color="primary"
                 @click="updateProfile">
            <span v-if="!isLoading">Обновить профиль</span>
            <span v-else>
               <v-progress-circular color="#ffffff" indeterminate size="20"/>
            </span>
          </v-btn>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
  <v-row justify="center">
    <v-dialog
      v-model="dialog"
      persistent
      width="auto"
    >
      <v-card>
        <v-card-text>Профиль успешно обновлен.</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="green-darken-1"
            variant="text"
            @click='router.push({name: "profile"})'
          >
            Назад в профиль
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script setup>
import {useStore} from "vuex";
import {useRouter} from "vue-router";
import {computed, ref, watch} from "vue";
import axios from "axios";


const store = useStore()
const router = useRouter()
const userData = store.state.user
const updatedUserData = ref({
  first_name: userData.first_name,
  last_name: userData.last_name,
  phone_number: userData.phone_number,
  image: [],
  selected_time: [],
})

const imageSrc = computed(() => {
  if (updatedUserData.value.image.length > 0) {
    return URL.createObjectURL(updatedUserData.value.image[0])
  } else {
    return ''
  }
})
const rules = ref({
  minLength: value => {
    return !value || value.length >= 3 || 'Минимальная длинна поля составляет 3 символов.'
  },
  minLengthNumber: value => {
    return !value || value.length >= 10 || 'Минимальная длинна поля составляет 10 символов.'
  },
  isNumber: value => {
    return !value || Boolean(Number(value)) || 'Допустимы только цифры.'
  },
})
watch(updatedUserData.value, async (newValue) => {
  isActiv.value = infoActiv.value = !(await check_name(newValue.first_name, userData.first_name) || await check_name(newValue.last_name, userData.last_name) || await check_number(newValue.phone_number, userData.phone_number) || newValue.image.length > 0)
  console.log(updatedUserData.value.image)
})

const check_name = async (value_new, value_old) => {
  return value_new !== value_old && value_new && value_new.length >= 3;

}
const check_number = async (value_new, value_old) => {
  return value_new !== value_old && value_new && value_new.length >= 10 && value_new.length <= 16 && Boolean(Number(value_new))
}


const work_time = ref([])
const dialog = ref(false)
const noneData = ref('Нет информации')
const isActiv = ref(true)
const isLoading = ref(false)
const infoActiv = ref(true)
const existFieldData = ref({})
const error = ref(null)

const getCurrentUserData = async () => {
  try {
    const response = await axios.get(`user/profile/`)
    if (
      !(response.data.email === store.state.user.email &&
        response.data.first_name === store.state.user.first_name &&
        response.data.last_name === store.state.user.last_name &&
        response.data.full_name === store.state.user.full_name &&
        response.data.image === store.state.user.image &&
        response.data.phone_number === store.state.user.phone_number &&
        response.data.type === store.state.user.type)
    ) {
      store.commit('setUser', response.data)
    }
  } catch (error) {
  }
}

getCurrentUserData();
const updateProfile = () => {
  isLoading.value = true
  try {
    axios.post('user/profile/', updatedUserData.value, {headers: {'Content-Type': 'multipart/form-data'}})
    dialog.value = true
    isLoading.value = false
  } catch (error) {
  }

}


</script>

<style scoped>
.v-sheet {
  padding: 50px;
}

.v-form {
  margin-top: 3%;
  min-width: 30%;
  padding: 10px;
  margin-bottom: 30px;
}

.v-title {
  margin-top: -6%;
}

@media screen and (max-width: 800px) {
  .v-form {
    min-width: 100%;
  }

}
</style>
