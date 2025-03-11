import { createRouter, createWebHistory } from 'vue-router';
import { getUser } from '../api/user'; // 替换为您的实际路径

const routes = [
  {
    path: '/', // 重定向
    redirect: (_) => {
      return { path: '/login' }; // 切换到哪一个路由地址
    },
  },
  {
    path: '/login/', // 路由地址
    name: 'login',
    component: () => import('../view/login.vue'),
  },
  {
    path: '/404',
    name: '404',
    component: () => import('../view/404.vue'),
  },
  {
    path: '/temp',
    name: 'temp',
    component: () => import('../view/temp.vue'),
  },
  {
    path: '/details',
    name: 'detail',
    component: () => import('../view/detail.vue'),
  },
  {
    path: '/trans',
    name: 'translate',
    component: ()=> import('../view/third.vue'),
  },
  {
    path: '/contacts',
    name: 'contacts',
    component:()=> import('../view/contacts.vue'),
    meta: { requiresAdmin: true } // 添加 meta 属性，标记需要管理员权限的路由
  },
  {
    path: '/admine',
    name: 'admine',
    component:()=> import('../view/admine.vue'),
    meta: { requiresAdmin: true } // 添加 meta 属性，标记需要管理员权限的路由
  },
  {
    path: '/:currentPath(.*)*', // 路由未匹配到，进入这个
    redirect: (_) => {
      return { path: '/404' };
    },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 添加全局导航守卫
router.beforeEach(async (to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAdmin)) {
    try {
      const response = await getUser();
      if (response.data.data.role) {
        // alert('是管理员');
        next(); // 允许访问
      } else {
        next('/temp'); // 重定向到主页或其他页面
      }
    } catch (error) {
      console.error('检查管理员状态时出错:', error);
      next('/404'); // 出错时也重定向到主页或其他页面
    }
  } else {
    next(); // 不需要管理员权限，允许访问
  }
});

export default router;
