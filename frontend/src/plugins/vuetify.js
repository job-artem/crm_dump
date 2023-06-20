// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'material-design-icons-iconfont/dist/material-design-icons.css'
import '@fortawesome/fontawesome-free/css/all.css'
import 'vuetify/dist/vuetify.min.css'
import 'vuetify/styles'

// Composables
import {createVuetify} from 'vuetify'
import {mdi} from 'vuetify/iconsets/mdi-svg'
import {md} from 'vuetify/iconsets/md'
import {fa} from 'vuetify/iconsets/fa'

export default createVuetify({
  theme: {
    themes: {
      light: {
        colors: {
          primary: '#1867C0',
          secondary: '#5CBBF6',
        },
      },
    },
    icons: {
      defaultSet: mdi,
      sets: {
        mdi,
        md,
        fa
      },
    },
  },
})
