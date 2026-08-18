@echo off

set PYTHON="C:\Users\%username%\AppData\Local\Programs\Python\Python310\python.exe"
set GIT=
set VENV_DIR=

nvidia-smi
if %ERRORLEVEL% NEQ 0 (
    set COMMANDLINE_ARGS=--use-cpu all --precision full --no-half --skip-torch-cuda-test
) else (
    set COMMANDLINE_ARGS=--xformers
)

call webui.bat
