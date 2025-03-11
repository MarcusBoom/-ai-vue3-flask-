<template>
  <div id="chat-app">
    <div class="navbar">
      <div class="logo">
        <h1>Chat App</h1>
      </div>
      <ul class="nav-links">
        <li @click="goToInfo">My Information</li>
        <li @click="goToAbout">Machine Translation</li>
        <li @click="goToCont" v-if="isAdmin">contacts</li>
      </ul>
    </div>

    <div class="content-container">
      <div class="sidebar">
        <ul class="nav">
            <li v-for="chatBox in chatBoxes" :key="chatBox.id">
            <div @click="changeChatBox(chatBox.id)">
              {{ chatBox.name }}
              <button @click="editChatBoxName(chatBox.id)">Edit Name</button>
              <button @click="confirmDeleteChatBox(chatBox.id)">Delete</button>
            </div>
            </li>
            <li @click="createNewChatBox">New Chat Box</li>         
        </ul>
      </div>

      <div class="main-content">
        <div class="header">
          <el-select v-model="selectedModel" placeholder="Select Model" class="model-select">
            <el-option v-for="model in models" :key="model" :label="model" :value="model"></el-option>
          </el-select>
          <el-select v-model="selectedRole" placeholder="Select Role" class="role-select">
            <el-option v-for="role in roles" :key="role" :label="role" :value="role"></el-option>
          </el-select>
          <h2>Chat Application</h2>
        </div>

        <div v-for="chatBox in chatBoxes" :key="chatBox.id" class="chat-box" v-show="selectedChatBoxId === chatBox.id">
          <div class="message-history">
            <div v-for="(item, index) in chatBox.messageHistory" :key="index" class="message" :class="{ user: item.type === 'user', chatAnswer: item.type === 'chatAnswer' }">
              {{ item.content }}
            </div>
          </div>
          <div class="input-box">
            <textarea v-model="chatBox.userInput" placeholder="Type your question..."></textarea>
            <button class="ask_btn" @click="askQuestion(chatBox)">Ask</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { getUser, askToModel, loadBox, addBox, editBoxName, sendChatMessage, getChatHistory, deleteChatBoxRecord, loadmodels, loadroles } from '../api/user';

const router = useRouter();

const roles = ref([]);
const selectedRole = ref(null);

const models = ref([]);
const selectedModel = ref(null); // 默认选择第一个模型
const chatBoxes = ref([]);
const selectedChatBoxId = ref(null);
const isAdmin = ref(false); // 默认值为 false

// 在 onMounted 钩子中设置默认选项
onMounted(async () => {
  try {
    // 示例：使用 API 调用或其他逻辑检查管理员状态
    const Admine = await getUser();
    isAdmin.value = Admine.data.data.role; // 根据您的实际响应结构进行调整

    // 加载聊天框数据
    const response = await loadBox();
    chatBoxes.value = response.data.chatBoxes;

    // 加载模型和角色数据
    const response1 = await loadmodels();
    models.value = response1.data.model_name;
    roles.value = response1.data.role_name;

    // 设置默认选项
    selectedModel.value = models.value.length > 0 ? models.value[0] : null;
    selectedRole.value = roles.value.length > 0 ? roles.value[0] : null;

    selectedChatBoxId.value = chatBoxes.value.length > 0 ? chatBoxes.value[0]?.id : null;

    // 初始化加载第一个聊天框
    await changeChatBox(selectedChatBoxId.value);
  } catch (error) {
    console.error('Error while initializing chat application:', error);
  }
});



// 创建新的聊天框
const createNewChatBox = async () => {
  try {
    const newBoxId = String.fromCharCode('A'.charCodeAt(0) + chatBoxes.value.length);
    const newBoxName = 'Chat Box ' + newBoxId;
    const response = await addBox({ name: newBoxName });

    // 刷新聊天框列表
    await refreshChatBoxes();
  } catch (error) {
    console.error('Error while creating new chat box:', error);
  }
};

// 删除聊天框
const deleteChatBox = async (boxId) => {
  const index = chatBoxes.value.findIndex((box) => box.id === boxId);
  if (index !== -1) {
    try {
      await deleteChatBoxRecord(boxId);
      chatBoxes.value.splice(index, 1);
      selectedChatBoxId.value = chatBoxes.value[Math.max(index - 1, 0)]?.id || null;
    } catch (error) {
      console.error('Error while deleting chat box:', error);
    }
  }
};

// 确认删除聊天框
const confirmDeleteChatBox = (boxId) => {
  if (confirm('确定删除该聊天吗？')) {
    deleteChatBox(boxId);
  }
};

// 编辑聊天框名称
const editChatBoxName = async (boxId) => {
  const newName = prompt('Enter the new name for the Chat Box:', chatBoxes.value.find(box => box.id === boxId)?.name);
  if (newName !== null) {
    const index = chatBoxes.value.findIndex((box) => box.id === boxId);
    if (index !== -1) {
      try {
        await editBoxName({ boxId, newName });
        chatBoxes.value[index].name = newName;
      } catch (error) {
        console.error('Error while updating chat box name:', error);
      }
    }
  }
};

// 发送问题到模型
const askQuestion = async (chatBox) => {
  try {
    if (!chatBox.messageHistory) {
      chatBox.messageHistory = [];
    }
    if (chatBox.userInput !== '') {
      chatBox.messageHistory.push({ type: 'user', content: chatBox.userInput });
      const input = chatBox.userInput;
      chatBox.userInput = '';
      const response = await askToModel({ userInput: input, model: selectedModel.value || 'glm-4',role: selectedRole.value || 'User'});
      chatBox.chatAnswer = response.data.answer;
      await sendChatMessage({ type: 'user', content: input }, chatBox.id);
      chatBox.messageHistory.push({ type: 'chatAnswer', content: chatBox.chatAnswer });
      await sendChatMessage({ type: 'chatAnswer', content: chatBox.chatAnswer }, chatBox.id);
    }
  } catch (error) {
    console.error('Error while asking question:', error);
  }
};

