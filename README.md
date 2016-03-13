# python-tools
Python utilities for creative coding

## osc.py
OSC handling, can be both used as python module or called as command from bash

### Commands:
- Forward received messages to address  
  ```bash
./osc.py forward 1234 192.168.0.23:5678
```
  ```python
def forward(port, addr)
```
All messages received on `port` will be sent to `address`

- Do something on message  
  ```bash
./osc.py handle 1234 "~/my-script.sh"
```
  ```python
def handle(port, action)
```
If called from bash `action` is a single quoted command, if used in python is a
function like:
   ```python
def callback(path, msg)
```

- Display every message received on the given port  
  ```bash
./osc.py log 1234
```
  ```python
def print_log(port)
```

- Send message on a given path  
  ```bash
./osc.py send 192.168.0.23:5678 /synth1/volume 0.2
```
  ```python
def send(addr, path, *msg)
```

Addresses care in the form `ip:port`, if ip is omitted (just `port`) localhost
will be used.
