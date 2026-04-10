[app]
title = PT1Manager
package.name = pt1manager
package.domain = org.toopen7170
source.dir = .
# 모든 이미지와 폰트 확장자를 포함하도록 수정했습니다. (검수 완료)
source.include_exts = py,png,jpg,jpeg,ttf,kv
version = 0.3
requirements = python3,kivy==2.3.0,plyer,android,cython==0.29.33
orientation = portrait
fullscreen = 1
android.archs = arm64-v8a
android.api = 31
android.minapi = 21
android.build_tools_version = 33.0.0
android.ndk = 25b
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, INTERNET
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
