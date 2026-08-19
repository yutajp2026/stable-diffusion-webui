@echo off
title Stable Diffusion WebUI
set PYTHON="C:\Users\%username%\AppData\Local\Programs\Python\Python310\python.exe"

nvidia-smi
if %ERRORLEVEL% NEQ 0 (
    set COMMANDLINE_ARGS=--use-cpu all --precision full --no-half --skip-torch-cuda-test
) else (
    set COMMANDLINE_ARGS=--xformers
)

git config --global --add safe.directory %~dp0
if %ERRORLEVEL% NEQ 0 (
    winget install --id Git.Git -e --source winget
    echo Gitをインストールしました。もう一度このアプリを起動する必要があるかもしれません。
)

call webui.bat