// 获取聊天历史记录
const changeChatBox = async (boxId) => {
  selectedChatBoxId.value = boxId || chatBoxes.value[0]?.id;
  const selectedChatBox = chatBoxes.value.find(box => box.id === selectedChatBoxId.value);
  if (selectedChatBox) {
    try {
      const response = await getChatHistory(selectedChatBox.id);
      selectedChatBox.messageHistory = response.data.chatHistory;
    } catch (error) {
      console.error('Error while getting chat history:', error);
    }
  }
};

// 跳转个人信息页面
const goToInfo = () => {
  router.push('/details');
};

// 跳转机器翻译页面
const goToAbout = () => {
  router.push('/trans');
};

//跳转通讯录页面
const goToCont = () => {
  router.push('/contacts');
};

// 刷新聊天框列表
const refreshChatBoxes = async () => {
  try {
    const response = await loadBox();
    chatBoxes.value = response.data.chatBoxes;
    selectedChatBoxId.value = chatBoxes.value[0]?.id;
  } catch (error) {
    console.error('Error while refreshing chat boxes:', error);
  }
};
</script>

<style scoped>
#chat-app {
  background-color: #f5f8fa;
  display: flex;
  height: 95vh;
  flex-direction: column;
}

.content-container {
  background-color: #e0f7fa;
  display: flex;
  flex: 1;
}

.logo {
  margin-left: 20px;
}

.sidebar {
  overflow-y: auto;
  background-color: #009688;
  color: #ffffff;
  width: 270px;
  height: 80vh;
  padding: 20px;
  flex: 0 0 auto;
  border-top-left-radius: 10px;
  border-bottom-left-radius: 10px;
  box-shadow: 2px 0px 5px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
  display: flex; /* 使用 Flex 布局 */
  flex-direction: column; /* 垂直排列子元素 */
}

.nav {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex; /* 使用 Flex 布局 */
  flex-direction: column; /* 垂直排列列表项 */
  flex-grow: 1; /* 填充整个可用空间 */
}

.nav li {
  padding: 10px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  display: flex; /* 使用 Flex 布局 */
  align-items: center; /* 垂直居中 */
}

.nav li:hover {
  background-color: #45a049;
}

.nav li button:nth-child(1) {
  border-top-left-radius: 10px;
  border-bottom-left-radius: 10px;
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
  background-color: #007bff;
  color: #ffffff;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.nav li button:nth-child(1):hover {
  background-color: #0056b3;
}

.nav li button:nth-child(2) {
  border-top-right-radius: 10px;
  border-bottom-right-radius: 10px;
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
  background-color: #dc3545;
  color: #ffffff;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.nav li button:nth-child(2):hover {
  background-color: #c82333;
}

.main-content {
  flex: 1;
  padding: 10px;
  display: flex;
  max-height: 100%;
  flex-direction: column;
}

.header {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #00796b;
  color: #ffffff;
  padding: 10px;
  border-top-right-radius: 10px;
  border-top-left-radius: 10px;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
}

.chat-box {
  flex:1;
  display: flex;
  flex-direction: column;
  max-height: 60vh;
  padding: 16px;
  border: 1px solid #26a69a;
  border-radius: 8px;
  position: relative;
  background-color: #e0f7fa; 
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
}

.message-history {
  flex:1;
  max-height: 100%;
  overflow-y: auto;
  padding-right: 10px;
}

.message {
  margin-bottom: 8px;
  padding: 8px;
  border-radius: 4px;
}

.user {
  background-color: #e6f7ff; /* 用户消息背景颜色 */
}

.chatAnswer {
  background-color: #f0f0f0; /* 机器翻译回复消息背景颜色 */
}

.input-box {
  margin-top: auto;
  padding: 10px;
  background-color: #80cbc4;
  display: flex;
  align-items: center;
  justify-content: space-around;
  border-bottom-left-radius: 10px;
  border-bottom-right-radius: 10px;
  box-shadow: 0px -2px 5px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
}

textarea {
  width: 80%;
  height: 40px;
}

button {
  cursor: pointer;
}

.ask_btn {
  margin-left: 10px;
  width: 15%;
  border: none;
  padding: 8px 16px;
  border-radius: 20px; /* 圆角按钮 */
  background-color: #4caf50; /* 按钮背景色 */
  color: #ffffff;
  cursor: pointer;
  transition: background-color 0.3s ease; /* 添加背景颜色过渡效果 */
}

.navbar {
  background-color: #00796b;
  color: #ffffff;
  padding: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60px;
  z-index: 1000;
  top: 0;
  overflow: hidden;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
}

.nav-links {
  list-style: none;
  display: flex;
  margin: 0;
  padding: 0;
  white-space: nowrap;
}

.nav-links li {
  margin-right: 20px;
  cursor: pointer;
}

.nav-links li:hover {
  text-decoration: underline;
  color: #ffcc00;
}

.sidebar:hover, .header:hover, .chat-box:hover, .input-box:hover, .navbar:hover {
  box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.2);
}

.select-container{
  position: absolute;
  left: 10px;
  display: flex;
  align-items: center;
}

.model-select,
.role-select {
  flex: 1; /* 平均分配空间 */
  margin: 0 10px;
  max-width: 10%;
}

</style>
