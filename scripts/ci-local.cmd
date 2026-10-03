@echo off
rem Reproduces .github/workflows/ci.yml job "test (windows-latest, 3.14)" 1:1.
rem Usage: scripts\ci-local.cmd [REPO_DIR]  (default: the repo containing this script). Stops at first failing step.
setlocal
if "%~1"=="" (pushd "%~dp0.." || exit /b 2) else (pushd "%~1" || exit /b 2)
set UV_PYTHON=3.14
call :now TOTAL0
call :step sync uv sync --locked || goto :fail
call :step ruff-check uv run ruff check . || goto :fail
call :step ruff-fmt uv run ruff format --check . || goto :fail
call :step pyright uv run pyright || goto :fail
call :step lint-imports uv run lint-imports || goto :fail
call :step pytest uv run pytest --cov "--cov-fail-under=80" || goto :fail
call :step zensical uv run zensical build || goto :fail
call :now TOTAL1
set /a TD=TOTAL1-TOTAL0
echo === TOTAL %TD%s - ALL PASS
exit /b 0

:fail
call :now TOTAL1
set /a TD=TOTAL1-TOTAL0
echo === TOTAL %TD%s - FAILED
exit /b 1

:now
for /f %%t in ('powershell -NoProfile -Command "[DateTimeOffset]::UtcNow.ToUnixTimeSeconds()"') do set %1=%%t
exit /b 0

:step
set NAME=%1
shift
call :now T0
echo === STEP: %NAME% : %1 %2 %3 %4 %5 %6 %7 %8
%1 %2 %3 %4 %5 %6 %7 %8
set RC=%errorlevel%
call :now T1
set /a DUR=T1-T0
if not "%RC%"=="0" (
  echo === FAIL %NAME% ^(%DUR%s, exit %RC%^)
  exit /b 1
)
echo === PASS %NAME% ^(%DUR%s^)
exit /b 0
