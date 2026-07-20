#
# Copyright (C) 2021-2025 The LineageOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

# Inherit from those products. Most specific first.
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit_only.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)

# Inherit from waffle device
$(call inherit-product, device/oneplus/waffle/device.mk)

# Inherit some common Lineage stuff.
$(call inherit-product, vendor/lineage/config/common_full_phone.mk)

PRODUCT_NAME := lineage_waffle
PRODUCT_DEVICE := waffle
PRODUCT_MANUFACTURER := OnePlus
PRODUCT_BRAND := OnePlus
PRODUCT_MODEL := CPH2573

PRODUCT_GMS_CLIENTID_BASE := android-oneplus

PRODUCT_BUILD_PROP_OVERRIDES += \
    BuildDesc="qssi_64-user 16 BP2A.250605.015 1783515001002 release-keys" \
    BuildFingerprint=OnePlus/CPH2573IN/OP595DL1:16/BP2A.250605.015/U.R4T3.1bb7df3_9001b7_8f80ba:user/release-keys \
    DeviceName=OP595DL1 \
    DeviceProduct=CPH2573 \
    SystemDevice=OP595DL1 \
    SystemName=CPH2573
