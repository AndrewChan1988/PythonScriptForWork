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


def release_apk():
    apks_name = os.listdir("D:\\APK_FAST_RELEASE\\APK")
    for apk in apks_name:
        src = "D:\\APK_FAST_RELEASE\\APK\\{0}".format(apk)
        dst = apk_release_path + "\\" + apk + "\\" + baseline
        if not os.path.exists(apk_release_path + "\\" + apk):
            os.makedirs(apk_release_path + "\\" + apk)
        shutil.copytree(src, dst)

if __name__ == '__main__':
    product_name = sys.argv[1]

    zip_path = "D:\\APK_FAST_RELEASE\\APK.zip"
    apk_release_path = "\\\\10.250.115.51\\APK_Release_Version\\03-product\\{0}".format(product_name)

    baseline = datetime.datetime.now().strftime("%Y.%m.%d_%H.%M")

    if not os.path.exists(zip_path):
        print("未上传包含所有APK的zip压缩包，请上传！！")
        sys.exit(1)

    # upzip APK.zip
    os.makedirs("D:\\APK_FAST_RELEASE\\APK")
    unzip_cmd = "D:\\WinRAR\\WinRAR.exe x D:\\APK_FAST_RELEASE\\APK.zip D:\\APK_FAST_RELEASE\\APK"
    do_command(unzip_cmd, False)

    release_apk()

    shutil.rmtree("D:\\APK_FAST_RELEASE\\APK")

