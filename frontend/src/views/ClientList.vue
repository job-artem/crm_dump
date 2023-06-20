<template>
  <v-card outlined shaped style="max-width: 100%">
    <v-card-title v-if="height > 220">
      Таблица новых клиентов: {{ currentDate }}
    </v-card-title>
    <v-card-title v-if="height === 220">
      Таблица новых клиентов:
    </v-card-title>
    <v-card-title v-if="height === 220">
      {{ currentDate }}
    </v-card-title>
    <v-card-text>
      <n-space justify="space-between">
        <v-btn :loading="button_update" class="text-caption mb-1" variant="outlined" @click="fetchData">
          Обновить таблицу
        </v-btn>
        <v-btn :loading="button_send" :disabled="data.length === 0" class="text-caption mb-1" variant="outlined" @click="submitForm">
          Сохранить изменения
        </v-btn>
      </n-space>
    </v-card-text>
    <v-container v-if="showTable" style="overflow: auto; white-space: pre;">
      <v-form @submit.prevent="submitForm">
        <n-data-table
          :columns="createColumns()"
          :data="data"
          :pagination="pagination"
          :row-key="rowKey"
          :loading="loading"
          class="table-naive"
          size="small"
          @update:checked-row-keys="handleCheck"
        />
      </v-form>
    </v-container>
    <v-container v-else class="text-center" style="min-width: 100%">
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
import {computed, defineComponent, h, ref} from "vue";
import {useDisplay} from "vuetify";
import moment from "moment";
import axios from "axios";
import {NSelect} from "naive-ui";

const currentDate = ref(new Date().toLocaleDateString("ru-RU", {
  day: "numeric",
  month: "long",
  year: "numeric",
}))
const loading = ref(true)
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
const showTable = ref(true)
const data = ref([])
const group_type = ref([])
const crm_status = ref([])
const coach_list = ref([])
const rowKey = (row) => row.id
const pagination = ref({
  pageSize: 50
})
const checkedRowKeysRef = ref([]);
const handleCheck = (rowKeys) => {
  checkedRowKeysRef.value = rowKeys;
}
const formatDate = defineComponent({
  props: {
    value: [String]
  },
  setup(props) {
    return () =>
      h(
        'span',
        moment(props.value).locale('ru').format('DD MMMM YYYY р. HH:mm')
      )
  }
})
const button_update = ref(false)
const button_send = ref(false)
const createColumns = () => [
  {
    title: "Фамилия Имя",
    key: "fullname",
    width: 150,
  },
  {
    title: "Номер телефона",
    key: "phone_number",
  },
  {
    title: "Секция",
    key: "section",
    width: 150,
  },
  {
    title: "Возрастная категория",
    key: "age",
    width: 170,
  },
  {
    title: "Тип занятий",
    key: "class_type",
    width: 160,
    render(row, index) {
      return h(NSelect, {
        value: row.class_type,
        options: group_type.value,
        onUpdateValue(v) {
          data.value[index].class_type = v;
        }
      });
    },
  },
  {
    title: "Дни посещения",
    key: "visit_day",
  },
  {
    title: "Время посещения",
    key: "visit_time",
  },
  {
    title: "Статус клиента",
    key: "crm_status",
    width: 180,
    render(row, index) {
      return h(NSelect, {
        value: row.crm_status,
        options: crm_status.value,
        onUpdateValue(v) {
          data.value[index].crm_status = v;
        }
      });
    },
  },
  {
    title: "Тренер",
    key: "coach",
    width: 200,
    render(row, index) {
      return h(NSelect, {
        value: row.coach,
        options: coach_list.value,
        onUpdateValue(v) {
          data.value[index].coach = v;
        }
      });
    },
  },
  {
    title: "Дата добавления",
    key: "data",
    render(row, index) {
      return h(formatDate, {
        value: row.data,
        onUpdateValue(v) {
          data.value[index].data = v;
        }
      })
    },
  },
];

const submitForm = async () => {
  button_send.value = true
  try {
    await axios.post('client-list/', {clients: data.value})
    await fetchData()
  } catch (error) {

  }
  button_send.value = false
}

const fetchData = async () => {
  try {
    data.value = []
    button_update.value = true
    loading.value = true
    const response = await axios.get('client-list/')
    data.value = response.data.elements
    showTable.value = data.value.length > 0
    loading.value = false
    group_type.value = response.data.group_type
    crm_status.value = response.data.crm_status
    coach_list.value = response.data.coach
    button_update.value = false
  } catch (error) {
    showTable.value = false
    button_update.value = false
  }
}

fetchData()
</script>

<style scoped>
.table-naive {
  overflow: auto;
  white-space: pre;
}
</style>
