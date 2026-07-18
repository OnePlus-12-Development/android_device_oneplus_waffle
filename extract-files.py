#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'hardware/oplus',
    'hardware/qcom-caf/sm8650',
    'vendor/oneplus/sm8650-common',
    'vendor/qcom/opensource/commonsys-intf/display',
]


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'com.qti.sensor.lyt808',
        'libarcsoft_triple_sat',
        'libarcsoft_triple_zoomtranslator',
        'libdualcam_optical_zoom_control',
        'libdualcam_video_optical_zoom',
        'libhwconfigurationutil',
        'libpwirisfeature',
        'libpwirishalwrapper',
        'libtriplecam_optical_zoom_control',
        'libtriplecam_video_optical_zoom',
        'vendor.pixelworks.hardware.display-V2-ndk',
        'vendor.pixelworks.hardware.display@1.0',
        'vendor.pixelworks.hardware.display@1.1',
        'vendor.pixelworks.hardware.display@1.2',
        'vendor.pixelworks.hardware.feature-V1-ndk',
        'vendor.pixelworks.hardware.feature@1.0',
        'vendor.pixelworks.hardware.feature@1.1',
    ): lib_fixup_vendor_suffix,
}

blob_fixups: blob_fixups_user_type = {
    'odm/etc/camera/CameraHWConfiguration.config': blob_fixup()
        # Disable face detection AE behaviour
        .regex_replace(r'(enableSWfdForThirdCamUnit += )TRUE', r'\1FALSE')
        .regex_replace(r'(fdSupport += )TRUE;', r'\1FALSE;')
        # Expose AUX cameras
        .regex_replace('SystemCamera =  0;  0;  0;  1;  0; 1;', 'SystemCamera =  0;  0;  0;  0;  0; 0;'),
    (
        'odm/etc/libnfc-mtp-SN220.conf_22825',
        'odm/etc/libnfc-mtp-SN220.conf_22877',
    ): blob_fixup()
        .regex_replace('(NXPLOG_.*_LOGLEVEL)=0x03', '\\1=0x02')
        .regex_replace('NFC_DEBUG_ENABLED=1', 'NFC_DEBUG_ENABLED=0'),
    'odm/lib64/libAlgoProcess.so': blob_fixup()
        .replace_needed('android.hardware.graphics.common-V3-ndk.so', 'android.hardware.graphics.common-V7-ndk.so')
        .replace_needed('android.hardware.graphics.common-V4-ndk.so', 'android.hardware.graphics.common-V7-ndk.so'),
    'odm/lib64/libarcsoft_high_dynamic_range_v4.so': blob_fixup()
        .clear_symbol_version('remote_handle_close')
        .clear_symbol_version('remote_handle_invoke')
        .clear_symbol_version('remote_handle_open')
        .clear_symbol_version('remote_register_buf')
        .clear_symbol_version('remote_register_buf_attr'),
    (
        'odm/lib64/libCOppLceTonemapAPI.so',
        'odm/lib64/libSuperRaw.so',
        'odm/lib64/libYTCommon.so',
        'odm/lib64/libyuv2.so',
    ): blob_fixup()
        .replace_needed('libstdc++.so', 'libstdc++_vendor.so'),
    (
        'odm/lib64/libdisplaycolorfeature.so',
        'odm/lib64/libdisplayfossfeature_nature.so',
        'vendor/bin/hw/vendor.qti.hardware.display.composer-service',
        'vendor/lib64/libdpps.so',
        'vendor/lib64/libsnapdragoncolor-manager.so',
    ): blob_fixup()
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v34.so'),
    (
        'odm/lib64/libEIS.so',
        'odm/lib64/libEISLive.so',
        'odm/lib64/libHIS.so',
        'odm/lib64/libOGLManager.so',
        'odm/lib64/libOPAlgoCamFaceBeautyCap.so',
    ): blob_fixup()
        .clear_symbol_version('AHardwareBuffer_allocate')
        .clear_symbol_version('AHardwareBuffer_describe')
        .clear_symbol_version('AHardwareBuffer_lock')
        .clear_symbol_version('AHardwareBuffer_release')
        .clear_symbol_version('AHardwareBuffer_unlock'),
    'vendor/etc/libnfc-nci.conf': blob_fixup()
        .regex_replace('NFC_DEBUG_ENABLED=1', 'NFC_DEBUG_ENABLED=0'),
    'vendor/lib64/libcwb_qcom_aidl.so': blob_fixup()
        .add_needed('libui_shim.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'waffle',
    'oneplus',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
    add_firmware_proprietary_file=True,
)

if __name__ == '__main__':
    utils = ExtractUtils.device_with_common(
        module, 'sm8650-common', module.vendor
    )
    utils.run()
