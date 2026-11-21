@echo off
rem Converts .\input\<case>\*.pdf to .\output\<case>\*.json (extra arguments are passed through).
setlocal
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" -X utf8 -m odw2json %*
) else (
  python -X utf8 -m odw2json %*
)
