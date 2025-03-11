import { defineStore } from 'pinia';
import {refreshByToken} from '../api/user.js'
export const useTestStore = defineStore('user', {
    //若仅配置true，则全部存储
    persist: true,
    state: () => {return {
      user_id: '',
      access_token: '',
      refresh_token: '',
      // chat_id: ''
  }},
  actions: {
    setTokens({ user_id, access_token, refresh_token }) {
      this.user_id = user_id;
      this.access_token = access_token;
      this.refresh_token = refresh_token;
      // console.log("保存",this.user_id)
    },
    getUserId() {
      return this.user_id;
    },
    getAccessToken() {
      return this.access_token;
    },
    getRefreshToken() {
      return this.refresh_token;
    },
    async refreshToken() {
      try {
        // 调用后端接口刷新令牌
        const response = await refreshByToken({
          refresh_token: this.refresh_token,
        });

        // 更新 store 中的令牌信息
        this.setTokens({
          user_id: response.data.user_id,
          access_token: response.data.access_token,
          refresh_token: response.data.refresh_token,
        });

        // 返回新的访问令牌
        return response.data.access_token;
      }catch (error) {
        console.error('Error refreshing token:', error);
        throw error; // 可以根据需要处理刷新令牌失败的情况
      }
    }
  
  }
  })
  
