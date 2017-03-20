import os
import sys
import subprocess
import shutil


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


def sign_apk():
    dir_names = os.listdir(sign_dir)
    sign_type = ""
    apk_name_list = []
    for dir_name in dir_names:
        if os.path.isdir(sign_dir + "\\" + dir_name) and "copy_files" not in dir_name and "incodefile" not in dir_name:
            with open(sign_dir + "\\" + dir_name + "\\Android.mk", 'r') as f:
                lines = f.readlines()
            for line in lines:
                if "LOCAL_CERTIFICATE" in line:
                    sign_type = line.split(":=")[1].strip()
                    break
            for file_list in os.listdir(sign_dir + "\\" + dir_name):
                if ".apk" in file_list:
                    apk_name_list.append(file_list)
            for apk_name in apk_name_list:
                sign_cmd = "call D:\\APK_Sign\\apk_sign_spreadtrum.bat {0} {1} {2}".format(sign_type, sign_dir + "\\" + dir_name + "\\" + apk_name, sign_dir + "\\" + dir_name + "\\" + apk_name.strip(".apk") + "_Signed.apk")
                do_command(sign_cmd)
                os.remove(sign_dir + "\\" + dir_name + "\\" + apk_name)
                os.rename(sign_dir + "\\" + dir_name + "\\" + apk_name.strip(".apk") + "_Signed.apk", sign_dir + "\\" + dir_name + "\\" + apk_name)
            apk_name_list = []


def zip_apk():
    dir_names = os.listdir(sign_dir)
    zip_cmd = "D:\\WinRAR\\WinRAR.exe a D:\\APK_Sign\\{1}\\{0}_Signed.zip ".format(unsigned_zip_name.split(".zip")[0], product_name)
    for dir_name in dir_names:
        zip_cmd = zip_cmd + " " + dir_name
    os.chdir(sign_dir)
    do_command(zip_cmd)
    print("打包成功！！！！！")

if __name__ == '__main__':
    unsigned_zip_name = sys.argv[1]
    product_name = sys.argv[2]
    unsigned_zip_dir = "\\\\10.250.119.10\\osteam\\simg2img\\out_osapp_zip_dir\\{0}".format(product_name)
    sign_dir = "D:\\APK_Sign\\sign\\{0}".format(product_name)

    shutil.rmtree(sign_dir)

    if not os.path.exists(sign_dir):
        os.makedirs(sign_dir)

    if not os.path.exists("D:\\APK_Sign\\{0}".format(product_name)):
        os.makedirs("D:\\APK_Sign\\{0}".format(product_name))

    # 获取zip文件并且解压
    unzip_cmd = "D:\\WinRAR\\WinRAR.exe -y x {0}\\{1} {2}".format(unsigned_zip_dir, unsigned_zip_name, sign_dir)
    do_command(unzip_cmd)

    # 对APK进行签名
    sign_apk()

    # 重新打包已经签名的APK文件
    zip_apk()

    src = "D:\\APK_Sign\\{1}\\{0}_Signed.zip".format(unsigned_zip_name.split(".zip")[0], product_name)
    if os.path.exists(src):
        print("拷贝到原路径！！！")
        shutil.copy(src, unsigned_zip_dir)
        os.remove(src)
