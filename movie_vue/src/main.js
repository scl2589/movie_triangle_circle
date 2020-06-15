import Vue from 'vue'
import App from './App.vue'
import router from './router'
import VueCookies from 'vue-cookies'

import { library } from '@fortawesome/fontawesome-svg-core'
import { faUserSecret } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { BootstrapVue} from 'bootstrap-vue'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(VueCookies)
Vue.use(BootstrapVue)
Vue.config.productionTip = false

library.add(faUserSecret)

Vue.component('font-awesome-icon', FontAwesomeIcon)


new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
