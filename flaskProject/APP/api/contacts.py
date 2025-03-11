from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.testing.pickleable import User
from werkzeug.security import generate_password_hash, check_password_hash
from APP.models import *

class Contacts(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        top_departments = Department.query.filter_by(parent_id=-1).all()
        department_tree = []

        def build_tree(department):
            children = Department.query.filter_by(parent_id=department.department_id).all()
            return {
                'id': department.department_id,
                'label': department.department,
                'children': [build_tree(child) for child in children]
            }

        for top_dept in top_departments:
            department_tree.append(build_tree(top_dept))
        return jsonify(department_tree)


class getUsers(Resource):
    @jwt_required()
    def get(self, parent_id):
        current_user = get_jwt_identity()
        members = []

        def get_department_members(department_id):
            department = Department.query.get_or_404(department_id)
            # Fetch members directly under this department
            # department_members = Users.query.filter_by(department_id=department_id).all()
            department_members = Users.query.filter_by(department_id=department_id).all()

            members.extend(department_members)

            # Recursively fetch members from child departments
            children_departments = Department.query.filter_by(parent_id=department_id).all()
            for child in children_departments:
                get_department_members(child.department_id)

        get_department_members(parent_id)

        serialized_members = [{
            'id': member.id,
            'name': member.name,
            'username': member.username,
            'position': member.position,
            'phone': member.phone,
            'admine': member.admine
        } for member in members]
        # print(serialized_members)
        return jsonify(serialized_members)



class AddDepartment(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        print(data)
        new_department = Department(
            department=data['name'],
            parent_id=data['parent_id'],
        )
        db.session.add(new_department)
        db.session.commit()
        return jsonify({'id': new_department.department})


class UpdateDepartment(Resource):
    @jwt_required()
    def put(self, id):
        data = request.get_json()
        department = Department.query.get_or_404(id)
        department.department = data['label']
        db.session.commit()
        return jsonify({'message': 'Department updated successfully'})


class DeleteDepartment(Resource):
    @jwt_required()
    def delete(self, id):
        print(id)
        getuser = getUsers()
        department = Department.query.filter_by(department_id=id).first()
        partment = getuser.get(parent_id=id)
        print(partment.content_length)
        if partment.content_length > 3:
            print("有成员")
            return jsonify({'code': 222, 'message': 'have partment'})
        else:
            db.session.delete(department)
            db.session.commit()
            return jsonify({'message': 'Department deleted successfully'})


class AddMember(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        print(data)
        hashed_password = generate_password_hash('123456')
        new_member = Users(
            name=data['name'],
            username=data['username'],
            position=data['position'],
            phone=data['phone'],
            department_id=data['department_id'],
            password=hashed_password
        )
        db.session.add(new_member)
        db.session.commit()
        return jsonify({'message': 'Member added successfully', 'id': new_member.id})


class DeleteMember(Resource):
    @jwt_required()
    def delete(self, id):
        member = Users.query.filter_by(id=id).first()
        if not member:
            return jsonify({'message': 'Member not found'}), 404
        db.session.delete(member)
        db.session.commit()
        return jsonify({'message': 'Member deleted successfully'})


class UpdateMember(Resource):
    @jwt_required()
    def put(self):
        data = request.get_json()
        print(data)
        member = Users.query.filter_by(id=data['id']).first()
        member.name = data['name']
        member.username = data['username']
        member.position = data['position']
        member.phone = data['phone']
        print(member.username)
        db.session.commit()
        return jsonify({'message': 'Member updated successfully'})

class moveMembers(Resource):
    @jwt_required()
    def put(self):
        data = request.get_json()
        print(data)
        for member_id in data['member_id']:
            member = Users.query.filter_by(id=member_id).first()
            member.department_id = data['department_id']
        db.session.commit()
        return jsonify({'message': 'Member updated successfully'})

class getAdmine(Resource):
    @jwt_required()
    def get(self):
        admines = Users.query.filter_by(admine=True).all()
        json_admines = [{
            'id':admine.id,
            'name': admine.name,
            'position': admine.position,
            'username':admine.username,
            'phone': admine.phone,
        } for admine in admines]
        return jsonify(json_admines)
        # admine = [i for i in user if user['admine']=='t']
        # print(admine)


class get_NO_admine(Resource):
    def get(self):
        # 获取所有非管理员用户
        non_admin_users = Users.query.filter_by(admine=False).all()
        # 获取所有部门
        departments = Department.query.all()
        # 构建部门与用户的树形结构
        department_dict = {dept.department_id: dept.department for dept in departments}
        users_tree = {}
        for user in non_admin_users:
            dept_name = department_dict.get(user.department_id, 'Other')
            if dept_name not in users_tree:
                users_tree[dept_name] = []
            users_tree[dept_name].append({
                'id': user.id,
                'username': user.username,
                'name': user.name,
                'position': user.position
            })
        return jsonify(users_tree)

class AddAdmin(Resource):
    def put(self):
        user_ids = request.get_json()

        # 将用户ID列表中的每个ID转换为整数
        user_ids = [int(user_id) for user_id in user_ids if user_id is not None]
        print(user_ids)
        # 遍历用户ID列表，更新用户的角色为管理员
        for user_id in user_ids:
            user = Users.query.filter_by(id=user_id).first()
            if user:
                print(user.admine)
                user.admine = True
                db.session.commit()
        return {'code':'200','message': 'Admins added successfully'}


class deleteAdmin(Resource):
    def put(self):
        user_id = request.get_json()
        user = Users.query.filter_by(id=user_id).first()
        user.admine = False
        db.session.commit()
        return {'code': '200', 'message': 'Admins deleted successfully'}