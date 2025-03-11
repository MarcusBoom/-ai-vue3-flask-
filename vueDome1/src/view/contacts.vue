<template>
  <div>
    <el-container style="height: 100vh;">
      <!-- 左侧菜单栏 -->
      <el-aside width="300px" style="background-color: #f2f2f2;">
        <!-- 部门树形菜单 -->
        <el-tree
          :data="departmentTree"
          :props="defaultProps"
          node-key="id"
          highlight-current
          @node-click="handleNodeClick"
        >
          <!-- 自定义节点内容模板 -->
          <template #default="{ node, data }">
            <span>{{ node.label }}</span>
          </template>
        </el-tree>
      </el-aside>
      <!-- 右侧主内容区域 -->
      <el-main>
        <el-button type="primary" @click="goAdmine">管理员</el-button>
        <div v-if="selectedNode">
          <!-- 只有选中部门时才显示详情 -->
          <h3>子部门</h3>
          <!-- 操作按钮 -->
          <el-button type="primary" @click.stop="showAddGroupDialog">新增分组</el-button>
          
          <!-- 子部门列表 -->
          <el-table :data="subDepartments" v-if="subDepartments.length > 0">
            <el-table-column prop="label" label="子部门名称"></el-table-column>
          </el-table>
          <p v-else>暂无子部门信息</p>

          <p>
            <!-- 部门名称 -->
            <strong>部门名称：</strong>
            {{ selectedNode.label }}
            <el-button type="danger" @click="deleteGroup(selectedNode)">删除该分组</el-button>
          </p>
          <!-- 查找输入框 -->
          <el-input
            placeholder="搜索成员"
            v-model="searchQuery"
            clearable
            @input="filterMembers"
            style="margin-bottom: 20px;"
          ></el-input>

          <!-- 成员列表表格 -->
          <el-table :data="filteredMembers" v-if="filteredMembers.length > 0" @selection-change="handleSelectionChange">
            <el-table-column type="selection" width="55"></el-table-column>
            <el-table-column prop="name" label="姓名">
              <template #default="scope">
                <el-input v-model="scope.row.name" v-if="scope.row.isEditing" placeholder="请输入姓名"></el-input>
                <span v-else>{{ scope.row.name }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="username" label="工号">
              <template #default="scope">
                <el-input v-model="scope.row.username" v-if="scope.row.isEditing" placeholder="请输入工号"></el-input>
                <span v-else>{{ scope.row.username }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="position" label="职位">
              <template #default="scope">
                <el-input v-model="scope.row.position" v-if="scope.row.isEditing" placeholder="请输入职位"></el-input>
                <span v-else>{{ scope.row.position }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="phone" label="电话">
              <template #default="scope">
                <el-input v-model="scope.row.phone" v-if="scope.row.isEditing" placeholder="请输入电话"></el-input>
                <span v-else>{{ scope.row.phone }}</span>
              </template>
            </el-table-column>
            <el-table-column label="操作">
              <template #default="scope">
                <el-button type="primary" size="small" @click="editStudent(scope.row)" v-if="!scope.row.isEditing">编辑</el-button>
                <el-button type="primary" size="small" @click="saveStudent(scope.row)" v-else>保存</el-button>
                <el-button type="danger" size="small" @click="deleteStudent(scope.row)" v-if="!scope.row.isEditing">删除</el-button>
                <el-button type="danger" size="small" @click="canceledit(scope.row)" v-else>取消</el-button>
              </template>
            </el-table-column>
          </el-table>
          <p v-else>暂无成员信息</p>
          <!-- 批量删除按钮 -->
          <el-button type="danger" @click="batchDeleteMembers">批量删除</el-button>
          <!-- 添加成员按钮 -->
          <el-button type="primary" @click="addNewMember">新增成员</el-button>
          <el-button type="info" @click.stop="batchMoveMembers">批量移动成员</el-button>

        </div>
      </el-main>

      <!-- 新增分组弹窗 -->
      <div class="custom-dialog" v-if="addGroupDialogVisible">
        <div class="custom-dialog-content">
          <h3>新增分组</h3>
          <el-input v-model="newGroupName" placeholder="请输入新分组名称"></el-input>
          <div class="dialog-buttons">
            <el-button @click="addGroupDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="addSubGroup">确定</el-button>
          </div>
        </div>
      </div>

      <div class="custom-dialog" v-if="moveMembersDialogVisible">
        <el-tree
          :data="departmentTree"
          :props="defaultProps"
          node-key="id"
          highlight-current
          @node-click="handleTargetNodeClick"
        ></el-tree>
        <div slot="footer" class="dialog-footer">
          <el-button @click="moveMembersDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="moveMembersConfirm">确定</el-button>
        </div>
      </div>
    </el-container>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import {
  getContacts,
  getUsers,
  addDepartment,
  deleteDepartment,
  addMember,
  updateMember,
  deleteMember,
  moveMembers
} from '../api/user.js';

// 响应式变量
const departmentTree = ref([]);       // 部门树数据
const selectedNode = ref(null);       // 当前选中的节点信息
const selectedMembers = ref([]);      // 当前选中部门及其子部门的成员列表
const subDepartments = ref([]);       // 当前选中的部门的子部门
const addGroupDialogVisible = ref(false); // 新增分组弹窗显示状态
const newGroupName = ref('');         // 新分组名称
const targetGroup = ref(null);        // 选中的目标部门
const moveMembersDialogVisible = ref(false); // 移动成员对话框显示状态
const selected = ref([])
const router = useRouter();
const filteredMembers = ref([]);
const searchQuery = ref('');



// 组件挂载后获取部门树数据
onMounted(async () => {
  try {
    
    const response = await getContacts();
    departmentTree.value = response.data;  // 更新部门树数据
  } catch (error) {
    console.error('获取部门数据失败:', error);
    ElMessage({
      type: 'error',
      message: '获取部门数据失败'
    });
  }
});

// 部门树组件属性配置
const defaultProps = {
  children: 'children',   // 子节点数据字段名
  label: 'label'          // 节点显示文本字段名
};

// 处理部门树节点点击事件
const handleNodeClick = async (data) => {
  try {
    const response = await getUsers(data.id);  // 获取点击部门的成员数据
    selectedNode.value = data;         // 更新选中节点信息为当前点击的部门信息
    selectedMembers.value = response.data;   // 更新选中成员列表为部门成员信息
    filteredMembers.value = selectedMembers.value; // 初始化过滤后的成员列表
    subDepartments.value = data.children || []; // 更新子部门列表
  } catch (error) {
    console.error('获取分组成员失败:', error);
    ElMessage({
      type: 'error',
      message: '获取分组成员失败'
    });
  }
};

// 显示新增分组弹窗
const showAddGroupDialog = () => {
  addGroupDialogVisible.value = true;
};

// 新增分组逻辑
const addSubGroup = async () => {
  if (!newGroupName.value) {
    ElMessage({
      type: 'warning',
      message: '请输入新分组名称'
    });
    return;
  }

  try {
    const response = await addDepartment({
      parent_id: selectedNode.value.id,
      name: newGroupName.value
    });

    // 添加成功后刷新树并打开新添加的分组
    await getContacts().then(res => {
      departmentTree.value = res.data;
    });
    handleNodeClick(selectedNode.value); // 刷新当前节点
    addGroupDialogVisible.value = false; // 关闭弹窗
    newGroupName.value = ''; // 清空输入框
  } catch (error) {
    console.error('添加分组失败:', error);
    ElMessage({
      type: 'error',
      message: '添加分组失败'
    });
  }
};

// 添加新成员
const addNewMember = () => {
  selectedMembers.value.push({
    new:true,
    name: '',
    username: '',
    position: '',
    phone: '',
    isEditing: true  // 标记为编辑状态
  });
};

// 编辑成员逻辑
const editStudent = (student) => {
  student.isEditing = true;
};

//取消编辑
const canceledit = async(student) => {
  await handleNodeClick(selectedNode.value)
  student.isEditing = false;
};

// 保存成员逻辑
const saveStudent = async (student) => {
  if (!student.name ) {
    ElMessage({
      type: 'warning',
      message: '请填写完整的成员信息'
    });
    return;
  }

  student.isEditing = false;

  try {
    if (student.new) {
      // 新增成员逻辑
      console.log(student.id)
      const response = await addMember({
        department_id: selectedNode.value.id,
        ...student
      });
      student.id = response.data.id;  // 更新实际 ID
      ElMessage({
        type: 'success',
        message: '添加成员成功'
      });
    } else {
      // 更新成员逻辑
      const response = await updateMember(student);
      ElMessage({
        type: 'success',
        message: '编辑成员成功'
      });
    }
  } catch (error) {
    console.error('保存成员失败:', error);
    ElMessage({
      type: 'error',
      message: '保存成员失败'
    });
  }

  // 刷新成员列表
  handleNodeClick(selectedNode.value);
};

// 删除部门逻辑
const deleteGroup = async (node) => {
  // 使用 ElMessageBox 弹出确认对话框
  ElMessageBox.confirm('此操作将永久删除该分组, 是否继续?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      const response = await deleteDepartment(node.id);
      if (response.data.code == 222) {
        ElMessage({
          type: 'warning',
          message: '该分组中有成员，不能删除'
        });
      } else {
        // 重新加载部门树数据
        await getContacts().then(res => {
          departmentTree.value = res.data;
        });
        // 清空选中状态
        selectedNode.value = null;
        selectedMembers.value = [];
        ElMessage({
          type: 'success',
          message: '删除成功'
        });
      }
    } catch (error) {
      console.error('删除分组失败:', error);
      ElMessage({
        type: 'error',
        message: '删除分组失败'
      });
    }
  }).catch(() => {
    // 用户点击取消时执行的操作
    ElMessage({
      type: 'info',
      message: '已取消删除'
    });
  });
};

// 删除成员逻辑
const deleteStudent = async (student) => {
  // 使用 ElMessageBox 弹出确认对话框
  ElMessageBox.confirm('此操作将永久删除该成员, 是否继续?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      const response = await deleteMember(student.id);
      // 删除成功后刷新成员列表
      handleNodeClick(selectedNode.value);
      ElMessage({
        type: 'success',
        message: '删除成员成功'
      });
    } catch (error) {
      console.error('删除成员失败:', error);
      ElMessage({
        type: 'error',
        message: '删除成员失败'
      });
    }
  }).catch(() => {
    // 用户点击取消时执行的操作
    ElMessage({
      type: 'info',
      message: '已取消删除'
    });
  });
};

