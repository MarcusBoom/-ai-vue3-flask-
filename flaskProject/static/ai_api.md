openapi: 3.0.0
info:
  title: 用户信息修改 API
  description: 提供用户修改个人信息的接口
  version: 1.0.0
servers:
  - url: https://api.example.com

paths:
  /user:
    put:
      summary: 修改用户信息
      description: 允许用户修改其个人信息
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserUpdatePayload'
      responses:
        '200':
          description: 成功更新用户信息
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          description: 无效的请求参数
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
        '401':
          description: 未授权访问
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
          description: 用户 ID
        name:
          type: string
          description: 用户名
        email:
          type: string
          format: email
          description: 用户邮箱
      required:
        - id
        - name
        - email
    UserUpdatePayload:
      type: object
      properties:
        name:
          type: string
          description: 新的用户名
        email:
          type: string
          format: email
          description: 新的用户邮箱
      required:
        - name
        - email
    ErrorResponse:
      type: object
      properties:
        error:
          type: string