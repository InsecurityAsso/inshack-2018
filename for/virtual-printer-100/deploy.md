# Deploy

## Dependencies

### Python

```bash
sudo apt install python3 python3-pip redis
pip3 install Pillow redis
```

### REDIS

```bash
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
```

### Securing Redis

[source](https://redis.io/topics/quickstart)

By default Redis binds to all the interfaces and has no authentication at all. If you use Redis into a very controlled 
environment, separated from the external internet and in general from attackers, that's fine. However if Redis without 
any hardening is exposed to the internet, it is a big security concern. If you are not 100% sure your environment is 
secured properly, please check the following steps in order to make Redis more secure, which are enlisted in order of 
increased security.

1. Make sure the port Redis uses to listen for connections (by default 6379 and additionally 16379 if you run Redis in 
cluster mode, plus 26379 for Sentinel) is firewalled, so that it is not possible to contact Redis from the outside world.
2. Use a configuration file where the bind directive is set in order to guarantee that Redis listens just in as little 
network interfaces you are using. For example only the loopback interface (127.0.0.1) if you are accessing Redis just 
locally from the same computer, and so forth.
3. *(/!\ the script implements no authent currently /!\)* Use the requirepass option in order to add an additional layer 
of security so that clients will require to authenticate using the AUTH command.
4. *(/!\ do not do that, server will listen on loopback /!\)* Use spiped or another SSL tunnelling software in order to encrypt 
traffic between Redis servers and Redis clients if your environment requires encryption.

Note that a Redis exposed to the internet without any security is very simple to exploit, so make sure you understand the 
above and apply at least a firewalling layer. After the firewalling is in place, try to connect with redis-cli from an 
external host in order to prove yourself the instance is actually not reachable.

## Setup the challenge

### Start redis

```bash
redis-server
```

### Clone the repo

```bash
git clone git@github.com:HugoDelval/inshack-2018.git
cd inshack-2018/challenges/forensics/virtual-printer-100
echo "INSA{THE REAL FLAG}" > flag.txt
cd server-files
chmod 700 virtual_printer_wrapper.py
./virtual_printer_wrapper.py
```
