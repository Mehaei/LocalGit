# -*- coding: utf-8 -*-
# @Author: Mehaei
# @Date:   2020-08-06 17:17:59
# @Last Modified by:   Mehaei
# @Last Modified time: 2020-08-13 18:47:39

import tornado.web
import os
import re
from pycket.session import SessionMixin
from project.config import WORKDIR, GIT_PROJECT_DIR
from helper.tools import excute_cmd_get_result
# from utils import photo

class AuthBaseHandler(tornado.web.RequestHandler,SessionMixin):
    def get_current_user(self): #重写get_current_user()方法
        return self.session.get('user_info', None) #session是一种会话状态，跟数据库的session可能不一样

#添加装饰器,装饰需要验证的请求
# class IndexHandler(AuthBaseHandler):
class IndexHandler(tornado.web.RequestHandler):
    """
    """
    # @tornado.web.authenticated   #@tornado.web.authenticated装饰器包裹get方法时，表示这个方法只有在用户合法时才会调用，authenticated装饰器会调用get_current_user()方法获取current_user的值，若值为False，则重定向到登录url装饰器判断有没有登录，如果没有则跳转到配置的路由下去，但是要在app.py里面设置login_url
    def get(self, *args, **kwargs):
        show_file_list = []

        search_name = self.get_argument('search_name', None)
        for file_name in os.listdir(GIT_PROJECT_DIR):
            if os.path.isdir("%s/%s" % (GIT_PROJECT_DIR, file_name)):
                if search_name:
                    if re.search(search_name, file_name):
                        show_file_list.append(file_name)
                    else:
                        continue
                else:
                    show_file_list.append(file_name)

        # self.render('index.html')
        work_list = self.get_branch(show_file_list)
        self.render('project_list.html', work_list=work_list)

    def get_branch(self, work_list):
        new_work_list = []

        cmd = ["git", "branch"]
        for wdir in work_list:
            os.chdir("%s/%s" % (GIT_PROJECT_DIR, wdir))
            wdir_info = (wdir, excute_cmd_get_result(cmd, rgx=r"\*.+\n", clean=self.replace_branch, error_return="isn't git project"))
            new_work_list.append(wdir_info)

        os.chdir(WORKDIR)
        return new_work_list

    def replace_branch(self, strr):
        return strr.strip("*| |\n")


class ExploreHandler(AuthBaseHandler):
    """
    Explore page,photo of other users 发现页-----发现或最近上传的图片页面
    """
    @tornado.web.authenticated
    def get(self,*args,**kwargs):
        # image_urls = get_images("./static/uploads")  #打开指定路径下的文件，或者static/uploads
        os.chdir('static')  # 用于改变当前工作目录到指定的路径
        image_urls = photo.get_images("uploads/thumbs")
        os.chdir("..")
        self.render('explore.html',image_urls=image_urls)

class PostHandler(AuthBaseHandler):
    """
    Single photo page and maybe  单个图片详情页面
    """
    @tornado.web.authenticated
    def get(self,post_id):
        print(post_id)
        self.render('post.html',post_id = post_id)   #根据正则输入的内容，接收到，打开相应的图片


class UploadHandler(AuthBaseHandler):  #上传文件
    @tornado.web.authenticated
    def get(self,*args,**kwargs):
        self.render('upload.html')

    def post(self,*args,**kwargs):
        file_imgs = self.request.files.get('newImg',None)  #获取上传文件数据，返回文件列表

        for file_img in file_imgs: #可能同一个上传的文件会有多个文件，所以要用for循环去迭代它
            # filename 文件的实际名字，body 文件的数据实体；content_type 文件的类型。 这三个对象属性可以像字典一样支持关键字索引
            save_to = 'static/uploads/{}'.format(file_img['filename'])
            #以二进制格式打开一个文件只用于写入。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。一般用于非文本文件如图片等。
            with open(save_to,'wb') as f: #二进制
                f.write(file_img['body'])
            photo.make_thumb(save_to) #同时生成缩略图

        self.redirect('/explore')
