[app]

# (string) Title of your application
title = Lumix

# (string) Package name
package.name = lumix

# (string) Package domain (needed for android packaging)
package.domain = org.lumix

# (string) Source code where the main.py / client.py lives
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,spec

# (string) Main script name
source.filename = client.py

# (str) Icon of the application (Твоя кастомная аватарка)
icon.filename = 1782773291535.png

# (string) Application version
version = 0.1

# (list) Application requirements
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

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (list) Architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) Enable AndroidX support (required for KivyMD)
android.enable_androidx = True

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
