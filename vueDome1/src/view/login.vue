<template>
  <div class="main">
    <div :class="{ 'is-txl': aContainerClass }" class="container a-container" id="a-container">
      <div class="form" id="a-form">
        <h2 class="form_title title">登录网站</h2>
        <div style="height:50px;"></div>
        <input v-model="username" type="text" class="form__input" placeholder="账号">
        <input v-model="password" type="password" class="form__input" placeholder="密码">
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
        <div style="height:50px;"></div>
        <button class="form__button button switch-btn" @click="getButtons">登录</button>
      </div>
    </div>

    <div :class="{ 'is-txl': aContainerClass, 'is-z200': aContainerClass }" class="container b-container" id="b-container">
      <div class="form" id="b-form">
        <h2 class="form_title title">创建账号</h2>
        <div style="height:50px;"></div>
        <input v-model="new_account" type="text" class="form__input" placeholder="账号">
        <input v-model="new_name" type="text" class="form__input" placeholder="姓名">
        <input v-model="new_password" type="password" class="form__input" placeholder="密码">
        <input v-model="organization" type="text" class="form__input" placeholder="组织">
        <div v-if="registerMessage" class="error-message">{{ registerMessage }}</div>
        <div style="height:50px;"></div>
        <button class="form__button button" @click="rgetButtons">注册</button>
      </div>
    </div>
    <div class="switch" :class="{ 'is-txr': aContainerClass }" id="switch-cnt">
      <div :class="{ 'is-txr': aContainerClass }" class="switch__circle"></div>
      <div :class="{ 'is-txr': aContainerClass }" class="switch__circle switch__circle--t"></div>
      <div :class="{ 'is-hidden': aContainerClass }" class="switch__container" id="switch-c1">
        <h2 class="switch__title title">欢迎回来！</h2>
        <p class="switch__description description">
          与我们保持联系，请登录您的个人信息
        </p>
        <button class="switch__button button switch-btn" @click="changeForm">立即注册</button>
      </div>
      <div :class="{ 'is-hidden': !aContainerClass }" class="switch__container" id="switch-c2">
        <h2 class="switch__title title">你好朋友！</h2>
        <p class="switch__description description">
          输入您的个人信息，并开始与我们沟通
        </p>
        <button class="switch__button button switch-btn" @click="changeForm">立即登录</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { Login, Register } from '../api/user';
import { useRouter } from 'vue-router';
import { useTestStore } from '../store/user'

const router = useRouter();
const aContainerClass = ref(false);
const username = ref('');
const password = ref('');
const new_account = ref('');
const new_password = ref('');
const new_name = ref('');
const organization = ref('');
const errorMessage = ref('');
const loginMessage = ref('');
const registerMessage = ref('');
const testStore = useTestStore();


const getButtons = () => {
  if (username.value.trim() === '' || password.value.trim() === '') {
    errorMessage.value = '账号或密码不能为空';
    return;
  }

  Login({
    username: username.value,
    password: password.value,
  })
    .then(response => {
      if (response.data.code === 200) {
        loginMessage.value = response.message;
        alert('登录成功!!!');
        testStore.setTokens({
          user_id : response.data.data.user_id,
          access_token: response.data.data.access_token,
          refresh_token: response.data.data.refresh_token,
        });
        router.push({ path: '/temp' }); 
      } else {
        errorMessage.value = '用户名或密码错误!!!';
      }
    })
    .catch(error => {
      console.error('Login failed', error);
    });

  errorMessage.value = '';
};

const rgetButtons = () => {
  if (new_account.value.trim() === '' || new_name.value.trim() === '' || new_password.value.trim() === '') {
    registerMessage.value = '账号密码或姓名不能为空';
    return;
  }
  Register({
    name: new_name.value.trim(),
    password: new_password.value.trim(),
    username: new_account.value.trim(),
    organization: organization.value.trim(),
  })
    .then(response => {
      if (response.data.code === 200) {
        loginMessage.value = '注册成功';
        alert("注册成功")
      } else if (response.data.code === 234) {
        loginMessage.value = '用户已经存在';
        alert('用户已经存在');
      } else {
        errorMessage.value = response.data.message;
      }
    })
    .catch(error => {
      console.error('Registration failed', error);
    });

  registerMessage.value = '';
};

const changeForm = () => {
  aContainerClass.value = !aContainerClass.value;
  username.value = '';
  password.value = '';
  new_account.value = '';
  new_password.value = '';
  new_name.value = '';
  organization.value = '';
  errorMessage.value = '';
  loginMessage.value = '';
  registerMessage.value = '';
};
</script>


<style scoped>
*,*::after,*::before {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    user-select: none
}

