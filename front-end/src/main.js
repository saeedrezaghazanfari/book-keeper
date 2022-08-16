import { createApp } from 'vue'
import App from './App.vue'
import Vue3PersianDatetimePicker from 'vue3-persian-datetime-picker'
import './assets/css/configure.css'
import './assets/css/custom.css'
import './assets/font/themify-icons.css'
import router from './router'
import store from './store'
import { i18n } from 'vue-lang-router'


createApp(App)
    .use(i18n)
    .use(store)
    .use(router)
    .use(Vue3PersianDatetimePicker, {
        name: 'CustomDatePicker',
        props: {
            editable: false,
            inputClass: 'form-control my-custom-class-name',
            placeholder: 'Please select a date',
            color: '#00acc1',
            autoSubmit: false,
        }
    })
    .mount('#app');