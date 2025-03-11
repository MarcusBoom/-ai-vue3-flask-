from .exts import api
from .api import *

api.add_resource(Login, "/login/")
api.add_resource(Register, "/register/")
api.add_resource(UserProfileResource, "/details/")
api.add_resource(UpdateUserProfileResource, "/details/edit/")
api.add_resource(UserClass, "/leftBox/")
api.add_resource(Chat, "/temp/ask/")

api.add_resource(Contacts, '/contacts')
api.add_resource(getUsers, '/contacts/<int:parent_id>')
api.add_resource(AddDepartment, '/departments')
# api.add_resource(UpdateDepartment, '/departments/<int:id>/')
api.add_resource(DeleteDepartment, '/departments/<int:id>/')

# 新增成员、删除成员、更新成员的路由
api.add_resource(AddMember, '/members')
api.add_resource(DeleteMember, '/members/<int:id>')
api.add_resource(UpdateMember, '/members')  # 更新成员信息的路由
api.add_resource(moveMembers, '/members/move')

api.add_resource(getAdmine, '/admine')
api.add_resource(get_NO_admine, '/notadmine')
api.add_resource(AddAdmin, '/add-admin')  # 添加管理员
api.add_resource(deleteAdmin, '/delete-admin')  # 删除管理员，假设需要用户I


api.add_resource(Chat_History, "/temp/<int:chat_id>/history")
api.add_resource(Translator, "/translate/")
api.add_resource(RefreshTokenResource, '/org/refreshtoken')