const handleSelectionChange = (selection) => {
   selected.value = selection;
   console.log(selected)
}

// 批量删除成员逻辑
const batchDeleteMembers = () => {
  const selectedIds = selected.value.map(member => member.id);
  console.log("处理批量删除",selectedIds)
  if (selectedIds.length === 0) {
    ElMessage({
      type: 'warning',
      message: '请选择要删除的成员'
    });
    return;
  }
  console.log(selectedIds)
  ElMessageBox.confirm('此操作将永久删除选中的成员, 是否继续?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await Promise.all(selectedIds.map(id => deleteMember(id)));
      handleNodeClick(selectedNode.value);
      ElMessage({
        type: 'success',
        message: '批量删除成员成功'
      });
    } catch (error) {
      console.error('批量删除成员失败:', error);
      ElMessage({
        type: 'error',
        message: '批量删除成员失败'
      });
    }
  }).catch(() => {
    // 用户点击取消时执行的操作
    ElMessage({
      type: 'info',
      message: '已取消批量删除'
    });
  });
};

// 显示批量移动成员对话框
const batchMoveMembers = () => {
  moveMembersDialogVisible.value = true;
};

// 处理目标部门节点点击事件
const handleTargetNodeClick = (data) => {
  targetGroup.value = data;
};

// 确认移动成员操作
const moveMembersConfirm = async () => {
  if (!targetGroup.value) {
    ElMessage({
      type: 'warning',
      message: '请选择目标部门'
    });
    return;
  }

  const memberIds = selected.value.map(member => member.id);
  try {
    await moveMembers({member_id:memberIds,department_id: targetGroup.value.id});
    ElMessage({
      type: 'success',
      message: '批量移动成员成功'
    });
    moveMembersDialogVisible.value = false; // 关闭对话框
    handleNodeClick(selectedNode.value); // 刷新成员列表
  } catch (error) {
    console.error('移动成员失败:', error);
    ElMessage({
      type: 'error',
      message: '移动成员失败'
    });
  }
};

//过滤成员
const filterMembers = () => {
  if (!searchQuery.value) {
    filteredMembers.value = selectedMembers.value;
  } else {
    console.log("search",searchQuery.value)
    filteredMembers.value = selectedMembers.value.filter(member => 
      // member.name.includes(searchQuery.value) ||
      // member.username.includes(searchQuery.value) ||
      // member.position.includes(searchQuery.value) ||
      // member.phone.includes(searchQuery.value)
      member.name.includes(searchQuery.value) 
    );
    console.log(filteredMembers.value)
  }
};

const goAdmine = () => {
  router.push('/admine');
};
</script>

<style scoped>
.custom-dialog {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: white;
  padding: 20px;
  border: 1px solid #ccc;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 9999; /* 确保弹窗在最前面 */
}

.custom-dialog-content {
  text-align: center;
}

.dialog-buttons {
  text-align: right;
  margin-top: 10px;
}

.form-buttons {
  text-align: right;
  margin-top: 10px;
}
</style>
