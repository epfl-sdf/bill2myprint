source ./.venv/bin/activate

sudo aptitude install unixodbc unixodbc-dev freetds-dev tdsodbc

cat > /etc/odbc.ini << EOL
[FreeTDS]
  Description=FreeTDS Driver
  Driver=/usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so
  Setup=/usr/lib/x86_64-linux-gnu/odbc/libtdsS.so
  CPTimeout =
  CPReuse =
EOL

cat > /etc/odbcinst.ini << EOL
[FreeTDS]
Description=TDS driver (Sybase/MS SQL)
Driver=libtdsodbc.so
Setup=libtdsS.so
CPTimeout=
CPReuse=
UsageCount=2
EOL
