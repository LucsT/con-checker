con-checker
===========
Tools to check your internet connection.

Usage :
  $ python con-checker.py

Log will be save in the current directory as status.log

You can edit your local router Ip.
        edit sleeping time

Configure

Edit confs

Enable and start daemon

ln -s ./misc/con-checker.service /etc/systemd/system/con-checker.service
systemctl daemon-reload
systemctl enable con-checker
systemctl start con-checker
