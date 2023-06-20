<template>
  <v-responsive>
    <v-sheet style="display: grid; place-items: center">
      <v-card class="v-card-base" elevation="15" style="padding: 15px">
        <v-form @submit.prevent="submitForm">
          <v-card class="header-card" elevation="10">
            <v-card-title class="text-center text-caption">
              Записаться на тренировки
            </v-card-title>
            <v-card-text class="text-center text-caption form-description" style="margin-bottom: 15px">
              Для того чтобы начать тренироваться, заполните данную анкету.
              Свяжитесь с администратором после заполнения.
              Контактные номера: +380971916680, +380996374872, +380994687607
            </v-card-text>
          </v-card>
          <v-card class="mb-4" elevation="10">
            <v-card-title class="text-center text-caption">Персональная информация:
              <n-gradient-text type="error">
                *
              </n-gradient-text>
            </v-card-title>
            <v-card-text>
              <v-text-field
                v-model="formClient.name"
                :counter="true"
                :maxlength="50"
                :minlength="3"
                :rules="[rules.requiredField, rules.minNameLength]"
                clearable
                label="Имя"
                variant="underlined"
              />
              <v-text-field
                v-model="formClient.phone_number"
                :counter="true"
                :maxlength="50"
                :minlength="3"
                :rules="[rules.requiredField, rules.minNumberLength, rules.isNumber]"
                clearable
                label="Номер телефона"
                placeholder="380778899555"
                variant="underlined"
              />
            </v-card-text>
          </v-card>
          <v-card class="mb-4" elevation="10">
            <v-card-title class="text-center text-caption">Выберите тип тренировок:
              <n-gradient-text type="error">
                *
              </n-gradient-text>
            </v-card-title>
            <v-card-text class="text-center text-caption">
              <v-btn-toggle
                v-model="formClient.choice"
                class="text-caption mb-4"
                color="blue-accent-4"
                group
                rounded="x10"
                variant="outlined"
                @click="clear_data"
              >
                <v-btn
                  class="text-caption" round
                  value="yoga"
                >
                  Йога
                </v-btn>
                <v-btn class="text-caption"
                       round value="martialArts"
                >
                  Единоборства
                </v-btn>
              </v-btn-toggle>
            </v-card-text>
          </v-card>

          <v-card :disabled="!formClient.choice" class="mb-4" elevation="10">
            <v-card-title class="text-center text-caption">Выберите тип секции:
              <n-gradient-text type="error">
                *
              </n-gradient-text>
            </v-card-title>
            <v-card-subtitle class="text-center text-caption">
              (Возможно несколько вариантов)
            </v-card-subtitle>
            <v-card-text>
              <template v-if="formClient.choice === 'yoga'">
                <v-checkbox
                  v-for="(yoga, index) in yogaType"
                  :key="index"
                  v-model="formClient.yoga_type"
                  :label="yoga.title"
                  :value="yoga.value"
                  color="primary"
                  style="margin-bottom: -50px"
                />
                <v-select
                  v-model="formClient.yoga_type"
                  :items="yogaType"
                  chips
                  label="Выбранные секции:"
                  readonly
                  style="margin-top: 20px; margin-bottom: -25px"
                  variant="underlined"
                />
                <v-text-field
                  v-model="formClient.other_yoga_type"
                  :counter="true"
                  :maxlength="50"
                  :minlength="3"
                  label="Другие виды:"
                  variant="underlined"
                />
              </template>
              <template v-else-if="formClient.choice === 'martialArts'">
                <v-checkbox
                  v-for="(matrial_arts, index) in matrial_arts_type"
                  :key="index"
                  v-model="formClient.matrial_arts_type"
                  :label="matrial_arts.title"
                  :value="matrial_arts.value"
                  color="primary"
                  style="margin-bottom: -50px"
                />
                <v-select
                  v-model="formClient.matrial_arts_type"
                  :items="matrial_arts_type"
                  chips
                  label="Выбранные секции:"
                  readonly
                  style="margin-top: 20px; margin-bottom: -25px"
                  variant="underlined"
                />
                <v-text-field
                  v-model="formClient.other_matrial_arts_type"
                  :counter="true"
                  :maxlength="50"
                  :minlength="3"
                  label="Другие виды:"
                  variant="underlined"
                />
              </template>
              <template v-else>
                <v-card-subtitle class="text-center">
                  Секции отобразятся как только будет выбран тип тренировок.
                </v-card-subtitle>
              </template>
            </v-card-text>
          </v-card>

          <v-card :disabled="!formClient.choice" class="mb-4" elevation="10">
            <v-card-title class="text-center text-caption">Выберите тип занятий:
              <n-gradient-text type="error">
                *
              </n-gradient-text>
            </v-card-title>
            <v-card-text style="margin-bottom: 20px">
              <v-row>
                <v-col v-for="(type_group, index) in groups_type" :key="index" cols="6">
                  <v-checkbox
                    v-model="formClient.class_type"
                    :label="type_group.title"
                    :value="type_group.value"
                    color="primary"
                    style="margin-bottom: -50px"
                  />
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>

          <v-card :disabled="!formClient.choice" class="mb-4" elevation="10">
            <v-card-title class="text-center text-caption">Возрастная категория занятий:
              <n-gradient-text type="error">
                *
              </n-gradient-text>
            </v-card-title>
            <v-card-text style="margin-bottom: 30px">
              <v-row>
                <v-col v-for="(age, index) in ages" :key="index" cols="4">
                  <v-checkbox
                    v-model="formClient.age"
                    :label="age.title"
                    :value="age.value"
                    color="primary"
                    style="margin-bottom: -70px"
                  />
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>

          <v-card :disabled="!formClient.choice" class="mb-4" elevation="10">
            <v-card-title class="text-center text-caption">Выберите локацию для тренировок:
              <n-gradient-text type="error">
                *
              </n-gradient-text>
            </v-card-title>
            <v-card-subtitle class="text-center text-caption">
              (Возможно несколько вариантов)
            </v-card-subtitle>
            <v-card-text>
              <v-row>
                <v-col v-for="(loc, index) in location" :key="index" :cols="height > 500 ? 4 : height > 220 ? 6 : 7">
                  <v-checkbox
                    v-model="formClient.training_location"
                    :label="loc.title"
                    :value="loc.value"
                    color="primary"
                    style="margin-bottom: -50px"
                  />
                </v-col>
              </v-row>
              <v-select
                v-model="formClient.training_location"
                :items="location"
                chips
                label="Выбранные локации для тренировок:"
                readonly
                style="margin-top: 20px; margin-bottom: -25px"
                variant="underlined"
              />
              <v-text-field
                v-model="formClient.other_location"
                :counter="true"
                :maxlength="50"
                :minlength="3"
                label="Другие локации:"
                variant="underlined"
              />
            </v-card-text>
          </v-card>
          <v-card :disabled="!formClient.choice" class="mb-4" elevation="10">
            <v-card-title class="text-center text-caption">Выберите день посещения:
              <n-gradient-text type="error">
                *
              </n-gradient-text>
            </v-card-title>
            <v-card-subtitle class="text-center text-caption">
              (Возможно несколько вариантов)
            </v-card-subtitle>
            <v-card-text>
              <v-row>
                <v-col v-for="(day, index) in visit_day" :key="index" :cols="height > 220 ? 6 : 12">
                  <v-checkbox
                    v-model="formClient.visit_day"
                    :label="day.title"
                    :value="day.value"
                    color="primary"
                    style="margin-bottom: -65px"
                  />
                </v-col>
              </v-row>
              <v-select
                v-model="formClient.visit_day"
                :items="visit_day"
                chips
                label="Выбранные дни тренировок:"
                readonly
                style="margin-top: 45px"
                variant="underlined"
              />
            </v-card-text>
          </v-card>
          <v-card :disabled="!formClient.choice" class="mb-4" elevation="10">
            <v-card-title class="text-center text-caption">Выберите время посещения:
              <n-gradient-text type="error">
                *
              </n-gradient-text>
            </v-card-title>
            <v-card-subtitle class="text-center text-caption">
              (Возможно несколько вариантов)
            </v-card-subtitle>
            <v-card-text>
              <v-row>
                <v-col v-for="(tm, index) in time" :key="index" :cols="height > 500 ? 2 : height > 220 ? 3 : 6">
                  <v-checkbox
                    v-model="formClient.training_time"
                    :label="tm.title"
                    :value="tm.value"
                    color="primary"
                    style="margin-bottom: -70px"
                  />
                </v-col>
              </v-row>
              <v-select
                v-model="formClient.training_time"
                :items="time"
                chips
                label="Выбранное время для тренировок:"
                readonly
                style="margin-top: 35px; margin-bottom: -25px"
                variant="underlined"
              />
            </v-card-text>
          </v-card>

          <v-card class="mb-4" elevation="10">
            <v-card-actions class="mt-2 mb-2" style="display: grid; place-items: center">
              <v-btn v-if="!allert" :disabled="allert" block class="text-success text-caption text-capitalize" type="submit"
                     variant="outlined">
                Отправить форму
              </v-btn>
              <v-btn v-if="allert" block class="text-success text-caption text-capitalize" @click="dialog_error = true"
                     variant="outlined">
                Отправить форму
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-form>
        <div class="text-center">
          <v-dialog
            v-model="dialog_error"
            width="auto"
          >
            <v-card>
              <v-card-text>
                <v-alert icon="$error" title="Ошибка при заполнении формы." type="error" variant="outlined">
                  <p v-if="!formClient.name"> Поле "Имя" обязательно к заполнению.</p>
                  <p v-if="formClient.name && formClient.name.length >= 1 && formClient.name.length < 3">Минимальная
                    длинна поля "Имя" 3
                    символа.
                  </p>
                  <p v-if="!formClient.phone_number"> Поле "Телефон" обязательно к заполнению.</p>
                  <n-ul>
                    <n-li
                      v-if="formClient.phone_number && formClient.phone_number.length >= 1 && formClient.phone_number.length < 10">
                      Минимальная
                      длинна поля "Телефон" 10 символов.
                    </n-li>
                    <n-li
                      v-if="formClient.phone_number && formClient.phone_number.length > 1 && !Boolean(Number(formClient.phone_number))">
                      В поле
                      "Телефон" допустимы только цифры.
                    </n-li>
                  </n-ul>
                  <p v-if="!formClient.choice">Вы не выбрали тип тренировки.</p>
                  <p v-if="formClient.choice && allert && base_allert">Вы не выбрали:</p>
                  <n-ul v-if="formClient.choice">
                    <n-li
                      v-if="formClient.choice === 'yoga' && formClient.yoga_type.length === 0 && formClient.other_yoga_type.length === 0">
                      Тип секции для тренировок.
                    </n-li>
                    <n-li
                      v-if="formClient.choice === 'martialArts' && formClient.matrial_arts_type.length === 0 && formClient.other_matrial_arts_type.length === 0">
                      Тип секции для тренировок.
                    </n-li>
                    <n-li v-if="formClient.choice && formClient.age.length === 0">Возрастную категорию
                      тренировок.
                    </n-li>
                    <n-li v-if="formClient.other_location.length === 0 && formClient.training_location.length ===0">
                      Локацию для занятий.
                    </n-li>
                    <n-li v-if="formClient.training_time.length === 0">
                      Время занятий.
                    </n-li>
                    <n-li v-if="!formClient.class_type">
                      Тип занятий.
                    </n-li>
                    <n-li v-if="formClient.visit_day.length === 0">
                      День посещения занятий.
                    </n-li>
                  </n-ul>
                </v-alert>
              </v-card-text>
              <v-card-actions>
                <v-btn block color="error" @click="dialog_error = false">Закрыть</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </div>
        <div class="text-center">
          <v-dialog
            v-model="dialog"
            width="auto"
          >
            <v-card>
              <v-card-text>
                Форма успешно заполнена и отправлена!
              </v-card-text>
              <v-card-actions>
                <v-btn block color="primary" @click="dialog = false">Подтвердить</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </div>
      </v-card>
    </v-sheet>
  </v-responsive>
