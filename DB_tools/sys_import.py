import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 设置django环境，否则无法使用django的ORM
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "datacenter_drf.settings")
django.setup()

# 导入模型
from apps.user.models import Router, Permission, Role, UserProfile

# 导入菜单数据
from DB_tools.sys_router import router_datas

# 导入权限数据
# from DB_tools.sys_permission import permission_datas
from DB_tools.sys_permission_en import permission_datas

# 导入角色数据
# from DB_tools.sys_role import role_datas
from DB_tools.sys_role_en import role_datas

# 导入用户数据
from DB_tools.sys_user import user_datas

# 导入角色权限数据
from DB_tools.sys_role_permission import role_permission_datas

# 导入用户角色数据
from DB_tools.sys_user_role import user_role_datas


# 导入菜单数据
def import_router():
    for router in router_datas:
        Router.objects.create(
            router_id=router["router_id"],
            # 如果sub_router有值，就取出对应的菜单对象，否则就是None
            sub_router=(
                Router.objects.get(router_id=router["sub_router"])
                if router["sub_router"]
                else None
            ),
            path=router["path"],
            component=router["component"],
            redirect=router["redirect"],
            name=router["name"],
            title=router["title"],
            icon=router["icon"],
            hidden=router["hidden"],
        )


# 导入权限数据
def import_permission():
    # 1.遍历权限名称
    for permission in permission_datas:
        # 遍历方法名
        for temp in permission["method"]:
            Permission.objects.create(
                method=temp,
                name=permission["name"],
                router_id=permission["router_id"],
                desc=permission["desc"],
            )


# 导入用户数据
def import_user():
    for user in user_datas:
        if user.get("avatar"):
            UserProfile.objects.create(
                id=user["id"],
                username=user["username"],
                password=user["password"],
                email=user["email"],
                mobile=user["mobile"],
                avatar=user["avatar"],
            )
        else:
            UserProfile.objects.create(
                id=user["id"],
                username=user["username"],
                password=user["password"],
                email=user["email"],
                mobile=user["mobile"],
                # is_active=user["is_active"],
                # is_staff=user["is_staff"],
                # is_superuser=user["is_superuser"],
            )


# 导入角色数据
def import_role():
    for role in role_datas:
        Role.objects.create(
            id=role["id"],
            name=role["name"],
            desc=role["desc"],
        )


# 导入角色权限数据
def import_role_permission():
    for role_permission_data in role_permission_datas:
        # 从数据库中获取，对应角色的对象
        role = Role.objects.get(id=role_permission_data["role_id"])
        for permission in role_permission_data["permission_id"]:
            # 从数据中获取，对应权限的对象
            permission = Permission.objects.filter(
                id__in=role_permission_data["permission_id"]
            )
            role.permission.set(permission)


# 导入用户角色
def import_user_role():
    for user_role_data in user_role_datas:
        # 从数据库中获取对应的用户对象
        user = UserProfile.objects.get(id=user_role_data["user_id"])
        # 从数据库中获取对应的角色对象
        roles = Role.objects.filter(id__in=user_role_data["role_id"])
        # 将角色对象关联到用户对象
        user.role.set(roles)


if __name__ == "__main__":
    import_router()
    import_permission()
    import_role()
    import_user()
    import_role_permission()
    import_user_role()
    print("sys导入成功")
