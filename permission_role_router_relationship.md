# 权限、角色权限、路由关系说明

## 1. 概述

本系统采用基于角色的访问控制（RBAC）模型来管理用户权限。主要包括三个核心概念：
- **路由(Router)**：前端页面导航路径
- **权限(Permission)**：对特定资源的操作许可
- **角色(Role)**：一组权限的集合，分配给用户

这三者之间存在紧密的关系，共同构成了系统的安全访问控制体系。

## 2. 数据模型关系

### 2.1 基本结构

```
UserProfile (用户) ——< Role (角色) >——< Permission (权限) —— Router (路由)
     1           n      1         n      1              1
```

### 2.2 详细说明

#### Router（路由）
- 表示前端页面的路由信息
- 包含字段：
  - `router_id`: 路由ID（主键）
  - `sub_router`: 上级路由（外键，指向自身）
  - `path`: 页面路径
  - `component`: 组件名称
  - `name/title/icon`: 显示相关信息
  - `hidden`: 是否隐藏
- 路由分为两类：
  - 主路由：顶级菜单项，[sub_router](file:///workspaces/DATACENTER_DRF/apps/user/models.py#L23-L31)为NULL
  - 子路由：具体的页面路由，[sub_router](file:///workspaces/DATACENTER_DRF/apps/user/models.py#L23-L31)指向所属的主路由

#### Permission（权限）
- 表示对特定资源的操作权限
- 包含字段：
  - `name`: 权限名称（通常对应URL别名）
  - `method`: 请求方法（GET、POST、PUT、DELETE等）
  - `desc`: 描述信息
  - `router`: 关联的路由（外键）
- 每个权限精确绑定到一个特定的路由上
- 同一路由可能有多个不同方法的权限

#### Role（角色）
- 表示一组权限的集合
- 包含字段：
  - `name`: 角色名称
  - `desc`: 描述信息
  - `permission`: 多对多关联权限
- 角色是连接用户和权限的桥梁

#### UserProfile（用户）
- 系统用户模型，继承自Django的AbstractUser
- 通过多对多关系关联角色：
  - `role`: 多对多关联角色

## 3. 工作流程

### 3.1 用户访问流程

1. 用户登录系统
2. 根据用户的角色获取所有权限
3. 根据权限找到对应的路由
4. 构建用户的可访问路由树
5. 前端根据路由信息渲染菜单和页面

### 3.2 权限验证流程

1. 用户发起请求
2. 系统检查请求的URL和方法是否匹配用户拥有的权限
3. 如果匹配则允许访问，否则拒绝访问

## 4. 数据初始化

系统通过以下文件进行数据初始化：

### 4.1 路由数据 ([sys_router.py](file:///workspaces/DATACENTER_DRF/DB_tools/sys_router.py))
- 定义所有前端路由信息
- 每个路由都有唯一的router_id
- 通过[sub_router](file:///workspaces/DATACENTER_DRF/apps/user/models.py#L23-L31)字段建立父子路由关系

示例：
```python
{
    "router_id": 2000,           # 路由ID
    "sub_router": None,          # 上级路由（None表示为主路由）
    "path": "/user",             # 路径
    "component": "layout",       # 组件
    "name": "userManage",        # 名称
    "title": "user",             # 标题
    "icon": "personnel",         # 图标
}
```

### 4.2 权限数据 ([sys_permission_en.py](file:///workspaces/DATACENTER_DRF/DB_tools/sys_permission_en.py))
- 定义所有权限点
- 每个权限关联一个路由ID
- 支持多种HTTP方法

示例：
```python
{
    "name": "users-list",        # 权限名称
    "method": ["GET", "POST"],   # 支持的方法
    "router_id": 2001,           # 关联的路由ID
    "desc": "User management permissions",  # 描述
}
```

### 4.3 角色数据 ([sys_role_en.py](file:///workspaces/DATACENTER_DRF/DB_tools/sys_role_en.py))
- 定义系统角色
- 每个角色有唯一标识和描述

示例：
```python
{
    "id": 1,                     # 角色ID
    "name": "admin",             # 角色名称
    "desc": "Administrator...",  # 描述
}
```

### 4.4 角色权限关联 ([sys_role_permission.py](file:///workspaces/DATACENTER_DRF/DB_tools/sys_role_permission.py))
- 定义角色与权限的多对多关系
- 每个角色关联一组权限ID

示例：
```python
{
    "role_id": 1,                # 角色ID
    "permission_id": [1,2,3...]  # 权限ID列表
}
```

## 5. 实际应用示例

假设要为管理员角色添加用户管理功能：

1. 在[sys_router.py](file:///workspaces/DATACENTER_DRF/DB_tools/sys_router.py)中添加路由：
   ```python
   {
       "router_id": 2001,
       "sub_router": 2000,
       "path": "/user/manage",
       "component": "user-manage",
       "title": "userManage",
       # ...
   }
   ```

2. 在[sys_permission_en.py](file:///workspaces/DATACENTER_DRF/DB_tools/sys_permission_en.py)中添加权限：
   ```python
   {
       "name": "users-list",
       "method": ["GET", "POST"],
       "router_id": 2001,
       "desc": "User management permissions",
   }
   ```

3. 在[sys_role_permission.py](file:///workspaces/DATACENTER_DRF/DB_tools/sys_role_permission.py)中将权限赋予管理员角色：
   ```python
   {
       "role_id": 1,  # 管理员角色
       "permission_id": [..., 新权限ID],
   }
   ```

## 6. 注意事项

1. 路由ID必须全局唯一
2. 权限名称应该具有描述性且唯一
3. 角色权限分配要考虑最小权限原则
4. 删除路由时需要同步清理相关权限
5. 修改权限时要注意对现有用户的影响