# coding=utf-8

import shutil
import os
import sys
import subprocess


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


# output the differences between this tag and the previous tag
def diff_between_tag(current_baseline):
    print("获取代码\n")
    release_dir = apk_release_dir_server + "\\" + branch
    if os.path.exists(release_dir):
        print("代码目录已经存在，直接更新代码!!\n")
        os.chdir(release_dir)
        do_command("git clean -xdf", False)
        do_command("git reset --hard", False)
        do_command("git pull", False)
    else:
        os.makedirs(release_dir)
        os.chdir(release_dir)
        checkout_cmd = "git clone ssh://10.250.115.12:29418/APK/{0}.git . -b {1}".format(project_name, branch)
        do_command(checkout_cmd, False)

    # tag_lists = do_command("git tag")[0].replace('\n', ' ').split()
    print("获取上一个版本的tag\n")
    baseline_list = os.listdir(apk_release_path)
    baseline_list.reverse()
    if not os.path.exists("{0}\\{1}".format(apk_release_path, current_baseline)):
        os.makedirs("{0}\\{1}".format(apk_release_path, current_baseline))
    if len(baseline_list) == 0:
        print("第一个版本，无需比较tag\n")
        return 1
    else:
        previous_baseline = baseline_list[0]
        diff_content = do_command("git log --pretty=oneline {0}...{1}".format(previous_baseline, current_baseline))[0]
        with open("{0}\\{1}\\diff.txt".format(apk_release_path, current_baseline), 'w', encoding='utf-8') as f:
            f.write(diff_content)
    return 0


def copy_to_server():
    apk_lists = os.listdir(apk_int_path + "\\" + baseline)
    is_resolution = False
    if resolution == "all":
        for apk in apk_lists:
            if "universal" in apk:
                is_resolution = True
        for apk in apk_lists:
            if is_resolution is True:
                if "universal" in apk and "release" in apk and "unsigned" in apk:
                    src = apk_int_path + "\\" + baseline + "\\" + apk
                    dst = apk_release_path + "\\" + baseline + "\\" + project_name + ".apk"
                    if not os.path.exists(src):
                        return 3
                    shutil.copy(src, dst)
                    with open("{0}\\{1}\\apk_info.txt".format(apk_release_path, baseline), 'a', encoding='utf-8') as f:
                        f.write("From: {0} \nTo: {1}".format(src, dst))
                    break
            else:
                if "{0}-unsigned".format(project_name) in apk:
                    src = apk_int_path + "\\" + baseline + "\\" + apk
                    dst = apk_release_path + "\\" + baseline + "\\" + project_name + ".apk"
                    if not os.path.exists(src):
                        return 3
                    shutil.copy(src, dst)
                    with open("{0}\\{1}\\apk_info.txt".format(apk_release_path, baseline), 'a', encoding='utf-8') as f:
                        f.write("From: {0} \nTo: {1}".format(src, dst))
                    break
                if project_name in apk and "unsigned" in apk and "release" in apk:
                    src = apk_int_path + "\\" + baseline + "\\" + apk
                    dst = apk_release_path + "\\" + baseline + "\\" + project_name + ".apk"
                    shutil.copy(src, dst)
                    with open("{0}\\{1}\\apk_info.txt".format(apk_release_path, baseline), 'a', encoding='utf-8') as f:
                        f.write("From: {0} \nTo: {1}".format(src, dst))
                    break
    else:
        for apk in apk_lists:
            if resolution in apk and "release" in apk and "unsigned" in apk:
                src = apk_int_path + "\\" + baseline + "\\" + apk
                dst = apk_release_path + "\\" + baseline + "\\" + project_name + ".apk"
                shutil.copy(src, dst)
                with open("{0}\\{1}\\apk_info.txt".format(apk_release_path, baseline), 'a', encoding='utf-8') as f:
                    f.write("From: {0} \nTo: {1}".format(src, dst))
                break
        return 3
    return 0


def output_info(info):
    with open("{0}\\{1}\\apk_info.txt".format(apk_release_path, baseline), 'w', encoding='utf-8') as f:
        f.write(info)


if __name__ == '__main__':
    # system_version = sys.argv[1]
    branch = sys.argv[1]
    baseline = sys.argv[2]
    resolution = sys.argv[3]
    product_name = sys.argv[4]
    project_name = sys.argv[5]

    apk_release_dir_server = "D:\\apk_release"
    apk_int_path = "\\\\10.250.115.52\\APK_Test_Version\\{0}\\int\\{1}".format(project_name, branch)
    # apk_release_path = "\\\\10.250.115.51\\APK_Release_Version\\PRODUCT_APK\\{0}\\{1}".format(product_name,
    # project_name)
    apk_release_path = "\\\\10.250.115.51\\APK_Release_Version\\03-product\\{0}\\{1}".format(product_name, project_name)

    content = '''APK名称：{0}
基线：{1}
分辨率：{2}
产品名称：{3}
分支：{4}\n
'''.format(project_name + ".apk", baseline, resolution, product_name, branch)

    if not os.path.exists(apk_release_path):
        print("尚未创建发布目录{0}，重新创建\n".format(apk_release_path))
        os.makedirs(apk_release_path)

    print("输出与上一个release版本的差异\n")
    if baseline == "new":
        int_baseline_list = os.listdir(apk_int_path)
        int_baseline_list.reverse()
        if int_baseline_list is None:
            print("{0}中没有任何目录！！！！\n".format(apk_int_path))
            sys.exit(3)
        baseline = int_baseline_list[0]
    else:
        if baseline not in os.listdir(apk_int_path):
            print("基线{0}在目录{1}下不存在\n".format(baseline, apk_int_path))
            sys.exit(1)

    if baseline in os.listdir(apk_release_path):
        print("基线{0}已经发布过\n".format(baseline, apk_release_path))
        sys.exit(2)

    diff_between_tag(baseline)

    print("输出该apk信息到文档中\n")
    output_info(content)

    print("将apk拷贝到51服务器上\n")
    exit_code = copy_to_server()

    if exit_code == 3:
        print("没有找到要发布的apk，请检查参数是否设置正确，如果没有进行多分辨率编译的项目要选择all\n")
        shutil.rmtree(apk_release_path + "\\" + baseline)
        sys.exit(3)

    print("APK发布成功！！！\n")