</template>

<script setup>
import {computed, ref, watch} from "vue";
import axios from "axios";
import {useDisplay} from "vuetify";

const yogaType = ref([])
const matrial_arts_type = ref([])
const visit_day = ref([])
const location = ref([])
const groups_type = ref('')
const ages = ref([])
const time = ref([])
const allert = ref(true)
const base_allert = ref(true)
const dialog = ref(false)
const dialog_error = ref(false)
const rules = ref(
  {
    requiredField: value => !!value || 'Обязательное поле.',
    minNameLength: value => {
      return value.length >= 3 || 'Минимальная длинна поля 3 символов.'
    },
    minNumberLength: value => {
      return value.length >= 10 || 'Минимальная длинна поля 10 символов.'
    },
    isNumber: value => {
      return !value || Boolean(Number(value)) || 'Допустимы только цифры.'
    }
  }
)
const {name} = useDisplay()
const height = computed(() => {
  switch (name.value) {
    case 'xs':
      return 220
    case 'sm':
      return 400
    case 'md':
      return 500
    case 'lg':
      return 600
    case 'xl':
      return 800
    case 'xxl':
      return 1200
  }

  return undefined
})

const formClient = ref({
  choice: false,
  name: null,
  phone_number: null,
  class_type: '',
  training_location: [],
  other_location: '',
  training_time: [],
  visit_day: [],
  yoga_type: [],
  age: '',
  other_yoga_type: '',
  matrial_arts_type: [],
  other_matrial_arts_type: '',
})
const clear_data = async () => {
  formClient.value.matrial_arts_type = []
  formClient.value.yoga_type = []
  formClient.value.other_yoga_type = ''
  formClient.value.other_matrial_arts_type = ''
}
const clear_all_data = async () => {
  formClient.value.choice = false
  formClient.value.name = null
  formClient.value.phone_number = null
  formClient.value.class_type = ''
  formClient.value.training_location = []
  formClient.value.other_location = ''
  formClient.value.training_time = []
  formClient.value.visit_day = []
  formClient.value.age = ''
  formClient.value.matrial_arts_type = []
  formClient.value.yoga_type = []
  formClient.value.other_yoga_type = ''
  formClient.value.other_matrial_arts_type = ''
}
const fetchData = async () => {
  try {
    const response = await axios.get('forms/')
    yogaType.value = response.data.yoga_type
    matrial_arts_type.value = response.data.matrial_arts_type
    visit_day.value = response.data.days
    time.value = response.data.time
    location.value = response.data.location
    ages.value = response.data.age
    groups_type.value = response.data.groups_type
  } catch (_) {

  }
}
fetchData()

