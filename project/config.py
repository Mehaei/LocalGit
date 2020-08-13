# -*- coding: utf-8 -*-
# @Author: Mehaei
# @Date:   2020-08-06 17:44:40
# @Last Modified by:   Mehaei
# @Last Modified time: 2020-08-13 19:12:25

import os
import json
from project.field_name import UserConfig


WORKDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))

GIT_PROJECT_CONFIG_FILE_NAME = "%s/.%s" % (WORKDIR, "GitProjectConfig")
if not os.path.exists(GIT_PROJECT_CONFIG_FILE_NAME):
    # os.mkdir(GIT_PROJECT_CONFIG_FILE_NAME)

    project_root_config = {
        UserConfig.GitProjectDir: WORKDIR,
        UserConfig.RootPass: ""
    }
    json.dump(project_root_config, open(GIT_PROJECT_CONFIG_FILE_NAME, "w+"))

GIT_PROJECT_CONFIG = json.load(open(GIT_PROJECT_CONFIG_FILE_NAME, "r+"))

GIT_PROJECT_DIR = GIT_PROJECT_CONFIG.get(UserConfig.GitProjectDir, WORKDIR)

print("work dir===", WORKDIR)