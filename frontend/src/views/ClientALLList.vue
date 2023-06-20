<template>
  <v-card class="base-container" outlined shaped>
    <v-card-title v-if="height > 220">
      Таблица клиентов: {{ currentDate }}
    </v-card-title>
    <v-card-title v-if="height === 220">
      Таблица клиентов:
    </v-card-title>
    <v-card-title v-if="height === 220">
      {{ currentDate }}
    </v-card-title>
    <v-container v-if="showTable" style="min-width: 100%">
      <n-data-table
        :columns="createColumns()"
        :data="data"
        :loading="loading"
        :pagination="pagination"
        :row-key="rowKey"
        class="table-naive"
        size="small"
        @update:checked-row-keys="handleCheck"
      />
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
import axios from "axios";
import moment from "moment";

const showTable = ref(true)
const currentDate = ref(new Date().toLocaleDateString("ru-RU", {
  day: "numeric",
  month: "long",
  year: "numeric",
}))
const loading = ref(true)
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


const data = ref([])
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
    key: "class_type"
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
  },
  {
    title: "Тренер",
    key: "coach",
  },
  {
    title: "Дата добавления",
    key: "date_added",
    render(row, index) {
      return h(formatDate, {
        value: row.date_added,
        onUpdateValue(v) {
          data.value[index].date_added = v;
        }
      })
    },
  },
  {
    title: "Дата последнего обновления",
    key: "date_update",
    render(row, index) {
      return h(formatDate, {
        value: row.date_update,
        onUpdateValue(v) {
          data.value[index].date_update = v;
        }
      })
    },
  }
];
const rowKey = (row) => row.id
const pagination = ref({
  pageSize: 50
})
const checkedRowKeysRef = ref([]);
const handleCheck = (rowKeys) => {
  checkedRowKeysRef.value = rowKeys;
}
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

const fetchData = async () => {
  try {
    loading.value = true
    const response = await axios.get('client-all-list/')
    data.value = response.data.elements
    if (data.value.length === 0) {
      showTable.value = false
    }
    loading.value = false
  } catch (_) {
    showTable.value = false
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
