# coding=utf-8

import sys
import datetime
import os
import shutil


def copy_so():
    src = so_copy_path + "\\" + project_name + ".so"
    dst = so_release_path + "\\" + baseline + "\\" + product_name + ".so"
    if not os.path.exists(src):
        print("未上传so文件，请上传so文件")
        return 1
    shutil.copy(src, dst)
    return 0


if __name__ == '__main__':
    product_name = sys.argv[1]
    project_name = sys.argv[2]

    so_copy_path = "D:\\D:\SO_RELEASE"
    so_release_path = "\\\\10.250.115.51\\APK_Release_Version\\03-product\\{0}\\{1}".format(product_name, project_name)

    baseline = datetime.datetime.now().strftime("%Y.%m.%d_%H.%M")

    exit_code = copy_so()

    if exit_code == 1:
        print("so发布失败！！！")
        sys.exit(1)

    print("SO发布成功，发布地址为：{0}".format(so_release_path + "\\" + baseline))



