@echo off
start cmd /k "python port.py"
timeout /t 1 /nobreak >nul
start cmd /k "python backpack.py"
