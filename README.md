 ```                  
  ___ ___ _ _ _ ___ ___ ___ 
 |   | .'| | | | .'|   | . |
 |_|_|__,|_____|__,|_|_|___|
            100% OSS, BSD-2
```

Nawano is a simple, fast and secure way to manage your Nano funds locally—without doing any syncing, and without having to trust a wallet provider on the *World Wide Web*.

Seeds are encrypted with AES-256 and never leaves your computer.

Node communication is done over RPC; locally or using a remote backend (such as Canoe).

**Want to know more about Nano?** 

- Check out the [official website](https://nano.org/en/about).

**Want some free Nano to get started?**
 
- You can get a small amount for testing purposes at [nano-faucet.org](https://nano-faucet.org)


Demo
----

Shows some common wallet operations.

[![asciicast](https://asciinema.org/a/HevbcFFyi2OT7KJ6kpLyVbqJo.png)](https://asciinema.org/a/HevbcFFyi2OT7KJ6kpLyVbqJo)


Installing
----------


**Linux (Ubuntu)**

available setup (pip) environment variables:
- USE_GPU (install OpenCL libs and set to 1 to use the GPU for work generation)


```bash
$ sudo apt-get install libb2-dev python3
$ sudo pip3 install nawano --upgrade
$ nawano
```

**MacOS**

available setup (pip) environment variables:
- USE_GPU (enabled by default, set to 0 to use CPU for work generation)
- LINK_OMP (enabled by default, set to 0 to use gcc with builtin GOMP)


```bash
$ brew install gcc libb2 libomp python3
$ sudo pip3 install nawano --upgrade
$ nawano
```

**Windows**

Nawano can be installed in Microsoft Windows using WSL.

1. Enable WSL: https://docs.microsoft.com/en-us/windows/wsl/install-win10 
2. Using **Microsoft Store**, install **Ubuntu Linux** and start it.
3. Follow the **Ubuntu Linux** install instruction above.

You may now close the terminal window and simply run ```wsl nawano``` to start the application.


Project status
--------------

While Nawano does work, it's currently under heavy development and should probably be considered unstable as it lacks tests and extensive real-world use.


**Quality improvements**
- [ ] API documentation
- [ ] Usage documentation (Wiki)
- [ ] Unit tests & TravisCI

**Features**
- [ ] Transaction history
- [ ] Application logging

**Install guides**
- [X] Linux
- [X] MacOS
- [X] Windows


Future plans
------
- Ledger integration
- Yubikey integration
- Official Debian package


License
-------
Please bare in mind that—just as the official Nano software—Nawano uses the *BSD 2-Clause License* (i.e. no liability for loss of funds).


Author
------
Robert Wikman \<rbw@vault13.org\>
