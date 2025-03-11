<template>
  <div class="translator-container">
    <h1 class="translator-title">机器翻译</h1>

    <div class="translation-container">
      <div class="translation-input">
        <label for="sourceLanguage">源语言：</label>
        <div class="input-container">
          <select v-model="sourceLanguage" id="sourceLanguage" class="styled-select">
            <option value="auto">自动选择</option>
            <option value="en">英语</option>
            <option value="cn">中文</option>
            <option value="fr">法语</option>
            <option value="ko">韩语</option>
            <option value="ru">俄语</option>
            <option value="es">西班牙语</option>
          </select>
        </div>
        <div class="input-container">
          <textarea v-model="sourceText" placeholder="请输入待翻译文本" class="styled-textarea"></textarea>
        </div>
      </div>

      <div class="translation-output">
        <label for="targetLanguage">目标语言：</label>
        <div class="input-container">
          <select v-model="targetLanguage" id="targetLanguage" class="styled-select">
            <option value="cn">中文</option>
            <option value="en">英语</option>
            <option value="fr">法语</option>
            <option value="ko">韩语</option>
            <option value="ru">俄语</option>
            <option value="es">西班牙语</option>
          </select>
        </div>
        <div class="input-container">
          <div class="translated-text">{{ translatedText }}</div>
        </div>
      </div>
    </div>

    <button @click="translateText" class="styled-button">翻译</button>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { trans } from '../api/user';

const sourceText = ref('');
const sourceLanguage = ref('auto');
const targetLanguage = ref('cn');
const translatedText = ref('');

const translateText = async () => {
  try {
    const response = await trans({
      businessargs: {
        from: sourceLanguage.value,
        to: targetLanguage.value,
      },
      text: sourceText.value,
    });

    translatedText.value = response.data.trans_result.dst;
    sourceLanguage.value = response.data.from;
    targetLanguage.value = response.data.to;
  } catch (error) {
    console.error('Error translating text:', error);
  }
};
</script>

<style scoped>
.translator-container {
  /* width: 50%; */
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  margin: 20px;
  background-color: #f5f5f5;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}



.translator-title {
  font-size: 32px;
  text-align: center;
  margin-bottom: 20px;
}


.translation-container {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

.translation-input,
.translation-output {
  flex: 1;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
}

.label {
  display: block;
  margin-bottom: 10px;
  font-weight: bold;
}

.input-container {
  width: 100%;
}

.styled-select,
.styled-textarea {
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  margin-bottom: 10px;
  font-size: 14px;
  outline: none;
}
  .styled-textarea {
  width: 98%;
  height: 120px;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  margin-bottom: 10px;
  font-size: 16px;
  font-family: 'Arial', sans-serif;
  outline: none; 
  resize: none; 
}


.translated-text {
  margin-top: 15px;
  font-weight: bold;
  font-size: 20px;
  font-family: 'Arial', sans-serif; 
}

.styled-button {
  width: 50%; /* Adjusted width */
  padding: 12px; /* Adjusted padding */
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.styled-button:hover {
  background-color: #45a049;
}

</style>
