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
import DefaultDash from '@/layouts/AppLayout.vue';
import None from '@/layouts/None.vue';

// Layouts as usable components
Vue.component('default-dash-layout', DefaultDash);
Vue.component('none-layout', None);

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');
