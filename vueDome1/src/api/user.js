import service from './index.js';

// 注册
export function Register(data) {
  return service.request({
    method: "post",
    url: "/register/",
    data: data,
  });
}

// 登录
export function Login(data) {
  return service.request({
    method: "post",
    url: "/login/",
    data: data,
  });
}

// 修改密码
export function modifyPassword(data) {
  return service.request({
    method: "put",
    url: "/details/edit/",
    data: data,
  });
}

// 添加 Box
export function addBox(data) {
  return service.request({
    method: "post",
    url: "/leftBox/",
    data: data,
  });
}

// 登出
export function Logout(data) {
  return service.request({
    method: "post",
    url: "/org/logout",
    data: data,
  });
}

// 获取用户信息
export function getUser() {
  return service.request({
    method: "get",
    url: "/details/",
  });
}

// 编辑用户信息
export function editUser(data) {
  return service.request({
    method: "post",
    url: "/details/edit/",
    data: data,
  });
}

// 加载 Box
export function loadBox() {
  return service.request({
    method: "get",
    url: "/leftBox/",
  });
}

// 加载模型
export function loadmodels() {
  return service.request({
    method: "get",
    url: "/temp/ask/",
  });
}

// 加载角色
export function loadroles() {
  return service.request({
    method: "get",
    url: "/temp/ask/",
  });
}

// 编辑 Box 名称
export function editBoxName(data) {
  return service.request({
    method: "put",
    url: "/leftBox/",
    data: data,
  });
}

// 向模型提问
export function askToModel(data) {
  return service.request({
    method: "post",
    url: "/temp/ask/",
    data: data,
  });
}

// 发送聊天信息
export function sendChatMessage(data, chat_id) {
  return service.request({
    method: "post",
    url: `/temp/${chat_id}/history`,
    data: data,
  });
}

// 获取聊天历史记录
export function getChatHistory(chat_id) {
  return service.request({
    method: "get",
    url: `/temp/${chat_id}/history`,
  });
}

// 删除聊天记录
export function deleteChatBoxRecord(chat_id) {
  return service.request({
    method: "delete",
    url: `/temp/${chat_id}/history`,
  });
}

// 翻译
export function trans(data) {
  return service.request({
    method: "post",
    url: "/translate/",
    data: data,
  });
}

// 根据 Token 获取用户信息
export function getUserByToken(data) {
  return service.request({
    method: "post",
    url: "/org/signin",
    data: data,
  });
}

// 获取联系人数据
export function getContacts() {
  return service.request({
    method: "get",
    url: "/contacts",
  });
}

// 使用 Token 刷新
export function refreshByToken(data) {
  return service.request({
    method: "post",
    url: "/org/refreshtoken",
    data: data,
  });
}

//
export function getUsers(parent_id) {
  return service.request({
    method: "get",
    url: `/contacts/${parent_id}`,
  });
}

// 添加部门
export function addDepartment(data) {
  return service.request({
    method: "post",
    url: "/departments",
    data: data,
  });
}

// 更新部门信息
// export function updateDepartment(data) {
//   return service.request({
//     method: "put",
//     url: `/departments/${data.id}/`,
//     data: data,
//   });
// }

// 删除部门
export function deleteDepartment(id) {
  return service.request({
    method: "delete",
    url: `/departments/${id}/`,
  });
}

// 添加学生
export function addMember(data) {
  return service.request({
    method: "post",
    url: "/members",
    data: data,
  });
}

// 更新学生信息
export function updateMember(data) {
  return service.request({
    method: "put",
    url: `/members`,
    data: data,
  });
}


// 删除学生
export function deleteMember(id) {
  return service.request({
    method: "delete",
    url: `/members/${id}`,
  });
}

export function moveMembers(data) {
  return service.request({
    method: "put",
    url: `/members/move`,
    data:data
  });
}

export function getAdmins() {
  return service.request({
    method: "get",
    url: '/admine'
  })
}

export function getNoadmine() {
  return service.request({
    method: "get",
    url: '/notadmine'
  })
}

export function addAmine(data) {
  return service.request({
    method: "put",
    url: "/add-admin",
    data:data
  })
}

export function deleteAmine(data) {
  return service.request({
    method: "put",
    url: "/delete-admin",
    data:data
  })
}