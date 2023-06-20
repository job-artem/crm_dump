<template>
  <v-responsive>
    <n-message-provider>
      <n-dialog-provider>
        <v-app>
          <div>
            <div v-if="loading" class="loader-container">
              <div class="loader-inner">
                <v-progress-circular :size="64" :width="7" color="primary" indeterminate></v-progress-circular>
              </div>
            </div>

            <div v-else>
              <v-app-bar app>
                <v-app-bar-nav-icon v-if="height === 220" :icon="drawer ? 'mdi-menu' : 'mdi-menu-open'"
                                    @click="drawer = !drawer"/>
                <tab-auth v-if="store.state.user && height > 220"/>
                <tab-base v-if="!store.state.user && height > 220"/>
              </v-app-bar>
              <v-navigation-drawer
                v-model="drawer"
                app
                temporary
              >
                <left-menu-auth v-if="store.state.user"/>
                <left-menu-base v-else/>

                <div class="pa-2">
                  <v-btn v-if="store.state.user" block @click="logout">
                    Выход
                  </v-btn>
                </div>
              </v-navigation-drawer>
              <v-main>
                <v-responsive>
                  <v-container class="v-container" fluid>
                    <router-view/>
                  </v-container>
                </v-responsive>
              </v-main>
            </div>
          </div>
        </v-app>
      </n-dialog-provider>
    </n-message-provider>
  </v-responsive>
</template>

<script>

import {computed, ref, watchEffect} from "vue";
import axios from "axios";
import {useStore} from "vuex";
import {useRouter} from "vue-router";
import {useDisplay} from 'vuetify'
import LeftMenuBase from "@/components/navigation/LeftMenuBase.vue";
import LeftMenuAuth from "@/components/navigation/LeftMenuAuth.vue";
import TabAuth from "@/components/navigation/TabAuth.vue";
import TabBase from "@/components/navigation/TabBase.vue";

export default {
  name: 'App',
  components: {TabBase, TabAuth, LeftMenuBase, LeftMenuAuth},
  setup() {
    const store = useStore();
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
    store.dispatch('initializeStore');
    const router = useRouter();

    if (window.location.pathname.includes('/confirm_email/') && !store.state.user) {
    } else {
      if (window.location.pathname.includes('/confirm_email/') && store.state.user) {
        router.push({name: 'profile'});
      } else {
        if (!['auth/', 'form/'].includes(router.currentRoute.value.fullPath && !store.state.user)) {
          router.push({name: 'auth'});
        }
      }
    }
    watchEffect(() => {
      axios.defaults.headers['Authorization'] = store.state.access.length ? `Bearer ${store.state.access}` : ''
    });
    const getUserProfile = async () => {
      axios.defaults.headers['Authorization'] = `Bearer ${store.state.access}`
      try {
        const response = await axios.get('/user/profile/')
        const user = response.data

        let image = user.image
        if (image) {
          try {
            const responseImage = await axios.get('user/image/', {responseType: 'blob'})
            response.data.image = URL.createObjectURL(new Blob([responseImage.data], {type: 'text/plain;charset=utf-8'}))
          } catch (error) {
          }
        }
        store.commit('setLogout', true);
        store.commit('setUser', response.data)
      } catch (error) {
      }
    }
    setInterval(() => {
      if (!store.state.logout && !['/auth', '/form', '/confirm_email'].includes(router.currentRoute.value.fullPath)) {
        router.push({name: 'auth'});
      }
    })

    setInterval(() => {
      if (store.state.access && !store.state.user) {
        getUserProfile()
      }
    }, 1_000)

    const restoreAccess = async () => {
      delete axios.defaults.headers['Authorization']
      try {
        const response = await axios.post('refresh_token/', {refresh: store.state.refresh})
        store.commit('setAccess', response.data.access)
        await getUserProfile()
      } catch (error) {

      }
    }


    if (!store.state.access && localStorage.getItem('refresh')) {
      restoreAccess()
    }


    setInterval(() => {
      if (store.state.access && store.state.user) {
        restoreAccess()
        getUserProfile()
      }
    }, 59_000)

    const logout = async () => {
      localStorage.clear();
      store.commit('clearState')
      await router.push({name: 'auth'});
    }
    const loading = ref(true) // set the loading initially to true

    const initLoadingTimeout = () => {
      setTimeout(() => {
        loading.value = false
      }, 2000)
    }

    initLoadingTimeout()
    return {
      loading,
      height,
      logout,
      store,
      router
    }
  },
  data() {
    return {
      drawer: false,
      group: null,
      activeTab: null
    }
  },
}

</script>

<style>
.v-container {
  display: grid;
  place-items: center;
}


.loader-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.loader-inner {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}
</style>




