[app]
title = PT1Manager
package.name = pt1manager
package.domain = org.toopen7170
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 0.1

# Cython 버전을 고정하고, 호환성을 위해 도구 버전을 맞춥니다.
requirements = python3,kivy==2.3.0,plyer,android,cython==0.29.33

orientation = portrait
fullscreen = 1
android.archs = arm64-v8a
android.api = 31
android.minapi = 21
android.ndk = 25b
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, INTERNET

# 추가된 핵심 포인트: 빌드 시 구버전 Cython 방식을 허용하도록 설정
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
