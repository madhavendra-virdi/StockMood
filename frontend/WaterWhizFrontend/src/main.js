// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import directives from './directives'
import filters from './filters'
import ElementUI from 'element-ui'
import './assets/style/theme.scss'
import store from './store'
import { mapState, mapMutations } from 'vuex'
import iView from 'iview'
import axios from 'axios'
import qs from 'qs'
import * as echarts from 'echarts'
import 'iview/dist/styles/iview.css'




// axios.defaults.baseURL = 'http://38.181.47.50:8080'
axios.defaults.baseURL = 'https://thestockmood.com';



Vue.config.productionTip = false
Vue.prototype.axios = axios
Vue.prototype.qs = qs
Vue.prototype.echarts = echarts


Vue.use(directives)
Vue.use(filters)
Vue.use(iView)

Vue.use(ElementUI, {
  size: 'small'
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  data: {
    loading: false
  },
  router,
  store,
  components: { App },
  template: '<App/>',
  computed: {
    ...mapState(['userInfo','stock'])
  },
  methods: {
    ...mapMutations(['switchCollapseMenu']),
    // Initialising the local configuration
    initLocalConfig() {
      const menuStatus = window.localStorage.getItem('MENU_STATUS')
      if (menuStatus != null) {
        this.switchCollapseMenu(menuStatus === 'true')
      }
    }
  },
  mounted() {
    this.initLocalConfig();
    this.$store.dispatch('loadStockFromLocalStorage');  // Load stock data from Vuex action

  }
})
