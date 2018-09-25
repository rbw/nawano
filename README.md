 ```                  
  ___ ___ _ _ _ ___ ___ ___ 
 |   | .'| | | | .'|   | . |
 |_|_|__,|_____|__,|_|_|___|
            100% OSS, BSD-2
```

Nawano is a simple, secure and lightweight Nano funds management software that lets you set up a fully functional light-wallet locally on your machine and get started in just a few minutes — without doing any syncing, and without having to trust a wallet provider on the *World Wide Web*.

Seeds are encrypted with AES-256 and never leaves your computer. Node communication is done over RPC, using either a remote backend (such as Canoe) or a local node.

**Want to know more about Nano?** 

- Check out the [official website](https://nano.org/en/about).

**Want some free Nano to get started?**
 
- You can get a small amount for testing purposes at [nano-faucet.org](https://nano-faucet.org)


Please bare in mind that—just as the official Nano software—Nawano uses the *BSD 2-Clause License* (i.e. no liability for loss of funds).


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


Usage/Installing
=======

**Requirements**
- Python >= 3.6
- libb2 (Blake2)
- libomp (OpenMP)

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
2. Install the **latest version of Ubuntu Linux** using **Microsoft Store** and start it.
3. Follow the **Ubuntu Linux** installation guide above.
4. Close the terminal window and create a desktop shortcut with location: ```wsl nawano```


Author
------
Robert Wikman <rbw@vault13.org>
