
@echo off
SET PROJECT_DIR=%~dp0
cd /d "%PROJECT_DIR%"
IF NOT EXIST "venv" (
    echo إنشاء البيئة الافتراضية...
    python -m venv venv
) ELSE (
    echo البيئة الافتراضية موجودة بالفعل
)
call venv\Scriptsctivate
echo تثبيت المكتبات المطلوبة...
pip install --upgrade pip
pip install pandas matplotlib seaborn fpdf tk
echo تشغيل البرنامج...
python student_analysis.py
deactivate
echo البرنامج تم تشغيله وانتهى
pause
