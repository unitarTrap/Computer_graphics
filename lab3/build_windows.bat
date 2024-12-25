@echo off
pyinstaller --noconfirm --onefile --windowed ^
--name "AlienInvasion" ^
--icon=resources/Images/ship.bmp ^
--add-data "resources/Images;resources/images" ^
--add-data "resources/sounds;resources/sounds" ^
--add-data "resources/sounds;resources/saves" ^
alien_invasion.py
pause
