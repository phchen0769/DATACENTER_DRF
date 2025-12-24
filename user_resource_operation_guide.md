# 如何判断用户对某一资源的可行操作

## 1. 概述

在本系统中，用户对资源的操作权限通过RBAC模型进行控制。权限不仅决定了用户能否访问某个路由，还决定了用户能在该路由上执行哪些操作（如GET、POST、PUT、DELETE等）。本文档将详细介绍如何判断用户对资源的具体操作权限。

## 2. 权限判断机制

### 2.1 权限验证流程

系统通过以下步骤判断用户是否有权执行某项操作：

1. 用户发起请求（包含URL和HTTP方法）
2. 系统获取当前用户信息
3. 根据用户角色获取其所有权限
4. 检查请求的URL名称和HTTP方法是否匹配用户权限
5. 返回验证结果（允许或拒绝访问）

### 2.2 权限判断核心代码

在 [utils/permission.py](file:///workspaces/DATACENTER_DRF/utils/permission.py) 中实现了自定义权限类 [CustomPermission](file:///workspaces/DATACENTER_DRF/utils/permission.py#L9-L68)：

```python
def has_permission(self, request, view):
    # 1. 创建权限字典，获取当前用户所有权限
    permission_dict = {}
    user = request.user
    roles = user.role.all()
    
    # 对每个角色获取其所有的权限
    for role in roles:
        permissions = role.permission.all()
        for permission in permissions:
            method_list = []
            method_list.append(permission.method)
            
            # 构建权限字典：{权限名: [方法列表]}
            if permission_dict.get(permission.name):
                permission_dict[permission.name].extend(method_list)
                permission_dict[permission.name] = list(
                    set(permission_dict[permission.name])
                )
            else:
                permission_dict[permission.name] = list(method_list)

    # 2. 获取当前请求的URL名称和方法
    url_name = request.resolver_match.url_name
    
    # 3. 权限判断
    method_list = permission_dict.get(url_name)
    if not method_list:
        return False
    if request.method in method_list:
        return True
    return False
```

## 3. 不同类型操作的处理方式

### 3.1 路由级别操作（如list）

路由级别的操作通常对应列表展示功能，例如获取用户列表：

- 权限命名：`{资源名}-list`（如 [users-list](file:///workspaces/DATACENTER_DRF/DB_tools/sys_permission_en.py#L22-L27)）
- HTTP方法：通常是GET或POST
- 前端体现：整个页面或页面的主要内容区域
- 权限数据示例：
```python
{
    "name": "users-list",
    "method": ["GET", "POST"],
    "router_id": 2001,
    "desc": "User management permissions",
}
```

### 3.2 对象级别操作（如put/update）

对象级别的操作通常对应具体资源的修改操作，例如更新单个用户信息：

- 权限命名：`{资源名}-detail`（如 [users-detail](file:///workspaces/DATACENTER_DRF/DB_tools/sys_permission_en.py#L28-L33)）
- HTTP方法：通常是PUT、PATCH、DELETE或GET（查看详情）
- 前端体现：页面内的操作按钮（编辑、删除等）
- 权限数据示例：
```python
{
    "name": "users-detail",
    "method": ["GET", "DELETE", "PUT", "PATCH", "OPTIONS"],
    "router_id": 2002,
    "desc": "User management permissions",
}
```

## 4. 前端权限控制实践

### 4.1 页面访问控制

前端根据用户可访问的路由列表渲染菜单和页面：

```javascript
// 伪代码示例
const userRouters = await api.getUserRouters();
renderMenu(userRouters);
```

用户路由获取逻辑在后端 [UserProfile.get_routers()](file:///workspaces/DATACENTER_DRF/apps/user/models.py#L161-L183) 方法中实现：

```python
def get_routers(self):
    if self.is_anonymous:
        routers = []
        return routers
    else:
        # 获取该用户所有角色
        roles = self.role.all()
        # 获取所有角色的权限
        permissions = Permission.objects.filter(role__in=roles)
        # 获取所有权限的子菜单
        child_routers = Router.objects.filter(permission__in=permissions)
        # 获取所有的上级菜单
        sub_routers = Router.objects.filter(sub_router__isnull=True)
        # 获取所有权限的上级菜单
        routers = sub_routers.filter(
            router_id__in=child_routers.values("sub_router_id")
        )
        # 合并上级菜单和子菜单
        all_routers = routers | child_routers
        return all_routers
```

### 4.2 操作按钮显示控制

前端根据用户权限决定是否显示特定操作按钮：

```vue
<!-- Vue.js 伪代码示例 -->
<template>
  <div>
    <!-- 只有拥有users-detail权限且方法包含PUT的用户才能看到编辑按钮 -->
    <button v-if="hasPermission('users-detail', 'PUT')">编辑</button>
    
    <!-- 只有拥有users-detail权限且方法包含DELETE的用户才能看到删除按钮 -->
    <button v-if="hasPermission('users-detail', 'DELETE')">删除</button>
  </div>
</template>
```

## 5. 权限设计最佳实践

### 5.1 权限粒度控制

1. **列表操作**（list）：
   - 控制整个资源集合的访问权限
   - 通常对应页面访问权限
   
2. **详情操作**（detail）：
   - 控制单个资源的访问权限
   - 细分为GET（查看）、PUT/PATCH（更新）、DELETE（删除）等

### 5.2 权限命名规范

- 列表操作：`{资源名}-list`（如 articles-list）
- 详情操作：`{资源名}-detail`（如 articles-detail）
- 特殊操作：`{资源名}-{操作名}`（如 articles-publish）

### 5.3 权限与路由关联

每条权限记录都与特定路由相关联：

```python
{
    "name": "users-list",      # 权限名称
    "method": ["GET", "POST"], # 支持的HTTP方法
    "router_id": 2001,         # 关联的路由ID
    "desc": "User management permissions",  # 权限描述
}
```

## 6. 实际应用场景

### 6.1 用户管理页面

1. 用户访问 `/user/manage` 页面：
   - 需要 [users-list](file:///workspaces/DATACENTER_DRF/DB_tools/sys_permission_en.py#L22-L27) 权限（GET方法）
   - 如果没有此权限，则无法访问该页面

2. 在页面中显示"新增用户"按钮：
   - 需要 [users-list](file:///workspaces/DATACENTER_DRF/DB_tools/sys_permission_en.py#L22-L27) 权限（POST方法）
   - 前端检查用户是否拥有此权限

3. 在用户列表中显示"编辑"按钮：
   - 需要 [users-detail](file:///workspaces/DATACENTER_DRF/DB_tools/sys_permission_en.py#L28-L33) 权限（PUT/PATCH方法）
   - 前端按需显示

4. 在用户列表中显示"删除"按钮：
   - 需要 [users-detail](file:///workspaces/DATACENTER_DRF/DB_tools/sys_permission_en.py#L28-L33) 权限（DELETE方法）
   - 前端按需显示

### 6.2 权限检查顺序

当用户尝试执行操作时，系统按照以下顺序进行权限检查：

1. 路由访问权限（页面级别）
2. HTTP方法权限（操作级别）
3. 具体业务权限（如有特殊要求）

只有通过所有层级的权限检查，用户才能成功执行相应操作。