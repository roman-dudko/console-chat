# CLient-server console chat
> Based on Python 'socket' and 'threading' libraries

## Starting Server applicaton

``` bash
# run server.py from root folder:
$ python3 server.py

# Select port. '7777' is ussed by default in case you press enter.  
$ Enter port (press Enter to use default):
```

## Starting Client application

``` bash
# run client.py from root folder:
$ python3 client.py

# Select server IP and port. Default values: 'localhost' and '7777'.  
$ Enter server (press Enter to use default):
$ Enter port (press Enter to use default): 
```

## Chatting
Connected clients can send/receive messages asynchronously. Ssytem messages are shown on client enter/exit. 

## Supported commands
Type /help to see available commands:
``` bash
/whois #show list of online users
/count #show number of online users
/time #show current time
/game #'paper-rock-scissors' game
```
