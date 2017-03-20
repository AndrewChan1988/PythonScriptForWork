import os
import sys


def full_ota_package():
    pass


def diff_ota_package():
    global lower_zip_file
    global higher_zip_file


if __name__ == '__main__':
    android_home_dir = "~/MTK/S31/S31_Int/mydroid/"
    ota_from_target_files = android_home_dir + "build/tools/releasetools/ota_from_target_files"
    lower_zip_file = sys.argv[1]
    higher_zip_file = sys.argv[2]
    ota_type = sys.argv[3]

    if not os.path.exists(ota_from_target_files):
        print("不存在制作脚本，请检查环境是否正确!!!!!")
        sys.exit(1)

    if ota_type == "full":
        full_ota_package()
    else:
        diff_ota_package()