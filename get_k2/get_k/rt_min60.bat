echo bat 1 %time:~0,11% >> %~dp0\min60.txt
python %~dp0\daily_kline_min60.py
echo bat 2 %time:~0,11% >> %~dp0\min60.txt
