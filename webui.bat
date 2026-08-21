@echo off

title Stable Diffusion WebUI - Pythonとpipを確認しています...

if not defined PYTHON (set PYTHON=python)
if defined GIT (set "GIT_PYTHON_GIT_EXECUTABLE=%GIT%")
if not defined VENV_DIR (set "VENV_DIR=%~dp0%venv")

set SD_WEBUI_RESTART=tmp/restart
set ERROR_REPORTING=FALSE

mkdir tmp 2>NUL

%PYTHON% -c "" >tmp/stdout.txt 2>tmp/stderr.txt
if %ERRORLEVEL% == 0 goto :check_pip
title Stable Diffusion WebUI - Pythonをインストールしています...
curl  -L -O "https://www.python.org/ftp/python/3.10.6/python-3.10.6-amd64.exe"
echo msgbox "Pythonインストーラを開きます。「Add python.exe to PATH」へチェックを入れ、「Install Now」を選択してください。インストールできたらこのアプリをもう一度起動してください。" > %TEMP%/msgboxtest.vbs & %TEMP%/msgboxtest.vbs
start python-3.10.6-amd64.exe & goto :show_stdout_stderr

:check_pip
%PYTHON% -mpip --help >tmp/stdout.txt 2>tmp/stderr.txt
if %ERRORLEVEL% == 0 goto :start_venv
if "%PIP_INSTALLER_LOCATION%" == "" goto :show_stdout_stderr
%PYTHON% "%PIP_INSTALLER_LOCATION%" >tmp/stdout.txt 2>tmp/stderr.txt
if %ERRORLEVEL% == 0 goto :start_venv
goto :show_stdout_stderr

:start_venv
if ["%VENV_DIR%"] == ["-"] goto :skip_venv
if ["%SKIP_VENV%"] == ["1"] goto :skip_venv


dir "%VENV_DIR%\Scripts\Python.exe" >tmp/stdout.txt 2>tmp/stderr.txt
if %ERRORLEVEL% == 0 goto :activate_venv

for /f "delims=" %%i in ('CALL %PYTHON% -c "import sys; print(sys.executable)"') do set PYTHON_FULLNAME="%%i"
title Stable Diffusion WebUI - %PYTHON_FULLNAME% を使って %VENV_DIR% を作成しています...
%PYTHON_FULLNAME% -m venv "%VENV_DIR%" >tmp/stdout.txt 2>tmp/stderr.txt
if %ERRORLEVEL% == 0 goto :upgrade_pip
goto :show_stdout_stderr

:upgrade_pip
title Stable Diffusion WebUI - PIPをアップグレードしています...
"%VENV_DIR%\Scripts\Python.exe" -m pip install --upgrade pip
if %ERRORLEVEL% == 0 goto :activate_venv
echo 警告: PIPをアップグレードできませんでした。

:activate_venv
title Stable Diffusion WebUI - %VENV_DIR%\Scripts\activate.bat
set PYTHON="%VENV_DIR%\Scripts\Python.exe"
call "%VENV_DIR%\Scripts\activate.bat"

:skip_venv
if %ACCELERATE% == "True" goto :accelerate
goto :launch

:accelerate
set ACCELERATE="%VENV_DIR%\Scripts\accelerate.exe"
if EXIST %ACCELERATE% goto :accelerate_launch

:launch
title Stable Diffusion WebUI %COMMANDLINE_ARGS%
%PYTHON% launch.py %*
if EXIST tmp/restart goto :skip_venv
goto :endofscript

:accelerate_launch
title Stable Diffusion WebUI %COMMANDLINE_ARGS% with %ACCELERATE%
%ACCELERATE% launch --num_cpu_threads_per_process=6 launch.py
if EXIST tmp/restart goto :skip_venv
goto :endofscript

:show_stdout_stderr

echo.
echo exit code: %errorlevel%

for /f %%i in ("tmp\stdout.txt") do set size=%%~zi
if %size% equ 0 goto :show_stderr
echo.
echo stdout:
type tmp\stdout.txt

:show_stderr
for /f %%i in ("tmp\stderr.txt") do set size=%%~zi
if %size% equ 0 goto :show_stderr
echo.
echo stderr:
type tmp\stderr.txt

:endofscript

echo.
echo msgbox "起動に失敗しました。" > %TEMP%/msgboxtest.vbs & %TEMP%/msgboxtest.vbs
