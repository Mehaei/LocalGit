# -*- coding: utf-8 -*-
# @Author: Mehaei
# @Date:   2020-08-06 17:14:53
# @Last Modified by:   Mehaei
# @Last Modified time: 2020-08-13 18:16:21
import json
import tornado.web
from project.config import WORKDIR, GIT_PROJECT_CONFIG_FILE_NAME
from project.field_name import UserConfig

class ConfigHandler(tornado.web.RequestHandler):
    """
     config work dir
    """
    def get(self, *args, **kwargs):
        project_root_config = json.load(open(GIT_PROJECT_CONFIG_FILE_NAME, "r+"))
        self.render('index_config.html', config=project_root_config)

    def post(self, *args, **kwargs):

        project_root_config = {
            UserConfig.GitProjectDir: self.get_body_argument('GitProjectDir'),
            UserConfig.RootPass: self.get_body_argument('RootPass')
        }
        json.dump(project_root_config, open(GIT_PROJECT_CONFIG_FILE_NAME, "w+"))
        # self.write(project_root_config)
        # self.render('project_list.html', work_list=work_list)
        self.redirect("/project_list")
