import { createApp } from 'vue'
import ElementPlus from 'element-plus';
import App from './App.vue';
import 'element-plus/dist/index.css'; 
import router from "./components/router";
import api from '@/api.js';

const app = createApp(App)
app.use(router);//注意顺序
app.use(ElementPlus)
app.config.globalProperties.api=api
app.mount('#app')