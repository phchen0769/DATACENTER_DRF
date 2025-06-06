# Generated by Django 5.1.4 on 2025-05-27 07:38

import datetime
import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailVerifyCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(help_text='验证码', max_length=10, null=True, verbose_name='验证码')),
                ('email', models.EmailField(help_text='邮箱', max_length=100, null=True, unique=True, verbose_name='邮箱')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, help_text='添加时间', verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '邮箱验证码',
                'verbose_name_plural': '邮箱验证码',
            },
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='权限名称', max_length=30, null=True, verbose_name='权限名称')),
                ('method', models.CharField(help_text='方法类型', max_length=30, null=True, verbose_name='方法类型')),
                ('desc', models.CharField(help_text='描述', max_length=300, null=True, verbose_name='描述')),
            ],
            options={
                'verbose_name': '权限',
                'verbose_name_plural': '权限',
            },
        ),
        migrations.CreateModel(
            name='SmsVerifyCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(help_text='验证码', max_length=10, null=True, verbose_name='验证码')),
                ('mobile', models.CharField(help_text='手机', max_length=11, null=True, verbose_name='手机')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, help_text='添加时间', verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '短信验证码',
                'verbose_name_plural': '短信验证码',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='角色名称', max_length=30, null=True, verbose_name='角色名称')),
                ('desc', models.CharField(help_text='描述', max_length=300, null=True, verbose_name='描述')),
                ('permission', models.ManyToManyField(help_text='权限', to='user.permission', verbose_name='权限')),
            ],
            options={
                'verbose_name': '角色',
                'verbose_name_plural': '角色',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(blank=True, help_text='姓名', max_length=30, null=True, unique=True, verbose_name='姓名')),
                ('avatar', models.CharField(default='https://m.imooc.com/static/wap/static/common/img/logo-small@2x.png', help_text='用户头像', max_length=200, verbose_name='用户头像')),
                ('birthday', models.DateField(blank=True, help_text='生日', null=True, verbose_name='生日')),
                ('address', models.CharField(help_text='家庭地址', max_length=50, null=True, verbose_name='家庭地址')),
                ('mobile', models.CharField(help_text='手机', max_length=11, verbose_name='手机')),
                ('gender', models.CharField(choices=[('male', '男'), ('female', '女')], default='female', help_text='性别', max_length=6, verbose_name='性别')),
                ('email', models.CharField(blank=True, help_text='邮箱', max_length=100, null=True, verbose_name='邮箱')),
                ('add_time', models.DateField(default=datetime.date.today, help_text='添加时间', verbose_name='添加时间')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('role', models.ManyToManyField(help_text='角色', to='user.role', verbose_name='角色')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Router',
            fields=[
                ('router_id', models.IntegerField(default=0, help_text='路由id', primary_key=True, serialize=False, verbose_name='路由id')),
                ('path', models.CharField(help_text='路径', max_length=50, null=True, verbose_name='路径')),
                ('component', models.CharField(help_text='组件名称', max_length=50, null=True, verbose_name='组件名称')),
                ('redirect', models.CharField(help_text='重定向', max_length=30, null=True, verbose_name='重定向')),
                ('hidden', models.BooleanField(default=False, help_text='是否隐藏', verbose_name='是否隐藏')),
                ('name', models.CharField(help_text='路由名', max_length=30, null=True, verbose_name='路由名')),
                ('title', models.CharField(help_text='路由标题', max_length=30, null=True, verbose_name='路由标题')),
                ('icon', models.CharField(help_text='图标', max_length=50, null=True, verbose_name='图标')),
                ('sub_router', models.ForeignKey(blank=True, help_text='上级路由', null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.router', verbose_name='上级路由')),
            ],
            options={
                'verbose_name': '路由',
                'verbose_name_plural': '路由',
            },
        ),
        migrations.AddField(
            model_name='permission',
            name='router',
            field=models.ForeignKey(help_text='权限', null=True, on_delete=django.db.models.deletion.CASCADE, to='user.router', verbose_name='权限'),
        ),
    ]
