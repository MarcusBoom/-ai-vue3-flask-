import { createApp } from 'vue'
import App from './App.vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import router from './router'
import { useTestStore } from './store/user';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import 'element-plus/theme-chalk/index.css';
import * as ElementPlusIconsVue from '@element-plus/icons-vue';


const app = createApp(App)
const pinia = createPinia()


pinia.use(piniaPluginPersistedstate)

app.use(router).use(pinia).use(ElementPlus).mount('#app')

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component);
}

const testStore = useTestStore();
const refreshTokenInterval = setInterval(async () => {
    try {
      await testStore.refreshToken();
      console.log('Token refreshed successfully');
    } catch (error) {
      console.error('Error refreshing token:', error);
    }
  }, 30 * 60 * 1000);
app.config.globalProperties.$refreshTokenInterval = refreshTokenInterval

// 导航守卫
// router.beforeEach((to, from, next) => {
//   if (to.meta.requiresAdmin) {
//     // 假设有一个函数 isAdmin() 检查当前用户是否是管理员
//     const isAdmin = () => true; // 这里需要替换为实际的管理员判断逻辑
//     if (isAdmin()) {
//       next();
//     } else {
//       next('/temp');
//     }
//   } else {
//     next();
//   }
// });
