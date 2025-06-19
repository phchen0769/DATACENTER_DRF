#!/usr/bin/env python
# encoding: utf-8


permission_datas = [
    # Get personal user information
    {
        "name": "userinfo-detail",
        "method": ["GET", "DELETE", "PUT", "PATCH", "OPTIONS"],
        "router_id": "",
        "desc": "Get personal user information",
    },
    {
        "name": "userinfo-list",
        "method": ["GET", "POST"],
        "router_id": "",
        "desc": "Get personal user information",
    },
    # User management permissions
    {
        "name": "users-list",
        "method": ["GET", "POST"],
        "router_id": 2001,
        "desc": "User management permissions",
    },
    {
        "name": "users-detail",
        "method": ["GET", "DELETE", "PUT", "PATCH", "OPTIONS"],
        "router_id": 2002,
        "desc": "User management permissions",
    },
    # Role management data
    {
        "name": "roles-list",
        "method": ["GET", "POST"],
        "router_id": 2004,
        "desc": "Role management permissions",
    },
    {
        "name": "roles-detail",
        "method": ["GET", "DELETE", "PUT", "PATCH", "OPTIONS"],
        "router_id": 2004,
        "desc": "Role management permissions",
    },
    # Permission management data
    {
        "name": "permissions-list",
        "method": ["GET", "POST"],
        "router_id": 2005,
        "desc": "Permission management permissions",
    },
    {
        "name": "permissions-detail",
        "method": ["GET", "DELETE", "PUT", "PATCH", "OPTIONS"],
        "router_id": 2005,
        "desc": "Permission management permissions",
    },
    # Business
    {
        "name": "articles-list",
        "method": ["GET"],
        "router_id": 3001,
        "desc": "Article list",
    },
    {
        "name": "articles-detail",
        "method": ["GET"],
        "router_id": 3002,
        "desc": "Article details",
    },
    {
        "name": "articles-list",
        "method": ["POST"],
        "router_id": 3003,
        "desc": "Create article",
    },
    {
        "name": "articles-detail",
        "method": ["PATCH"],
        "router_id": 3004,
        "desc": "Update article",
    },
    {
        "name": "articles-detail",
        "method": ["DELETE"],
        "router_id": 3001,
        "desc": "Delete article",
    },
    {
        "name": "chapters-list",
        "method": ["GET", "POST"],
        "router_id": 3003,
        "desc": "Chapter management permissions",
    },
    {
        "name": "chapters-detail",
        "method": ["GET", "DELETE", "PUT", "PATCH", "OPTIONS"],
        "router_id": 3003,
        "desc": "Chapter management permissions",
    },
    {
        "name": "features-list",
        "method": ["GET", "POST"],
        "router_id": 3003,
        "desc": "Feature management permissions",
    },
    {
        "name": "features-detail",
        "method": ["GET", "DELETE", "PUT", "PATCH", "OPTIONS"],
        "router_id": 3003,
        "desc": "Feature management permissions",
    },
    {
        "name": "answers-list",
        "method": ["GET", "POST"],
        "router_id": "",
        "desc": "Answer management permissions",
    },
    {
        "name": "answers-detail",
        "method": ["GET", "DELETE", "PUT", "PATCH", "OPTIONS"],
        "router_id": "",
        "desc": "Answer management permissions",
    },
    {
        "name": "questions-list",
        "method": ["GET", "POST"],
        "router_id": "",
        "desc": "Question management permissions",
    },
    {
        "name": "questions-detail",
        "method": ["GET", "DELETE", "PUT", "PATCH", "OPTIONS"],
        "router_id": "",
        "desc": "Question management permissions",
    },
    {
        "name": "papers-list",
        "method": ["GET", "POST"],
        "router_id": "",
        "desc": "Paper management permissions",
    },
    {
        "name": "papers-detail",
        "method": ["GET", "DELETE", "PUT", "PATCH", "OPTIONS"],
        "router_id": "",
        "desc": "Paper management permissions",
    },
    {
        "name": "dividends-list",
        "method": ["GET", "POST"],
        "router_id": "",
        "desc": "dividends management permissions",
    },
    {
        "name": "dividends-detail",
        "method": ["GET", "DELETE", "PUT", "PATCH", "OPTIONS"],
        "router_id": "",
        "desc": "dividends management permissions",
    },
    {
        "name": "sms-list",
        "method": ["GET", "POST"],
        "router_id": "",
        "desc": "SMS management permissions",
    },
    {
        "name": "sms-detail",
        "method": ["GET", "DELETE", "PUT", "PATCH", "OPTIONS"],
        "router_id": "",
        "desc": "SMS management permissions",
    },
    {
        "name": "email-list",
        "method": ["GET", "POST"],
        "router_id": "",
        "desc": "Email management permissions",
    },
    {
        "name": "email-detail",
        "method": ["GET", "DELETE", "PUT", "PATCH", "OPTIONS"],
        "router_id": "",
        "desc": "Email management permissions",
    },
    # Router management
    {
        "name": "routers-list",
        "method": ["GET", "POST"],
        "router_id": "",
        "desc": "Router management permissions",
    },
    {
        "name": "routers-detail",
        "method": ["GET", "DELETE", "PUT", "PATCH", "OPTIONS"],
        "router_id": "",
        "desc": "Router management permissions",
    },
    {
        "name": "api-root",
        "method": ["GET", "OPTIONS"],
        "router_id": "",
        "desc": "API page access permissions",
    },
    {
        "name": "docs-index",
        "method": ["GET", "OPTIONS"],
        "router_id": "",
        "desc": "Online documentation access permissions",
    },
]
