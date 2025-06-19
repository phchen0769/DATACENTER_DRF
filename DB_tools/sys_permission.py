#!/usr/bin/env python
# encoding: utf-8


permission_datas = [
    # 获取个人用户信息
    {
        "name": "userinfo-detail",
        "method": ["GET", "DELETE", "PUT", "PATCH", "OPTIONS"],
        "router_id": "",
        "desc": "获取个人用户信息",
    },
    {
        "name": "userinfo-list",
        "method": ["GET", "POST"],
        "router_id": "",
        "desc": "获取个人用户信息",
    },
    # 用户管理权限
    {
        "name": "users-list",
        "method": ["GET", "POST"],
        "router_id": 2001,
        "desc": "用户管理权限",
    },
    {
        "name": "users-detail",
        "method": ["GET", "DELETE", "PUT", "PATCH", "OPTIONS"],
        "router_id": 2002,
        "desc": "用户管理权限",
    },
    # 角色管理数据
    {
        "name": "roles-list",
        "method": ["GET", "POST"],
        "router_id": 2004,
        "desc": "角色管理权限",
    },
    {
        "name": "roles-detail",
        "method": ["GET", "DELETE", "PUT", "PATCH", "OPTIONS"],
        "router_id": 2004,
        "desc": "角色管理权限",
    },
    # 权限管理数据
    {
        "name": "permissions-list",
        "method": ["GET", "POST"],
        "router_id": 2005,
        "desc": "权限管理权限",
    },
    {
        "name": "permissions-detail",
        "method": ["GET", "DELETE", "PUT", "PATCH", "OPTIONS"],
        "router_id": 2005,
        "desc": "权限管理权限",
    },
    # 业务
    {
        "name": "articles-list",
        "method": ["GET"],
        "router_id": 3001,
        "desc": "文章列表",
    },
    {
        "name": "articles-detail",
        "method": ["GET"],
        "router_id": 3002,
        "desc": "文章详情",
    },
    {
        "name": "articles-list",
        "method": ["POST"],
        "router_id": 3003,
        "desc": "创建文章",
    },
    {
        "name": "articles-detail",
        "method": ["PATCH"],
        "router_id": 3004,
        "desc": "更新文章",
    },
    {
        "name": "articles-detail",
        "method": ["DELETE"],
        "router_id": 3001,
        "desc": "删除文章",
    },
    {
        "name": "chapters-list",
        "method": ["GET", "POST"],
        "router_id": 3003,
        "desc": "章节管理权限",
    },
    {
        "name": "chapters-detail",
        "method": ["GET", "DELETE", "PUT", "PATCH", "OPTIONS"],
        "router_id": 3003,
        "desc": "章节管理权限",
    },
    {
        "name": "features-list",
        "method": ["GET", "POST"],
        "router_id": 3003,
        "desc": "功能管理权限",
    },
    {
        "name": "features-detail",
        "method": ["GET", "DELETE", "PUT", "PATCH", "OPTIONS"],
        "router_id": 3003,
        "desc": "功能管理权限",
    },
    {
        "name": "answers-list",
        "method": ["GET", "POST"],
        "router_id": "",
        "desc": "答案管理权限",
    },
    {
        "name": "answers-detail",
        "method": ["GET", "DELETE", "PUT", "PATCH", "OPTIONS"],
        "router_id": "",
        "desc": "答案管理权限",
    },
    {
        "name": "questions-list",
        "method": ["GET", "POST"],
        "router_id": "",
        "desc": "题目管理权限",
    },
    {
        "name": "questions-detail",
        "method": ["GET", "DELETE", "PUT", "PATCH", "OPTIONS"],
        "router_id": "",
        "desc": "题目管理权限",
    },
    {
        "name": "papers-list",
        "method": ["GET", "POST"],
        "router_id": "",
        "desc": "试卷管理权限",
    },
    {
        "name": "papers-detail",
        "method": ["GET", "DELETE", "PUT", "PATCH", "OPTIONS"],
        "router_id": "",
        "desc": "试卷管理权限",
    },
    {
        "name": "dividends-list",
        "method": ["GET", "POST"],
        "router_id": "",
        "desc": "分红管理权限",
    },
    {
        "name": "dividends-detail",
        "method": ["GET", "DELETE", "PUT", "PATCH", "OPTIONS"],
        "router_id": "",
        "desc": "分红管理权限",
    },
    {
        "name": "sms-list",
        "method": ["GET", "POST"],
        "router_id": "",
        "desc": "短信管理权限",
    },
    {
        "name": "sms-detail",
        "method": ["GET", "DELETE", "PUT", "PATCH", "OPTIONS"],
        "router_id": "",
        "desc": "短信管理权限",
    },
    {
        "name": "email-list",
        "method": ["GET", "POST"],
        "router_id": "",
        "desc": "邮箱管理权限",
    },
    {
        "name": "email-detail",
        "method": ["GET", "DELETE", "PUT", "PATCH", "OPTIONS"],
        "router_id": "",
        "desc": "邮箱管理权限",
    },
    # 路由管理
    {
        "name": "routers-list",
        "method": ["GET", "POST"],
        "router_id": "",
        "desc": "路由管理权限",
    },
    {
        "name": "routers-detail",
        "method": ["GET", "DELETE", "PUT", "PATCH", "OPTIONS"],
        "router_id": "",
        "desc": "路由管理权限",
    },
    {
        "name": "api-root",
        "method": ["GET", "OPTIONS"],
        "router_id": "",
        "desc": "api页面访问权限",
    },
    {
        "name": "docs-index",
        "method": ["GET", "OPTIONS"],
        "router_id": "",
        "desc": "在线文档访问权限",
    },
]
