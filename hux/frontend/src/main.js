import Vue from 'vue';

import App from '@/App';
import router from './router';
import store from './store';

// NG Progress
import '../node_modules/ngprogress/ngProgress.css';

// // Enabling Multi-lingual
// import VueI18n from 'vue-i18n';
// Vue.use(VueI18n);

// Layouts
import AppLayout from '@/layouts/AppLayout';
import DefaultLayout from '@/layouts/None';

// Layouts as usable components
Vue.component('AppLayout', AppLayout);
Vue.component('DefaultLayout', DefaultLayout);

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');
