<template>
    <div id="admin" class="admin-container" :class="{ 'dialog-open': isDialogVisible }">
      <h1>管理员信息</h1>
      <el-card class="admin-card">
        <h3>管理员</h3>
        <el-table ref="adminTable" :data="adminTableData">
          <el-table-column prop="username" label="姓名" width="120"></el-table-column>
          <el-table-column prop="position" label="职位" width="120"></el-table-column>
          <el-table-column prop="id" label="工号" width="120"></el-table-column>
          <el-table-column prop="phone" label="手机号" width="120"></el-table-column>
          <el-table-column prop="partment" label="部门" width="120"></el-table-column>
          <el-table-column label="操作" width="100">
            <template #default="scope">
              <el-button type="text" @click="deleteAdmin(scope.row.id)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-button type="primary" @click="openDialog">添加管理员</el-button>
      </el-card>
  
      <div v-if="isDialogVisible" class="custom-dialog">
        <div class="custom-dialog-content">
          <el-tree
            :data="usersTree"
            show-checkbox
            node-key="id"
            :props="defaultProps"
            @check="handleCheck"
          ></el-tree>
          <div class="dialog-footer">
            <el-button @click="closeDialog">取消</el-button>
            <el-button type="primary" @click="confirmAddAdmin">确认</el-button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import 'element-plus/dist/index.css';
  import { ElMessage } from 'element-plus'
  import { getAdmins, getNoadmine, addAmine, deleteAmine } from '../api/user'
  
  const isDialogVisible = ref(false)
  const adminTableData = ref([])
  const usersTree = ref([])
  const selectedUserIds = ref([])
  const defaultProps = ref({
    children: 'children',
    label: 'label'
  })
  
  const fetchAdmins = () => {
    getAdmins()
      .then(response => {
        if (response.data) {
          adminTableData.value = response.data;
        } else {
          console.error('返回的数据结构不正确:', response.data);
          ElMessage.error('返回的数据结构不正确!');
        }
      }).catch(error => {
        console.error('获取管理员信息时出错:', error);
        ElMessage.error('获取管理员信息时出错!');
      });
  }
  
  onMounted(() => {
    fetchAdmins()
  })
  
  const openDialog = () => {
    isDialogVisible.value = true;
    fetchNonAdminUsers()
  };
  
  const closeDialog = () => {
    isDialogVisible.value = false;
  };
  
  const deleteAdmin = async (adminId) => {
    try {
      await deleteAmine(adminId)
      ElMessage.success('管理员删除成功')
      await fetchAdmins() // Refresh admin table
    } catch (error) {
      console.error(error)
      ElMessage.error('删除管理员失败')
    }
  };
  
  const fetchNonAdminUsers = async () => {
    try {
      const response = await getNoadmine()
      usersTree.value = Object.entries(response.data).map(([department, users]) => ({
        label: department,
        children: users.map(user => ({
          id: user.id,
          label: user.username
        }))
      }))
    } catch (error) {
      console.error(error)
    }
  }
  
  const handleCheck = (checkedNodes, checkedKeys) => {
    selectedUserIds.value = checkedKeys
  }
  
  const confirmAddAdmin = async () => {
    try {
      await addAmine(selectedUserIds.value.checkedKeys)
      ElMessage.success('管理员添加成功')
      closeDialog()
      await fetchAdmins() // Refresh admin table
    } catch (error) {
      console.error(error)
      ElMessage.error('添加管理员失败')
    }
  }
  
  </script>
  
  <style scoped>
  /* 弹窗样式 */
  .custom-dialog {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.6); /* 半透明背景，阻止下方内容交互 */
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000; /* 高 z-index 值确保弹窗在最上方 */
  }
  
  .custom-dialog-content {
    background-color: #fff; /* 弹窗背景色 */
    padding: 20px;
    border-radius: 10px; /* 圆角边框 */
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 阴影效果 */
    max-width: 500px; /* 弹窗最大宽度 */
    width: 100%; /* 弹窗宽度 */
    overflow: hidden; /* 防止内容溢出 */
  }
  
  .custom-dialog-content h3 {
    margin-top: 0; /* 移除标题的默认上边距 */
  }
  
  .dialog-footer {
    display: flex;
    justify-content: flex-end;
    margin-top: 20px; /* 为按钮留出空间 */
  }
  
  /* 按钮样式 */
  .dialog-footer button {
    margin-left: 10px; /* 按钮间隔 */
  }
  
  /* 当弹窗打开时，禁用页面滚动 */
  .admin-container.dialog-open {
    overflow: hidden; /* 禁止滚动 */
  }
  </style>
  