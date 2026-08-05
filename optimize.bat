@echo off
chcp 65001 >nul
title Royal Steel - Optimizer
echo ============================================
echo ⚡ Royal Steel - Performance Optimizer
echo ============================================
echo.

cd /d "%~dp0"
if not exist "frontend" (
    echo ❌ frontend مش موجود!
    pause
    exit /b 1
)

:: 1. Minify CSS
echo [1/3] 🔧 Minify CSS...
for /r "frontend" %%f in (*.css) do (
    if not "%%~xf"==".min.css" (
        echo   %%~nxf
    )
)

:: 2. Minify JS  
echo.
echo [2/3] 🔧 Minify JS...
for /r "frontend" %%f in (*.js) do (
    if not "%%~xf"==".min.js" (
        echo   %%~nxf
    )
)

:: 3. Fix HTML
echo.
echo [3/3] 🔧 Fix HTML...
for /r "frontend" %%f in (*.html) do (
    powershell -Command "$c=(Get-Content '%%f'); $c=$c -replace '<script\s+(?!.*defer)(?!.*async)([^>]*src=)', '<script defer $1'; $c=$c -replace '(<iframe\s+(?!.*title=)[^>]*src=\")', '$1 title=\"Embedded Content\" '; $c=$c -replace '(<img\s+(?!.*loading=)[^>]*>)', '$1 loading=\"lazy\" '; Set-Content '%%f' $c"
    echo   %%~nxf
)

echo.
echo ============================================
echo 🎉 خلصنا!
echo.
echo اعمل Deploy:
echo    git add .
echo    git commit -m "Perf: optimize"
echo    git push
echo ============================================
pause