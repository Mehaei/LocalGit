# -*- coding: utf-8 -*-
# @Author: Mehaei
# @Date:   2020-08-06 17:16:10
# @Last Modified by:   Mehaei
# @Last Modified time: 2020-08-13 16:45:02

import os
import sys
import tornado.ioloop   #开启循环，让服务一直等待请求的到来
import tornado.web      #web服务基本功能都封装在此模块中
import tornado.options  #从命令行中读取设置
from tornado.options import define, options  #导入包

from handlers import config, auth, execute, main, project
from project.config import WORKDIR
sys.path.append(WORKDIR)

define('port', default='12345', help='Listening port', type=int) #定义如何接受传进来的东西


class Application(tornado.web.Application):  #引入Application类，重写方法，这样做的好处在于可以自定义，添加另一些功能
    def __init__(self):
        handlers = [
            (r'/project_list', main.IndexHandler),
            (r'/', config.ConfigHandler),
            (r'/explore', main.ExploreHandler),
            (r'/post/(?P<post_id>[0-9]+)', main.PostHandler), #命名组写法,使用关键字，路由与handler方法不一定顺序一致
            (r'/project/(.*)', project.ProjectHandler), #命名组写法,使用关键字，路由与handler方法不一定顺序一致
            (r'/upload', main.UploadHandler),
            (r'/login', auth.LoginHandler),
            (r'/logout', auth.LogoutHandler),
            (r'/register', auth.RegisterHandler),
            (r'/config', config.ConfigHandler),
        ]
        settings = dict(
            debug=True, #调试模式，修改后自动重启服务，不需要自动重启，生产情况下切勿开启，安全性
            # template_path='templates', #模板文件目录,想要Tornado能够正确的找到html文件，需要在 Application 中指定文件的位置
            # static_path='static',  #静态文件目录,可用于用于访问js,css,图片之类的添加此配置之后，tornado就能自己找到静态文件
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            login_url='/', #没有登录则跳转至此
            cookie_secret='1q2w3e4r',  # 加密cookie的字符串
            # pycket={  #固定写法packet，用于保存用户登录信息
            #     'engine': 'redis',
            #     'storage': {
            #         'host': 'localhost',
            #         'port': 6379,
            #         'db_sessions': 5,
            #         'db_notifications': 11,
            #         'max_connections': 2 ** 33,
            #     },
            #     'cookie': {
            #         'expires_days': 38,
            #         'max_age': 100
            #     }
            # }
        )

        super(Application, self).__init__(handlers, **settings) #用super方法将父类的init方法重新执行一遍，然后将handlers和settings传进去，完成初始化


app = Application() #实例化


if __name__ == '__main__':   #当.py文件被直接运行时，代码块将被运行；当.py文件以模块形式被导入时，代码块不被运行。
    try:
        tornado.options.parse_command_line()
        app.listen(options.port)  ##如果一个与define语句中同名的设置在命令行中被给出，那么它将成为全局的options的一个属性 即 options.port 相当于define的url的port
        print("Server start on port {}".format(str(options.port)))  #提示服务启动占用端口
        tornado.ioloop.IOLoop.current().start()   #执行ioloop
    except KeyboardInterrupt:
        pass
