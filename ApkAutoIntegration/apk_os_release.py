import shutil
import sys
import os
import subprocess
import datetime


# execute command
def do_command(cmd, need_result=True):
    print('执行命令: ', cmd)
    out = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    if need_result:
        out.wait()
        result = out.communicate()[0].decode().strip()
        print(result)
        return result, out.returncode
    else:
        while out.poll() is None:
            s = out.stdout.readline()
            if s != b'':
                if "ant" in cmd:
                    print(s.decode('cp936').strip())
                else:
                    print(s.decode('utf-8').strip())
        return out.returncode


if __name__ == '__main__':
    product_name = sys.argv[1]
    release_path = "\\\\10.250.115.51\\APK_Release_Version\\04-talpa\\{0}".format(product_name)
    workspace = "D:\\apk_release\\talpa"
    zip_file_path = workspace + "\\OS.zip"

    if not os.path.exists(zip_file_path):
        print("请检查是否上传了压缩文件包")
        sys.exit(1)

    if not os.path.exists(workspace + "\\release_note.xlsx"):
        print("请检查是否上传了修改发布文件")
        sys.exit(2)

    baseline = datetime.datetime.now().strftime("%Y.%m.%d_%H.%M")

    if not os.path.exists(release_path + "\\" + baseline):
        os.makedirs(release_path + "\\" + baseline)

    unzip_cmd = "D:\\WinRAR\\WinRAR.exe -y x {0} {1}".format(zip_file_path, release_path + "\\" + baseline)
    exit_code = do_command(unzip_cmd, False)
    if exit_code == 0:
        shutil.copy(workspace + "\\release_note.xlsx", release_path + "\\" + baseline + "\\release_note.xlsx")
        print("OS APK发布成功")
    else:
        print("OS APK发布失败")
        shutil.rmtree(release_path + "\\" + baseline)