const submitForm = async () => {
  try {
    await axios.post('forms/', {data: formClient.value})
    dialog.value = true
    await clear_all_data()
  } catch (_) {

  }
}

watch(formClient, async () => {
  allert.value = !(
    formClient.value.choice && formClient.value.age.length !== 0 &&
    formClient.value.class_type.length !== 0 &&
    (
      (formClient.value.yoga_type.length !== 0 || formClient.value.other_yoga_type.length !== 0) ||
      (formClient.value.matrial_arts_type.length !== 0 || formClient.value.other_matrial_arts_type.length !== 0)
    ) &&
    formClient.value.training_time.length !== 0 && (
      formClient.value.training_location.length !== 0 ||
      formClient.value.other_location.length !== 0
    ) &&
    formClient.value.name && formClient.value.name.length >= 3 &&
    formClient.value.phone_number && formClient.value.phone_number.length >= 10 && Boolean(Number(formClient.value.phone_number))
  )
  base_allert.value = !(
    formClient.value.choice && formClient.value.age.length !== 0 &&
    formClient.value.class_type.length !== 0 &&
    (
      (formClient.value.yoga_type.length !== 0 || formClient.value.other_yoga_type.length !== 0) ||
      (formClient.value.matrial_arts_type.length !== 0 || formClient.value.other_matrial_arts_type.length !== 0)
    ) &&
    formClient.value.training_time.length !== 0 && formClient.value.training_location.length !== 0
  )
}, {deep: true});
</script>

<style scoped>

.v-card-base {
  margin-bottom: 50px;
  padding: 10px;
  max-width: 40%;
}

@media screen and (max-width: 800px) {
  .v-card-base {
    max-width: 100%;
  }

}

.header-card {
  margin-bottom: 15px;
}
</style>
