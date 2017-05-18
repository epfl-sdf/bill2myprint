ssh -fNAL 3306:127.0.0.1:3306 ubuntu@sdf-bill2myprint-mysql-1

source ./.venv/bin/activate
python3 src/manage.py shell

PID=`pgrep -f "ssh -fNAL 3306:127.0.0.1:3306 ubuntu@sdf-bill2myprint-mysql-1"`
if [[ "" !=  "$PID" ]]; then
  echo "killing $PID"
  kill $PID
fi
