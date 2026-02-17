# Build K-Mod DLL (BTS 3.19)

## What is in this folder
- Full K-Mod SDK C++ sources (`CvGameCoreDLL/*.cpp`, `*.h`).
- Legacy `Makefile` used by `nmake`.
- `build_kmod.cmd` wrapper script to run a reproducible build on this machine setup.

## Prerequisites
- Microsoft Visual C++ Toolkit 2003 (`cl.exe`, `link.exe`).
- Microsoft Platform SDK (`nmake.exe`, Windows headers/libs).
- Civ4 SDK dependency folder containing:
  - `Boost-1.32.0`
  - `Python24`
  - `bin/fastdep.exe`

Default paths expected by `build_kmod.cmd`:
- `C:\Program Files (x86)\Civ4SDK\Microsoft Visual C++ Toolkit 2003`
- `C:\Program Files\Microsoft Platform SDK`
- `C:\Dev\Civ4 SDK\CvGameCoreDLL`
- `C:\Windows\Microsoft.NET\Framework\v2.0.50727` (for `cvtres.exe`)

You can override these by setting env vars before running:
- `TOOLKIT`
- `PSDK`
- `NMAKE_EXE`
- `CIV4_SDK_DEPS`
- `CVTRES_DIR`

## Build commands
Run from `CvGameCoreDLL`:

```bat
build_kmod.cmd Release
```

Other targets:

```bat
build_kmod.cmd Debug
build_kmod.cmd Profile
build_kmod.cmd clean
```

Output DLL:
- `CvGameCoreDLL\Release\CvGameCoreDLL.dll`

## Deploy to the mod
Copy the built DLL to:
- `..\Assets\CvGameCoreDLL.dll`

Example:

```bat
copy /Y Release\CvGameCoreDLL.dll ..\Assets\CvGameCoreDLL.dll
```
