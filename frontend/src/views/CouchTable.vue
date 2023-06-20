<template>
  <v-responsive>
    <v-sheet :class="`ml-${height > 220 ? 5 : 0} mr-${height > 220 ? 5 : 0} mt-2 mb-5` " style="padding: 10px;">
      <v-card class="v-card-base" elevation="20">
        <v-card-title v-if="height > 220">
          Отметить посещение за: {{ currentDate }}
        </v-card-title>
        <v-card-title v-if="height === 220">
          Отметить посещение за:
        </v-card-title>
        <v-card-title v-if="height === 220">
          {{ currentDate }}
        </v-card-title>
        <v-card-text>
          <n-space justify="space-between">
            <v-btn :loading="button_update" class="text-caption mb-1" variant="outlined" @click="fetchData">
              Обновить таблицу
            </v-btn>
          </n-space>
        </v-card-text>
        <v-data-table
          :headers="createColumns"
          :items="data"
          density="compact"
        >
          <template v-slot:item.fullname="{ item }">
            <v-text-field v-model="item.props.title.fullname" density="compact" style="min-width: 200px"
                          variant="underlined"/>
          </template>
          <template v-slot:item.exist="{ item }">
            <v-checkbox-btn v-model="item.props.title.exist" color="green" density="compact"/>
          </template>
          <template v-slot:item.status="{ item }">
            <v-select v-model="item.props.title.status" :disabled="!item.props.title.exist" :items="status"
                      density="compact" style="width: 200px"
                      variant="underlined"/>
          </template>
          <template v-slot:item.payed="{ item }">
            <v-text-field v-model="item.props.title.payed" :disabled="!item.props.title.exist" density="compact"
                          type="number" variant="underlined"/>
          </template>
          <template v-slot:item.info="{ item }">
            <v-text-field v-model="item.props.title.info" :disabled="!item.props.title.exist"  variant="underlined" density="compact"/>
          </template>
        </v-data-table>

        <v-card-text style="display: grid; place-items: center">
          <n-space justify="space-between">
            <v-btn :disabled="data.length === 0" :loading="button_submit" append-icon="mdi-account-plus-outline"
                   class="text-caption mb-1"
                   variant="outlined" @click="submit">
              Сохранить и отправить
            </v-btn>
          </n-space>
        </v-card-text>

      </v-card>
    </v-sheet>
  </v-responsive>
</template>
<script setup>

import {computed, ref} from "vue";
import axios from "axios";
import {useDisplay} from "vuetify";
import {VDataTable} from "vuetify/labs/components";

const button_submit = ref(false)
const button_update = ref(false)

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
const loading = ref(true)
const data = ref([])

const currentDate = ref(new Date().toLocaleDateString("ru-RU", {
  day: "numeric",
  month: "long",
  year: "numeric",
}))
const status = ref([])
const createColumns = ref([
  {title: "Фамилия Имя", key: "fullname",},
  {title: "Посещение", key: "exist",},
  {title: "Оплата", key: "payed"},
  {title: "Статус оплаты", key: "status"},
  {title: "Текущий статус", key: "payed_status"},
  {title: "Доп информация", key: "info",}
])
const timeItems = ref([])
const class_type = ref([])
const days = ref([])
const ages = ref([])

const fetchData = async () => {
  try {
    button_update.value = true
    data.value = []
    const response = await axios.get('clients-date/')
    loading.value = false
    data.value = response.data.clients
    class_type.value = response.data.class_type
    timeItems.value = response.data.time
    status.value = response.data.status_paid
    days.value = response.data.visit_day
    ages.value = response.data.ages
  } catch (error) {
  }
  button_update.value = false
}

fetchData()

const submit = async () => {
  try {
    button_submit.value = true
    await axios.post('clients-date/', {clients: data.value}, {headers: {'Content-Type': 'application/json;charset=utf-8'}})
    await fetchData()
  } catch (_) {

  }
  button_submit.value = false
}
</script>

<style scoped>
.v-card-base {
  margin-bottom: 25px;
  padding: 5px;
}

.table-naive {
  overflow: auto;
  white-space: pre;
}
</style>

