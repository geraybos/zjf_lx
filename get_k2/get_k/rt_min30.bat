echo bat 1 %time:~0,11% >> %~dp0\min30.txt
python %~dp0\daily_kline_min30.py
echo bat 2 %time:~0,11% >> %~dp0\min30.txt
python %~dp0\new_kline_60.py
