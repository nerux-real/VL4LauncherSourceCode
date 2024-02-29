pyinstaller --onefile --windowed --icon=./v4l_smp_logo.ico --distpath=./build --add-data "C:\Users\NERUX\AppData\Local\Programs\Python\Python311\Lib\site-packages\pyfiglet;./pyfiglet" ./launcher_gui.pyw
pyinstaller --onefile --icon=./v4l_smp_logo.ico --distpath=./build ./launcher_cli.py
pyinstaller --onefile --icon=./v4l_smp_logo.ico --distpath=./build ./launcher_updater.py