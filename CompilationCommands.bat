call .\env\Scripts\activate
call pyinstaller -F --clean main.spec
call pyinstaller -F --clean debug.spec
