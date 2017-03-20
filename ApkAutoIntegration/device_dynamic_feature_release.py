import os
import sys
import shutil
import datetime


if __name__ == '__main__':
    product_name = sys.argv[1]
    device_dynamic_feature_file = "D:\\apk_release\\device_dynamic_feature\\device_dynamic_feature"
    device_dynamic_feature_delete_file = "D:\\apk_release\\device_dynamic_feature\\device_dynamic_feature_delete"
    device_dynamic_feature_release_path = "\\\\10.250.115.51\\APK_Release_Version\\03-product\\{0}\\" \
                                          "device_dynamic_feature".format(product_name)

    if not os.path.exists(device_dynamic_feature_file):
        print("未上传device_dynamic_feature_file文件！！！")
        sys.exit(1)

    # if os.path.exists(device_dynamic_feature_delete_file):
    #    shutil.rmtree(device_dynamic_feature_delete_file)

    baseline = datetime.datetime.now().strftime("%Y.%m.%d_%H.%M")

    if not os.path.exists(device_dynamic_feature_release_path + "\\" + baseline):
        os.makedirs(device_dynamic_feature_release_path + "\\" + baseline)

    dst = device_dynamic_feature_release_path + "\\" + baseline + "\\device_dynamic_feature"
    shutil.copy(device_dynamic_feature_file, dst)

    shutil.move(device_dynamic_feature_file, device_dynamic_feature_delete_file + baseline)
