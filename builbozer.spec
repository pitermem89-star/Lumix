[app]

# (string) Title of your application
title = LUMIX

# (string) Package name
package.name = lumix

# (string) Package domain (needed for android packaging)
package.domain = org.lumix

# (string) Source code where the main.py / client.py lives
source.dir = .

# (list) Source files to include (let's include everything python and kv)
source.include_exts = py,png,jpg,kv,spec

# (string) Main script name (Поскольку у тебя главный файл client.py, пишем его!)
source.filename = client.py

# (string) Application version
version = 0.1

# (list) Application requirements
# Обязательно добавляем kivymd и websockets, чтобы билд не падал
requirements = python3,kivy==2.3.0,kivymd==1.2.0,websockets,materialyoucolor,exceptiongroup,asyncio

# (str) Supported orientations (landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# =============================================================================
# Android specific configuration
# =============================================================================

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (list) list of Java .jar files to add to the libs so that pyobjus can use them
#android.add_jars = foo.jar

# (list) Architectures to build for (ARM64 для современных тел, ARMv7 для старых)
android.archs = arm64-v8a, armeabi-v7a

# (bool) Enable AndroidX support (required for KivyMD)
android.enable_androidx = True

# (str) The Android arch to build for choices: armeabi-v7a, arm64-v8a, x86, x86_64
# (if not specified, built for all architecture specified in android.archs)
#android.arch = arm64-v8a

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
