// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import 'es6-promise/auto' // PhantomJS, the headless browser, requires it
import Vue from 'vue'
import App from '@/App'
import router from '@/router'
import store from '@/store'
// import config from '@/config.js'
// import Cookies from 'js-cookie'

Vue.config.productionTip = true

/* eslint-disable no-new */
new Vue({
  el: '#app',
  store,
  router,
  template: '<App/>',
  components: {
    App
  }
})
