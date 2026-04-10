[app]
title = PT1Manager
package.name = pt1manager
package.domain = org.toopen7170
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 0.1

# Cython 3.x의 엄격한 검사를 피하기 위해 0.29.x 버전을 강제 지정합니다.
requirements = python3,kivy==2.3.0,plyer,android,cython==0.29.33

orientation = portrait
fullscreen = 1
android.archs = arm64-v8a
android.api = 31
android.minapi = 21
# NDK 버전을 안정적인 버전으로 고정합니다.
android.ndk = 25b
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, INTERNET

[buildozer]
log_level = 2
warn_on_root = 1
