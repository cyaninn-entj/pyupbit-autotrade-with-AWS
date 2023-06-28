find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

today=$(date "+%Y%m%d")
nohup python3 ethereum_autotrade.py > output${today}.log &