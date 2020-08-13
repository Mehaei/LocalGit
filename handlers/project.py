# -*- coding: utf-8 -*-
# @Author: Mehaei
# @Date:   2020-08-06 19:33:35
# @Last Modified by:   Mehaei
# @Last Modified time: 2020-08-13 17:02:07

import os
import tornado.web
from project.config import WORKDIR, GIT_PROJECT_DIR
from helper.tools import excute_cmd_get_result


class ProjectHandler(tornado.web.RequestHandler):
    """
     config work dir
    """
    def clean(self, strr):
        if "无文件要提交，干净的工作区" in strr:
            return ""
        else:
            # return [st.strip("*| |\n") for st in strr.split("\n") if st]
            return strr.replace("\t", "&nbsp"*4).replace("\n", "<br>")

    def get(self, git_dir):
        project_info = {}
        cmds = {
            "GitBranch": ["git", "branch"],
            "GitStatus": ["git", "status"]
        }
        for cmd_name, cmd in cmds.items():
            os.chdir("%s/%s" % (GIT_PROJECT_DIR, git_dir))
            # project_info[cmd_name] = excute_cmd_get_result(cmd, clean=self.clean)
            project_info[cmd_name] = excute_cmd_get_result(cmd)

        os.chdir(WORKDIR)

        self.render('project_info.html', project_info=project_info)

    def post(self, *args, **kwargs):
        print(self.body)
        self.write({'work_dir': '/Users/msw/works/platform/post'})
