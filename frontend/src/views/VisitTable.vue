<script setup>

import {VDataTable} from "vuetify/labs/components";
import {computed, ref} from "vue";
import {useDisplay} from "vuetify";
import axios from "axios";

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


const date_choice = ref([
  "Сегодня",
  "Неделя",
  "3 месяца",
  "Полгода",
  "Год"
])
const choice_date = ref("Сегодня")
const items = ref([])
const header = ref([])
const loading = ref(false)
const getData = async () => {
  items.value = []
  header.value = []
  loading.value = true
  const response = await axios.post('visit/', {date: choice_date.value})
  items.value = response.data.attention
  header.value = response.data.header
  loading.value = false
}
</script>

<template>
  <v-responsive>
    <v-sheet :class="`ml-${height > 220 ? 5 : 0} mr-${height > 220 ? 5 : 0} mt-2 mb-5` " style="padding: 10px;">
      <v-card class="v-card-base" elevation="20">
        <v-card-title class="mb-5">
          Таблица посещений:
        </v-card-title>
        <v-card-text style="display: grid; place-items: center">
          <v-select
            v-model="choice_date"
            :items="date_choice"
            density="compact"
            label="Посещения за:"
            style="min-width: 200px"
            variant="underlined"
          />
        </v-card-text>
        <v-card-actions style="display: grid; place-items: center">
          <v-btn class="text-caption mb-1" variant="outlined" @click="getData">
            Сгенерировать таблицу посещений
          </v-btn>
        </v-card-actions>
        <v-card-text v-if="items.length > 0">
          <v-data-table
            :headers="header"
            :items="items"
          />
        </v-card-text>
        <v-card-text v-if="items.length === 0 && loading" style="display: grid; place-items: center">
          <v-progress-circular
            :size="50"
            color="primary"
            indeterminate
          />
        </v-card-text>

        <v-card-text style="display: grid; place-items: center">
          <n-space justify="space-between">
            <!--            <v-btn :disabled="data.length === 0" :loading="button_submit" append-icon="mdi-account-plus-outline"-->
            <!--                   class="text-caption mb-1"-->
            <!--                   variant="outlined" @click="submit">-->
            <!--              Сохранить и отправить-->
            <!--            </v-btn>-->
          </n-space>
        </v-card-text>

      </v-card>
    </v-sheet>
  </v-responsive>
</template>

<style scoped>

</style>
