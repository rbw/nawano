 ```                  
  ___ ___ _ _ _ ___ ___ ___ 
 |   | .'| | | | .'|   | . |
 |_|_|__,|_____|__,|_|_|___|
            100% OSS, BSD-2
```

Nawano is a simple, fast and secure Nano currency management software that lets you set up a light-wallet locally on your machine and get started in just a few minutes — without doing any syncing, and without having to trust a wallet provider on the *World Wide Web*.

Seeds are encrypted with AES-256 and never leaves your computer. Node communication is done over RPC, using either a remote backend (such as Canoe) or a local node.

**Want to know more about Nano?** 

- Check out the [official website](https://nano.org/en/about).

**Want some free Nano to get started?**
 
- You can get a small amount for testing purposes at [nano-faucet.org](https://nano-faucet.org)


Demo
----

Shows some common wallet operations

[![asciicast](https://asciinema.org/a/HevbcFFyi2OT7KJ6kpLyVbqJo.png)](https://asciinema.org/a/HevbcFFyi2OT7KJ6kpLyVbqJo)


Installing
=======

**Requirements**
- Python >= 3.6
- Blake2 (libb2)
- OpenMP (libomp)

Ubuntu Linux
--------
```bash
$ sudo apt-get install libb2-dev libomp-dev python3
$ sudo pip3 install nawano --upgrade
$ nawano
```

MacOS
-----
```bash
$ brew install gcc libb2 libomp python3
$ sudo install nawano --upgrade
$ nawano
```

Windows
-------
Nawano can be installed in Microsoft Windows using WSL.

1. Enable WSL: https://docs.microsoft.com/en-us/windows/wsl/install-win10 
2. Using **Microsoft Store**, install **Ubuntu Linux** and start it.
3. Follow the **Ubuntu Linux** install instruction above.
4. Close the terminal window and create a desktop shortcut with location: ```wsl nawano```


Project status
--------------

While Nawano does work, it's currently under heavy development and probably should be considered unstable as it lacks *Test automation* and extensive real-world use.


Beta
----

**Quality improvements**
- [ ] API documentation
- [ ] Usage documentation (Wiki)
- [ ] Unit tests & TravisCI
- [ ] Test more OSes

**Features**
- [ ] Transaction history
- [ ] Application logging
- [ ] Support for Websocket backends

**Install guides**
- [X] Linux
- [X] MacOS
- [X] Windows


Future
------
- Ledger integration
- Yubikey integration
- Official Debian package
- LSM support (SELinux/AppArmor)


License
-------
Please bare in mind that—just as the official Nano software—Nawano uses the *BSD 2-Clause License* (i.e. no liability for loss of funds).

Author
------
Robert Wikman \<rbw@vault13.org\>
