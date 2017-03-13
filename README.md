# Con-checker

Tools to check your internet connection 24/7 and log results

### Prerequisites

You need python2 to run it

### Installing

```
git clone https://github.com/LucsT/con-checker /root/con-checker
cd /root/con-checker
```

Edit config.py if necessary


### Run it!
```
python con-checker.py
```

A log will be kept locally in status.log

### Enable and start daemon

```
ln -s /root/misc/con-checker.service /etc/systemd/system/con-checker.service
systemctl daemon-reload
systemctl enable con-checker
systemctl start con-checker
```