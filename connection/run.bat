@echo off

REM Удаляем существующую базу данных, если она есть
del /F /Q database.db > nul 2>&1

REM Запускаем каждый python-скрипт последовательно
python .\config.py && (
    python .\data.py && (
        python .\users.py && (
            python .\fine.py && (
                python .\ts.py
            )
        )
    )
)

echo all files completed
pause