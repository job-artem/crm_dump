import {loadFonts} from './webfontloader'
import vuetify from './vuetify'
import store from '../store'
import router from '../router'
import GoogleSignInPlugin from "vue3-google-signin"
import axios from "axios";
import VueAxios from "vue-axios";
import {library} from "@fortawesome/fontawesome-svg-core";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import {fas} from "@fortawesome/free-solid-svg-icons";
import components from "@/components";
import components_ui from "@/components/UI"
import moment from "moment/dist/moment"
import naive from 'naive-ui'
import ru from "moment/dist/locale/ru"

moment.locale("ru", ru)

const gauthOption = {
  clientId: import.meta.env.VITE_GOOGLE_KEY
}
axios.defaults.baseURL = 'http://localhost:8000/backend/api/'
// axios.defaults.baseURL = 'http://185.233.119.142:8080/api/'
// axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*';
// axios.defaults.headers.common['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept';


export function registerPlugins(app) {
  loadFonts()
  components.forEach(component => {
    app.component(component.name, component)
  })
  components_ui.forEach(component => {
    app.component(component.name, component)
  })
  app.component('font-awesome-icon', FontAwesomeIcon) // Register component globally
  library.add(fas)
  app
    .use(VueAxios, axios)
    .use(store)
    .use(vuetify, {
      iconfont: 'mdi'
    })
    .use(router)
    .use(naive)
    .use(GoogleSignInPlugin, gauthOption)
}
