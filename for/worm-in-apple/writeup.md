# Forensics | Worm In Apple

Once you've found that the sublime package is a zip file, unzip it.

As the plugin is a real one you should be able to download an original version
of it and make a diff on all files (the fastest way to find the "worm").

When you find the awkward piece of code, de-obfuscate it to find out what it's
actually doing when started.

You should find that it communicates regularly with a server. It's a beacon.

As you were told to _investigate as far as you can_, you try to communicate
with the webserver receiving messages from the beacon.

See `exploit/exploit` for then automated exploitation of the server.
