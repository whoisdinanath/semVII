@echo off
setlocal enabledelayedexpansion

REM ============================
REM Configuration Section
REM ============================

REM Get the directory where the script is located
set "script_dir=%~dp0"

REM Define the input and output directories
set "input_dir=%script_dir%drawio\"
set "output_dir=%script_dir%img\"

REM Define a local temp directory inside the script directory
set "temp_dir=%script_dir%temp\pdfcrop_temp"

REM ============================
REM Setup Section
REM ============================

REM Create the local temp directory if it doesn't exist
if not exist "%temp_dir%" (
    mkdir "%temp_dir%"
    if errorlevel 1 (
        echo Failed to create local temp directory "%temp_dir%".
        exit /b 1
    )
)

REM Redirect TEMP and TMP to the local temp directory
set "TEMP=%temp_dir%"
set "TMP=%temp_dir%"

REM Ensure the output directory exists
if not exist "%output_dir%" (
    mkdir "%output_dir%"
    if errorlevel 1 (
        echo Failed to create output directory "%output_dir%".
        exit /b 1
    )
)
REM ============================
REM Processing Section
REM ============================

REM Avoid hardlink privilege issue globally
set "PDFCROP_NOLINKS=1"

REM Loop through all .drawio files in the input directory
for %%f in ("%input_dir%\*.drawio") do (
    echo Processing %%~nxf...

    REM Export the .drawio file to PDF
    draw.io --export "%%f" --output "%output_dir%\%%~nf.pdf" --format pdf
    if errorlevel 1 (
        echo Failed to export %%~nxf to PDF. Skipping...
    ) else (
        REM Use cmd /C to ensure PDFCROP_NOLINKS is respected
        cmd /C "set PDFCROP_NOLINKS=1 && pdfcrop \"%output_dir%\%%~nf.pdf\" \"%output_dir%\%%~nf_cropped.pdf\""
        if errorlevel 1 (
            echo Failed to crop %%~nf.pdf. Skipping...
        ) else (
            del "%output_dir%\%%~nf.pdf"
            if errorlevel 1 (
                echo Failed to delete "%output_dir%\%%~nf.pdf". Please check permissions.
            ) else (
                ren "%output_dir%\%%~nf_cropped.pdf" "%%~nf.pdf"
                if errorlevel 1 (
                    echo Failed to rename "%%~nf_cropped.pdf". Please check permissions.
                ) else (
                    echo Successfully processed %%~nxf.
                )
            )
        )
    )
)


REM ============================
REM Cleanup Section
REM ============================

REM Remove the local temporary directory
rd /s /q "%temp_dir%"

echo All files processed.
pause
