@echo off
setlocal EnableExtensions

set "TARGET=%~1"
if "%TARGET%"=="" set "TARGET=Release"

if /I "%TARGET%"=="clean" goto clean_all
if /I "%TARGET%"=="Release" goto build_target
if /I "%TARGET%"=="Debug" goto build_target
if /I "%TARGET%"=="Profile" goto build_target

echo Usage: build_kmod.cmd [Release^|Debug^|Profile^|clean]
exit /b 1

:clean_all
call :resolve_paths || exit /b 1
call :run_nmake Release_clean || exit /b 1
call :run_nmake Debug_clean || exit /b 1
call :run_nmake Profile_clean || exit /b 1
echo Clean complete.
exit /b 0

:build_target
call :resolve_paths || exit /b 1
call :run_nmake %TARGET%_clean || exit /b 1
call :run_nmake %TARGET% || exit /b 1
echo Build complete: %CD%\%TARGET%\CvGameCoreDLL.dll
exit /b 0

:resolve_paths
if not defined TOOLKIT set "TOOLKIT=C:\Program Files (x86)\Civ4SDK\Microsoft Visual C++ Toolkit 2003"
if not defined PSDK set "PSDK=C:\Program Files\Microsoft Platform SDK"
if not defined NMAKE_EXE set "NMAKE_EXE=%PSDK%\Bin\nmake.exe"
if not defined CVTRES_DIR set "CVTRES_DIR=C:\Windows\Microsoft.NET\Framework\v2.0.50727"
if not defined CIV4_SDK_DEPS set "CIV4_SDK_DEPS=C:\Dev\Civ4 SDK\CvGameCoreDLL"

if not exist "%TOOLKIT%\bin\cl.exe" (
  echo ERROR: cl.exe not found under "%TOOLKIT%".
  echo Set TOOLKIT to your VC++ Toolkit 2003 root folder.
  exit /b 1
)

if not exist "%PSDK%\Include\Windows.h" (
  echo ERROR: Windows headers not found under "%PSDK%".
  echo Set PSDK to your Microsoft Platform SDK root folder.
  exit /b 1
)

if not exist "%NMAKE_EXE%" (
  echo ERROR: nmake.exe not found at "%NMAKE_EXE%".
  echo Set NMAKE_EXE to your nmake.exe full path.
  exit /b 1
)

if not exist "%CIV4_SDK_DEPS%\Boost-1.32.0\include" (
  echo ERROR: Boost include folder missing in "%CIV4_SDK_DEPS%".
  echo Set CIV4_SDK_DEPS to a Civ4 SDK directory containing Boost-1.32.0 and Python24.
  exit /b 1
)

if not exist "%CIV4_SDK_DEPS%\Python24\include" (
  echo ERROR: Python24 include folder missing in "%CIV4_SDK_DEPS%".
  exit /b 1
)

if not exist "%CIV4_SDK_DEPS%\bin\fastdep.exe" (
  echo ERROR: fastdep.exe missing in "%CIV4_SDK_DEPS%\bin".
  exit /b 1
)

if not exist "%CVTRES_DIR%\cvtres.exe" (
  echo WARNING: cvtres.exe not found in "%CVTRES_DIR%".
  echo          Link step may fail unless cvtres.exe is already in PATH.
)

call :shortpath "%TOOLKIT%" TOOLKIT_SHORT || exit /b 1
call :shortpath "%PSDK%" PSDK_SHORT || exit /b 1
call :shortpath "%CIV4_SDK_DEPS%" DEPS_SHORT || exit /b 1
call :shortpath "%CIV4_SDK_DEPS%\bin\fastdep.exe" FD_SHORT || exit /b 1

set "PROJECT_INCS=/I%DEPS_SHORT%\Boost-1.32.0\include /I%DEPS_SHORT%\Python24\include"
set "PROJECT_LIBS=/LIBPATH:%DEPS_SHORT%\Python24\libs /LIBPATH:%DEPS_SHORT%\Boost-1.32.0\libs boost_python-vc71-mt-1_32.lib"
set "PATH=%CVTRES_DIR%;%PATH%"
exit /b 0

:run_nmake
echo.
echo === nmake %~1 ===
"%NMAKE_EXE%" /NOLOGO /f Makefile TOOLKIT=%TOOLKIT_SHORT% PSDK=%PSDK_SHORT% FD=%FD_SHORT% "PROJECT_INCS=%PROJECT_INCS%" "PROJECT_LIBS=%PROJECT_LIBS%" %~1
exit /b %ERRORLEVEL%

:shortpath
set "SP_INPUT=%~1"
set "SP_OUT="

if not exist "%SP_INPUT%" (
  echo ERROR: path does not exist: "%SP_INPUT%"
  exit /b 1
)

for %%I in ("%SP_INPUT%") do set "SP_OUT=%%~sI"

if "%SP_OUT%"=="" (
  echo ERROR: unable to resolve short path for "%SP_INPUT%".
  exit /b 1
)

if not "%SP_OUT: =%"=="%SP_OUT%" (
  echo ERROR: short path conversion failed for "%SP_INPUT%".
  echo        Enable 8.3 short names or set paths without spaces.
  exit /b 1
)

set "%~2=%SP_OUT%"
exit /b 0
