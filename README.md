 ```                  
  ___ ___ _ _ _ ___ ___ ___ 
 |   | .'| | | | .'|   | . |
 |_|_|__,|_____|__,|_|_|___|
            100% OSS, BSD-2
```

Nawano is a lightweight, secure and fast [REPL](https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop) command-line application that provides a simple and intuative interface for managing Nano funds.

Seeds are encrypted with AES-256 and stored along with information about derivate keys locally.

Please bare in mind that—just as the official Nano software—Nawano uses the *BSD 2-Clause License* (i.e. no liability for loss of funds).

- Want to know more about Nano? Check out the [official website](https://nano.org/en/about).

- Don't have any Nano? You can get a small amount for testing purposes at [nano-faucet.org](https://nano-faucet.org)


Demo
----

Shows some common wallet operations

[![asciicast](https://asciinema.org/a/HevbcFFyi2OT7KJ6kpLyVbqJo.png)](https://asciinema.org/a/HevbcFFyi2OT7KJ6kpLyVbqJo)


Project status: Development/Testing
--------------

While Nawano does work, it probably should be considered unstable/unsafe/alpha as it lacks Documentation, Unit Tests and extensive real-world use.


Beta
----

**Quality improvements**
- [ ] API documentation
- [ ] Usage documentation
- [ ] Unit tests & TravisCI
- [ ] Test more OSes

**Features**
- [ ] Transaction history
- [ ] Application logging
- [ ] Support for Websocket backends

**Guides**
- [X] Linux installation guide
- [X] MacOS installation guide
- [ ] Windows installation guide
- [ ] Operations/Wiki


Future
------
- Ledger integration
- Yubikey integration
- Official Debian package
- LSM support (SELinux/AppArmor)


Usage/Installing
=======

Ubuntu Linux
--------
```bash
$ sudo apt-get install libb2-dev
$ sudo pip3 install nawano --upgrade
$ nawano
```

MacOS
-----
```bash
$ brew install cmake gcc libb2 python3
$ sudo CC=/usr/local/bin/gcc-8 pip3.7 install nawano --upgrade
$ nawano
```

Windows
-------
TBA


Author
------
Robert Wikman \<rbw@vault13.org\>
