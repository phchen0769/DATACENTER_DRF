# datacenter_drf
## 目录
1. logs 目录为日志文件以及uwsgi和nginx运行时产生的临时文件。
2. supervisor.conf 为supervisord工作时的配置文件
3. uwsgi.ini 为uwsgi的配置文件
4. repositories 为alpine国内源文件
5 . requients.txt为项目需要安装的依赖包

## 启动步骤

### 1. 运行postgre数据库
```bash
docker run -d --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=123456 -v /Volumes/myDriver/github/db/postgresql:/var/lib/postgresql/data postgres:latest
```
### 2. 创建数据库
1. 创建数据库 Postgres
2. 数据库名：sina_finance
3. 所有者：postgres
4. 模版：postgres
5. 表空间： pg_default


### 3. 生成数据表
1. python manage.py  makemigrations
2. python manage.py  migrate

* 注意：数据库创建表格，请使用全小写

### 4. 导入项目数据
DB_tools中的工具使用，请在项目根目录中运行:

1.DB_tools/sys_import.py

2.DB_tools/data_import.py

## 5. 运行
`F5`

或

`python manage.py runserver`

Your are done!

