[app]
title = PristonTale
package.name = pt1manager
package.domain = org.toopen7170
source.dir = .
source.include_exts = py,png,jpg,jpeg,ttf
version = 0.1
requirements = python3,kivy==2.3.0,plyer,android,cython==0.29.33
orientation = portrait
fullscreen = 1
android.archs = arm64-v8a
android.api = 31
android.minapi = 21
android.ndk = 25b
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, INTERNET
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
