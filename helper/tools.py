# -*- coding: utf-8 -*-
# @Author: Mehaei
# @Date:   2020-08-07 17:40:10
# @Last Modified by:   Mehaei
# @Last Modified time: 2020-08-12 17:23:48
import re
import os
import subprocess
from project.config import WORKDIR


def excute_cmd_get_result(cmd, rgx=None, clean=None, retry=2, error_return=None):
    while retry:
        try:
            stdout = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            eresult = stdout.decode("utf8")
            break
        except:
            print(cmd, "execute failed")
            if retry <= 1:
                if error_return:
                    return error_return
                return ""
        finally:
            retry -= 1
    if rgx:
        result = re.findall(rgx, eresult)
        if result:
            if clean:
                return clean(result[0])
            else:
                return result[0]
    else:
        if clean:
            return clean(eresult)

    return eresult