body {
    width: 100%;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    font-family: 'Montserrat',sans-serif;
    font-size: 12px;
    background-color: #ecf0f3;
    color: #a0a5a8
}

.main {
    position: relative;
    width: 1000px;
    min-width: 1000px;
    min-height: 600px;
    height: 600px;
    padding: 25px;
    background-color: #ecf0f3;
    box-shadow: 10px 10px 10px #d1d9e6,-10px -10px 10px #f9f9f9;
    border-radius: 12px;
    overflow: hidden
}

.error-message {
    color: red;
    font-size: 14px;
    margin-top: 5px; /* 适当的上边距，使其与输入框有一些间距 */
  }
  

.container {
    display: flex;
    justify-content: center;
    align-items: center;
    position: absolute;
    top: 0;
    width: 600px;
    height: 100%;
    padding: 25px;
    background-color: #ecf0f3;
    transition: 1.25s
}

.form {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    width: 100%;
    height: 100%
}

.form__icon {
    object-fit: contain;
    width: 30px;
    margin: 0 5px;
    opacity: .5;
    transition: .15s
}

.form__icon:hover {
    opacity: 1;
    transition: .15s;
    cursor: pointer
}

.form__input {
    width: 350px;
    height: 40px;
    margin: 4px 0;
    padding-left: 25px;
    font-size: 13px;
    letter-spacing: .15px;
    border: 0;
    outline: 0;
    font-family: 'Montserrat',sans-serif;
    background-color: #ecf0f3;
    transition: .25s ease;
    border-radius: 8px;
    box-shadow: inset 2px 2px 4px #d1d9e6,inset -2px -2px 4px #f9f9f9
}

.form__input:focus {
    box-shadow: inset 4px 4px 4px #d1d9e6,inset -4px -4px 4px #f9f9f9
}

.form__span {
    margin-top: 30px;
    margin-bottom: 12px
}

.form__link {
    color: #181818;
    font-size: 15px;
    margin-top: 25px;
    border-bottom: 1px solid #a0a5a8;
    line-height: 2
}

.title {
    font-size: 34px;
    font-weight: 700;
    line-height: 3;
    color: #181818
}

.description {
    font-size: 14px;
    letter-spacing: .25px;
    text-align: center;
    line-height: 1.6
}

.button {
    width: 180px;
    height: 50px;
    border-radius: 25px;
    margin-top: 50px;
    font-weight: 700;
    font-size: 14px;
    letter-spacing: 1.15px;
    background-color: #4B70E2;
    color: #f9f9f9;
    box-shadow: 8px 8px 16px #d1d9e6,-8px -8px 16px #f9f9f9;
    border: 0;
    outline: 0
}

.a-container {
    z-index: 100;
    left: calc(100% - 600px)
}

.b-container {
    left: calc(100% - 600px);
    z-index: 0
}

.switch {
    display: flex;
    justify-content: center;
    align-items: center;
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    width: 400px;
    padding: 50px;
    z-index: 200;
    transition: 1.25s;
    background-color: #ecf0f3;
    overflow: hidden;
    box-shadow: 4px 4px 10px #d1d9e6,-4px -4px 10px #f9f9f9
}

.switch__circle {
    position: absolute;
    width: 500px;
    height: 500px;
    border-radius: 50%;
    background-color: #ecf0f3;
    box-shadow: inset 8px 8px 12px #d1d9e6,inset -8px -8px 12px #f9f9f9;
    bottom: -60%;
    left: -60%;
    transition: 1.25s
}

.switch__circle--t {
    top: -30%;
    left: 60%;
    width: 300px;
    height: 300px
}

.switch__container {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    position: absolute;
    width: 400px;
    padding: 50px 55px;
    transition: 1.25s
}

.switch__button {
    cursor: pointer
}

.switch__button:hover {
    box-shadow: 6px 6px 10px #d1d9e6,-6px -6px 10px #f9f9f9;
    transform: scale(0.985);
    transition: .25s
}

.switch__button:active,.switch__button:focus {
    box-shadow: 2px 2px 6px #d1d9e6,-2px -2px 6px #f9f9f9;
    transform: scale(0.97);
    transition: .25s
}

.is-txr {
    left: calc(100% - 400px);
    transition: 1.25s;
    transform-origin: left
}

.is-txl {
    left: 0;
    transition: 1.25s;
    transform-origin: right
}

.is-z200 {
    z-index: 200;
    transition: 1.25s
}

.is-hidden {
    visibility: hidden;
    opacity: 0;
    position: absolute;
    transition: 1.25s
}

.is-gx {
    animation: is-gx 1.25s
}

@keyframes is-gx {
    0%,10%,100% {
        width: 400px
    }

    30%,50% {
        width: 500px
    }
}

</style>



