# OSC-tool
Command line tool for the OSC protocol, can be also used as Python module.

TODO: setup.py

## Requirements
It depends on [pyliblo](http://das.nasophon.de/pyliblo/):
```
pip install pyliblo
```

If you are on GNU/Linux I suggest to use the one in the distribution repository,
e.g. in Debian/Ubuntu:
```
sudo apt install python-liblo
```

## Command line usage
OSC handling, can be both used as python module or called as command from bash

- Forward received messages to address  
  ```
./osc.py forward 1234 192.168.0.23:5678
```

- Do something on message  
  ```
./osc.py handle 1234 "~/my-script.sh"
```

- Display every message received on the given port  
  ```
./osc.py log 1234
```

- Send message on a given path  
  ```
./osc.py send 192.168.0.23:5678 /synth1/volume 0.2
```

Addresses are in the form `ip:port`, if ip is omitted (just `port`) localhost
will be used.
