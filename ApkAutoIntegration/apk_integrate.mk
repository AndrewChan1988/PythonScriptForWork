LOCAL_PATH := $(call my-dir)

# integrate so
########################################################
all_so := $(strip $(notdir $(shell find $(LOCAL_PATH)/lib/ -name *.so)))
$(warning =================all_so:====$(all_so)=============)
ifneq (,$(all_so))
    $(shell mkdir -p $(PRODUCT_OUT)/system/lib)
    $(shell cp -f $(LOCAL_PATH)/lib/*.so $(PRODUCT_OUT)/system/lib/)
endif
########################################################

# integrate conf
########################################################
all_conf := $(strip $(notdir $(shell find $(LOCAL_PATH)/conf/ -name *.conf)))
$(warning =================all_conf:====$(all_conf)=============)
ifneq (,$(all_conf))
    $(shell mkdir -p $(PRODUCT_OUT)/system/etc)
    $(shell cp -f $(LOCAL_PATH)/conf/*.conf $(PRODUCT_OUT)/system/etc/)
endif
########################################################

include $(CLEAR_VARS)
$(warning $(LOCAL_PATH)====)
define all-files
$(patsubst ./%,%, \
  $(shell cd $(LOCAL_PATH) ; \
    find $(1) -name "*.$(2)" \
  )
)
endef

define all-subdir-files
$(call all-files,.,$(1))
endef

# integrate apk
all_apks := $(shell echo $(notdir $(call all-subdir-files,apk)))
all_apks := $(filter-out SysStasl.apk,$(all_apks))
all_apks := $(filter-out DataTransferMaster.apk,$(all_apks))

$(warning ==================all_apks:=====$(all_apks)====================)

#apks re-signed by platform,will be dexpreopt.
platform_apks := $(shell ($(LOCAL_PATH)/getApkDetail.sh platform app $(LOCAL_PATH)))
platform_apks := $(filter $(all_apks),$(platform_apks))
$(warning ==========platform_apks:====$(platform_apks)==================================)

platform_priv_apks := $(shell ($(LOCAL_PATH)/getApkDetail.sh platform priv-app $(LOCAL_PATH)))
platform_priv_apks := $(filter $(all_apks),$(platform_priv_apks))
$(warning ==========platform_priv_apks:====$(platform_priv_apks)==================================)

platform_preset_apks := $(shell ($(LOCAL_PATH)/getApkDetail.sh platform presetapp $(LOCAL_PATH)))
platform_preset_apks := $(filter $(all_apks),$(platform_preset_apks))
$(warning ==========platform_preset_apks:====$(platform_preset_apks)==================================)

platform_vendor_apks := $(shell ($(LOCAL_PATH)/getApkDetail.sh platform vendor/operator/app $(LOCAL_PATH)))
platform_vendor_apks := $(filter $(all_apks),$(platform_vendor_apks))
$(warning ==========platform_vendor_apks:====$(platform_vendor_apks)==================================)

media_apks := $(shell ($(LOCAL_PATH)/getApkDetail.sh media app $(LOCAL_PATH)))
media_apks := $(filter $(all_apks),$(media_apks))
$(warning ==========media_apks:====$(media_apks)==================================)

media_priv_apks := $(shell ($(LOCAL_PATH)/getApkDetail.sh media priv-app $(LOCAL_PATH)))
media_priv_apks := $(filter $(all_apks),$(media_priv_apks))
$(warning ==========media_priv_apks:====$(media_priv_apks)==================================)

media_vendor_apks := $(shell ($(LOCAL_PATH)/getApkDetail.sh media vendor/operator/app $(LOCAL_PATH)))
media_vendor_apks := $(filter $(all_apks),$(media_vendor_apks))
$(warning ==========media_vendor_apks:====$(media_vendor_apks)==================================)

shared_apks := $(shell ($(LOCAL_PATH)/getApkDetail.sh shared app $(LOCAL_PATH)))
shared_apks := $(filter $(all_apks),$(shared_apks))
$(warning ==========shared_apks:====$(shared_apks)==================================)

shared_priv_apks := $(shell ($(LOCAL_PATH)/getApkDetail.sh shared priv-app $(LOCAL_PATH)))
shared_priv_apks := $(filter $(all_apks),$(shared_priv_apks))
$(warning ==========shared_priv_apks:====$(shared_priv_apks)==================================)

shared_vendor_apks := $(shell ($(LOCAL_PATH)/getApkDetail.sh shared vendor/operator/app $(LOCAL_PATH)))
shared_vendor_apks := $(filter $(all_apks),$(shared_vendor_apks))
$(warning ==========shared_vendor_apks:====$(shared_vendor_apks)==================================)

nosign_apks := $(shell ($(LOCAL_PATH)/getApkDetail.sh nosign app $(LOCAL_PATH)))
nosign_apks := $(filter $(all_apks),$(nosign_apks))
$(warning ==========nosign_apks:====$(nosign_apks)==================================)

nosign_priv_apks := $(shell ($(LOCAL_PATH)/getApkDetail.sh nosign priv-app $(LOCAL_PATH)))
nosign_priv_apks := $(filter $(all_apks),$(nosign_priv_apks))
$(warning ==========nosign_priv_apks:====$(nosign_priv_apks)==================================)

nosign_vendor_apks := $(shell ($(LOCAL_PATH)/getApkDetail.sh nosign vendor/operator/app $(LOCAL_PATH)))
nosign_vendor_apks := $(filter $(all_apks),$(nosign_vendor_apks))
$(warning ==========nosign_vendor_apks:====$(nosign_vendor_apks)==================================)

presetapp_apks := $(shell ($(LOCAL_PATH)/getApkDetail.sh nosign presetapp $(LOCAL_PATH)))
presetapp_apks := $(filter $(all_apks),$(presetapp_apks))
$(warning ==========presetapp_apks:====$(presetapp_apks)==================================)

test_apks := $(shell ($(LOCAL_PATH)/getApkDetail.sh testkey app $(LOCAL_PATH)))
test_apks := $(filter $(all_apks),$(test_apks))
$(warning ==========test_apks:====$(test_apks)==================================)

test_priv_apks := $(shell ($(LOCAL_PATH)/getApkDetail.sh testkey priv-app $(LOCAL_PATH)))
test_priv_apks := $(filter $(all_apks),$(test_priv_apks))
$(warning ==========test_priv_apks:====$(test_priv_apks)==================================)

test_preset_apks := $(shell ($(LOCAL_PATH)/getApkDetail.sh testkey presetapp $(LOCAL_PATH)))
test_preset_apks := $(filter $(all_apks),$(test_preset_apks))
$(warning ==========test_preset_apks:====$(test_preset_apks)==================================)

test_vendor_apks := $(shell ($(LOCAL_PATH)/getApkDetail.sh testkey vendor/operator/app $(LOCAL_PATH)))
test_vendor_apks := $(filter $(all_apks),$(test_vendor_apks))
$(warning ==========test_vendor_apks:====$(test_vendor_apks)==================================)

data_apks := $(shell ($(LOCAL_PATH)/getApkDetail.sh platform data-app $(LOCAL_PATH)))
data_apks := $(filter $(all_apks),$(data_apks))
$(warning ==========data_apks:====$(data_apks)==================================)

other_apks := $(filter-out $(platform_apks) \
                           $(media_apks) \
                           $(shared_apks) \
                           $(nosign_apks) \
                           $(nosign_priv_apks) \
                           $(platform_priv_apks) \
                           $(shared_priv_apks) \
                           $(media_priv_apks) \
                           $(presetapp_apks) \
                           $(test_apks) \
                           $(test_priv_apks) \
                           $(platform_preset_apks) \
                           $(test_preset_apks) \
                           $(data_apks) \
                           $(test_vendor_apks) \
                           $(platform_vendor_apks) \
                           $(media_vendor_apks) \
                           $(shared_vendor_apks) \
                           $(nosign_vendor_apks) \
                           SysStasl.apk \
                           DataTransferMaster.apk \
                           ,$(all_apks))


#ifneq (,$(strip $(other_apks)))
$(warning ==========other apks:====$(other_apks)==================================)

#    result = $(strip \
                         $(filter-out 3RD_APK,\
                                  $(foreach apk,$(other_apks),\
                                          $(if $(filter ERROR_APK ERROR_LOAD_APK,\
                                                          $(shell ($(LOCAL_PATH)/get_apkcerts.sh $(apk) $(LOCAL_PATH)/$(basename $(apk))))),\
                                               $(apk),\
                                               3RD_APK))))

#    ifneq ($(result),)
#        $(error ==========other_apks using google sign :===$(result)=====================)
#    endif
#endif

my_archs := arm arm64 x86 x86_64
my_src_arch := $(call get-prebuilt-src-arch, $(my_archs))

$(warning ====my_archs==$(my_archs)========)
$(warning ====my_src_arch==$(my_src_arch)========)

define get_lib
$(strip $(if $(filter-out arm64 x86_64,$(my_src_arch)), \
             both, \
             32))
endef

$(warning ============arch:$(call get_lib)================)
###############################################################
# integrate apks which are installed in system/app

define auto-prebuilt-apps
$(foreach t,$(1), \
  $(eval include $(CLEAR_VARS)) \
  $(eval LOCAL_MODULE := $(basename $(notdir $(t)))) \
  $(eval LOCAL_MODULE_TAGS := optional) \
  $(eval LOCAL_MODULE_CLASS := APPS) \
  $(eval LOCAL_BUILT_MODULE_STEM := package.apk) \
  $(eval LOCAL_MODULE_SUFFIX := $(COMMON_ANDROID_PACKAGE_SUFFIX)) \
  $(eval LOCAL_SRC_FILES := $(LOCAL_MODULE)/$(t)) \
  $(eval LOCAL_CERTIFICATE := $(2)) \
  $(eval LOCAL_MULTILIB := $(call get_lib)) \
  $(eval include $(BUILD_PREBUILT)) \
)
endef

define auto-prebuilt-apps-SysStasl
$(foreach t,$(1), \
  $(eval include $(CLEAR_VARS)) \
  $(eval LOCAL_MODULE := $(basename $(notdir $(t)))) \
  $(eval LOCAL_MODULE_TAGS := optional) \
  $(eval LOCAL_MODULE_CLASS := APPS) \
  $(eval LOCAL_DEX_PREOPT := false) \
  $(eval LOCAL_BUILT_MODULE_STEM := package.apk) \
  $(eval LOCAL_MODULE_SUFFIX := $(COMMON_ANDROID_PACKAGE_SUFFIX)) \
  $(eval LOCAL_SRC_FILES := $(LOCAL_MODULE)/$(t)) \
  $(eval LOCAL_CERTIFICATE := $(2)) \
  $(eval LOCAL_MULTILIB := $(call get_lib)) \
  $(eval include $(BUILD_PREBUILT)) \
)
endef

$(call auto-prebuilt-apps,$(platform_apks),platform)
$(call auto-prebuilt-apps,$(media_apks),media)
$(call auto-prebuilt-apps,$(shared_apks),shared)
$(call auto-prebuilt-apps,$(test_apks),testkey)
$(call auto-prebuilt-apps,$(nosign_apks),PRESIGNED)
$(call auto-prebuilt-apps-SysStasl,SysStasl.apk,platform)
$(call auto-prebuilt-apps-SysStasl,DataTransferMaster.apk,platform)
###############################################################

###############################################################
# integrate apks which are installed in system/priv-app

define auto-prebuilt-priv-apps
$(foreach t,$(1), \
  $(eval include $(CLEAR_VARS)) \
  $(eval LOCAL_MODULE := $(basename $(notdir $(t)))) \
  $(eval LOCAL_MODULE_TAGS := optional) \
  $(eval LOCAL_MODULE_CLASS := APPS) \
  $(eval LOCAL_BUILT_MODULE_STEM := package.apk) \
  $(eval LOCAL_MODULE_SUFFIX := $(COMMON_ANDROID_PACKAGE_SUFFIX)) \
  $(eval LOCAL_PRIVILEGED_MODULE := true) \
  $(eval LOCAL_SRC_FILES := $(LOCAL_MODULE)/$(t)) \
  $(eval LOCAL_CERTIFICATE := $(2)) \
  $(eval LOCAL_MULTILIB := $(call get_lib)) \
  $(eval include $(BUILD_PREBUILT)) \
)
endef

$(call auto-prebuilt-priv-apps,$(platform_priv_apks),platform)
$(call auto-prebuilt-priv-apps,$(media_priv_apks),media)
$(call auto-prebuilt-priv-apps,$(shared_priv_apks),shared)
$(call auto-prebuilt-priv-apps,$(test_priv_apks),testkey)
$(call auto-prebuilt-priv-apps,$(nosign_priv_apks),PRESIGNED)
###############################################################


###############################################################
# integrate vendor/operator/app
define auto-prebuilt-vendor-apps
$(foreach t,$(1), \
  $(eval include $(CLEAR_VARS)) \
  $(eval LOCAL_MODULE := $(basename $(notdir $(t)))) \
  $(eval LOCAL_MODULE_TAGS := optional) \
  $(eval LOCAL_MODULE_CLASS := APPS) \
  $(eval LOCAL_BUILT_MODULE_STEM := package.apk) \
  $(eval LOCAL_MODULE_PATH := $(PRODUCT_OUT)/system/vendor/operator/app) \
  $(eval LOCAL_MODULE_SUFFIX := $(COMMON_ANDROID_PACKAGE_SUFFIX)) \
  $(eval LOCAL_SRC_FILES := $(LOCAL_MODULE)/$(t)) \
  $(eval LOCAL_CERTIFICATE := $(2)) \
  $(eval LOCAL_MULTILIB := $(call get_lib)) \
  $(eval include $(BUILD_PREBUILT)) \
)
endef

$(call auto-prebuilt-vendor-apps,$(platform_vendor_apks),platform)
$(call auto-prebuilt-vendor-apps,$(media_vendor_apks),media)
$(call auto-prebuilt-vendor-apps,$(shared_vendor_apks),shared)
$(call auto-prebuilt-vendor-apps,$(test_vendor_apks),testkey)
$(call auto-prebuilt-vendor-apps,$(nosign_vendor_apks),PRESIGNED)
###############################################################



###############################################################
# integrate apks which are installed in system/presetapp

define auto-prebuilt-preset-apps
$(foreach t,$(1), \
  $(eval include $(CLEAR_VARS)) \
  $(eval LOCAL_MODULE := $(basename $(notdir $(t)))) \
  $(eval LOCAL_MODULE_TAGS := optional) \
  $(eval LOCAL_MODULE_CLASS := APPS) \
  $(eval LOCAL_BUILT_MODULE_STEM := package.apk) \
  $(eval LOCAL_MODULE_SUFFIX := $(COMMON_ANDROID_PACKAGE_SUFFIX)) \
  $(eval LOCAL_MODULE_PATH := $(PRODUCT_OUT)/system/presetapp) \
  $(eval LOCAL_SRC_FILES := $(LOCAL_MODULE)/$(t)) \
  $(eval LOCAL_CERTIFICATE := $(2)) \
  $(eval LOCAL_MULTILIB := $(call get_lib)) \
  $(eval include $(BUILD_PREBUILT)) \
)
endef

$(call auto-prebuilt-preset-apps,$(platform_preset_apks),platform)
$(call auto-prebuilt-preset-apps,$(presetapp_apks),PRESIGNED)
$(call auto-prebuilt-preset-apps,$(other_apks),PRESIGNED)
$(call auto-prebuilt-preset-apps,$(test_preset_apks),testkey)
###############################################################


