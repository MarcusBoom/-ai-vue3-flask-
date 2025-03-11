<template>
  <div class="profile-container">
    <div class="profile-content">
      <h1>User Profile</h1>

      <div v-if="user" class="profile-content">
        <div v-if="!isEditing" class="info-section">
          <p><strong>Username:</strong> {{ user.username }}</p>
          <p><strong>Name:</strong> {{ user.name }}</p>
          <p><strong>Age:</strong> {{ user.age }}</p>
        </div>

        <div v-if="!isEditing" class="buttons">
          <button @click="toggleEdit">Edit</button>
          <button @click="openChangePasswordDialog">Modify Password</button>
        </div>

        <div v-else>
          <label for="username">Username:</label>
          <input v-model="editedUser.username" id="username" />

          <label for="name">Name:</label>
          <input v-model="editedUser.name" id="name" />

          <label for="age">Age:</label>
          <input v-model="editedUser.age" id="age" />

          <div class="buttons">
            <button @click="saveChanges">Save Changes</button>
            <button @click="toggleEdit">Cancel</button>
          </div>
        </div>
      </div>

      <div v-else>
        <p>Loading user profile...</p>
      </div>
    </div>

    <div v-if="isChangePasswordDialogOpen" class="change-password-dialog">
      <div class="dialog-content">
        <label for="currentPassword">Current password：</label>
        <input v-model="currentPassword" type="password" id="currentPassword" />

        <label for="newPassword">New password：</label>
        <input v-model="newPassword" type="password" id="newPassword" />

        <label for="confirmPassword">Confirm password：</label>
        <input v-model="confirmPassword" type="password" id="confirmPassword" />

        <div class="buttons">
          <button @click="changePassword">Confirm Modification</button>
          <button @click="closeChangePasswordDialog">cancel</button>
        </div>

        <p v-if="passwordChangeError" class="error-message">{{ passwordChangeError }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getUser, editUser, modifyPassword } from '../api/user';

const user = ref(null);
const editedUser = ref({
  username: '',
  name: '',
  age: 0,
});

const isEditing = ref(false);
const isChangePasswordDialogOpen = ref(false);

const currentPassword = ref('');
const newPassword = ref('');
const confirmPassword = ref('');
const passwordChangeError = ref('');

onMounted(async () => {
  try {
    const response = await getUser();
    if (response.data.code === 200) {
      user.value = response.data.data;
      editedUser.value = { ...response.data.data };
    } else {
      console.error('Error in response:', response);
    }
  } catch (error) {
    console.error('Error fetching user information', error);
  }
});

const toggleEdit = () => {
  isEditing.value = !isEditing.value;

  if (!isEditing.value) {
    editedUser.value = { ...user.value };
  }
};

const saveChanges = async () => {
  try {
    const response = await editUser(editedUser.value);

    if (response.status === 200) {
      if (response.data.code === 200 && response.data.message === 'Profile updated successfully') {
        user.value = response.data.data;
        editedUser.value = { ...response.data.data };
        isEditing.value = false;
      } else {
        console.error('Update failed. Unexpected response:', response.data);
      }
    } else {
      console.error('Update failed. Unexpected status code:', response.status);
    }
  } catch (error) {
    console.error('Error saving changes', error);
  }
};

const openChangePasswordDialog = () => {
  currentPassword.value = '';
  newPassword.value = '';
  confirmPassword.value = '';
  passwordChangeError.value = '';
  isChangePasswordDialogOpen.value = true;
};

const closeChangePasswordDialog = () => {
  currentPassword.value = '';
  newPassword.value = '';
  confirmPassword.value = '';
  passwordChangeError.value = '';
  isChangePasswordDialogOpen.value = false;
};

const changePassword = async () => {
  try {
    if (newPassword.value !== confirmPassword.value) {
    passwordChangeError.value = 'New password and confirm password do not match.';
    return;
  }
    const response = await modifyPassword({
      currentPassword: currentPassword.value,
      newPassword: newPassword.value,
      confirmPassword: confirmPassword.value,
    });

    if (response.status === 200 && response.data.code === 200) {
      console.log('Password updated successfully');
      alert("修改成功")
      closeChangePasswordDialog();
    } else {
      console.error('Password update failed. Unexpected response:', response.data);
      passwordChangeError.value = 'Password update failed. Please check your information and try again.';
    }
  } catch (error) {
    console.error('Error modifying password', error);
    passwordChangeError.value = 'An unexpected error occurred. Please try again later.';
  }
};
</script>

<style scoped>
.profile-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: 'Arial', sans-serif;
}

.profile-content {
  max-width: 600px;
  width: 90%;
  background-color: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  margin: 20px auto;
  text-align: center;
}

.info-section {
  text-align: left;
  margin-bottom: 15px;
}

.buttons {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

button {
  padding: 10px;
  margin: 0 10px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #45a049;
}

.edit-form {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-top: 10px;
}

input {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.change-password-dialog {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.dialog-content {
  background-color: white;
  width: 35%;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
}

.error-message {
  color: red;
  margin-top: 10px;
}
</style>