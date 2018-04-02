# web | Crypt0r second step

The goal here is to buy the file n°3. You have some money in your session cookie but not enough to buy the file. You need to modify the cookie to exploit the challenge.

Here is the shape of the cookie:

```
${SALT}:${SIGN}:${BASE64_ENCODED_YAML}
```

The content of the yaml file is signed to generate `${SIGN}` in the following way:

```
${SIGN} = sha256(${PRIVATE_KEY} + ${SALT} + ${YAML_CONTENT})
```

You cannot generate the signature on the client side as `${PRIVATE_KEY}` is unknown.

If the content of the yaml is altered (aka if you modify the amount of money), the server will reject your cookie.

The trick is that this type of signature is unsafe, it is exploitable by a [length extension attack](https://en.wikipedia.org/wiki/Length_extension_attack).

Hence, it is possible to generate a new cookie and a new signature from an existing one.

```
new_yaml = old_yaml + garbage + injection_goes_here
```

To see the full exploit, please refer to the `exploit/exploit` file.

PS: this challenge was written by our sponsor OVH ([https://ovh.com/](https://ovh.com/)), thanks again.
