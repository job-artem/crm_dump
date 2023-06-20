<template>
  <v-card class="base-container" outlined shaped style="max-width: 100%">
    <v-card-title>Таблица новых клиентов:
    </v-card-title>
    <v-card-text>
      <n-space justify="space-between">
        <v-btn :loading="loading" class="text-caption" variant="outlined" @click="fetchData">Обновить таблицу</v-btn>
        <v-btn :disabled="items.length === 0" :loading="submit" class="text-caption" variant="outlined"
               @click="submitForm">Сохранить данные
        </v-btn>
      </n-space>
    </v-card-text>
    <v-container v-if="items.length > 0" style="min-width: 90%">
      <v-data-table
        :headers="headers"
        :items="items"
        :loading="loading"
        :rows-per-page-items="[10, 20, 30]"
        class="elevation-1"
        height="100%"
        style="min-width: 100%; min-height: 100%;"
        width="100%"
      >
        <template v-slot:item.fullname="{ item }">
          <v-text-field
          v-model="item.props.title.fullname"
          style="min-width: 200px"
          variant="underlined"
          />
        </template>
        <template v-slot:item.status="{ item }">
          <n-select
            v-model:value="item.props.title.status"
            :options="status"
            style="width: 140px"
          />
        </template>
      </v-data-table>
    </v-container>
    <v-container v-else>
      <v-card>
        <v-alert
          text="Новые заявки отсутствуют!"
          type="info"
          variant="tonal"
        />
      </v-card>
    </v-container>
  </v-card>
</template>
<script setup>
import {computed, ref, watch} from 'vue';
import axios from 'axios';
import {VDataTable} from "vuetify/labs/components";
import {useDisplay} from "vuetify";

const status = ref([
  {'label': 'Записан', 'value': 'recorded'},
  {'label': 'Отказ', 'value': 'not_recorded'},
  {'label': 'Не проверен', 'value': 'not_checked'},
])
const items = ref([]);
const loading = ref(false);
const submit = ref(false);
const dialog = ref(false);
const selected_item = ref(null);
const new_item = ref({
  class_type: '',
  section: '',
  visit_time: '',
  visit_day: '',
  location: ''
})
const headers = [
  {title: 'Фамилия Имя', key: 'fullname'},
  {title: 'Номер телефона', key: 'phone_number'},
  {title: 'Статус клиента', key: 'status'},
];
const button_add = ref(true)
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
const new_client = async (value) => {
  if (!selected_item.details) {
    selected_item.details = []
  }
  value.details.push(new_item.value)
  new_item.value = {
    class_type: '',
    section: '',
    visit_time: '',
    visit_day: '',
    location: ''
  }
  dialog.value = false
}
watch(new_item, async () => {
  button_add.value = !(
    new_item.value.class_type.length > 0 &&
    new_item.value.section.length > 0 &&
    new_item.value.visit_time.length > 0 &&
    new_item.value.visit_day.length > 0
  )
}, {deep: true})
const fetchData = async () => {
  try {
    loading.value = true;
    const response = await axios.get('new-clients/');
    items.value = response.data.elements

  } catch (_) {
  } finally {
    loading.value = false;
  }
};


const submitForm = async () => {
  try {
    submit.value = true
    await axios.post("new-clients/", {data: items.value});
    await fetchData()
  } catch (_) {
  }
  submit.value = false
}
fetchData();
</script>
<style scoped>

</style>
