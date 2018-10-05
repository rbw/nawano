 ```                  
  ___ ___ _ _ _ ___ ___ ___ 
 |   | .'| | | | .'|   | . |
 |_|_|__,|_____|__,|_|_|___|
            100% OSS, BSD-2
```

Nawano provides a simple, fast and secure way of managing your Nano funds locally—without doing any syncing, and without having to trust a wallet provider on the *World Wide Web*.

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

Available setup (pip) environment variables:
- `CC=/path/to/c/compiler`
  * ALL: Path to C compiler (searches for an up-to-date gcc in path by default)
- `USE_GPU=1|0`
  * Linux: Install OpenCL libs and set to 1 to use the GPU for work generation
  * OSX: Should work directly with OS-default OpenCL libs, simply pass `USE_GPU=1` to pip3.
- `LINK_OMP=1|0`
  * Linux: Not used
  * OSX: Linking of libomp. Set to 0 to use gcc with builtin GOMP

**Linux (Ubuntu)**

```bash
$ sudo apt-get install libb2-dev python3
$ sudo pip3 install nawano --upgrade
$ nawano
```

**MacOS**

```bash
$ brew install gcc libb2 libomp python3
$ sudo LINK_OMP=1 pip3 install nawano --upgrade
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
- [ ] NanoBeam default backend
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
- Daily lottery mini-game
- Official Debian package


License
-------
Please bare in mind that—just as the official Nano software—Nawano uses the *BSD 2-Clause License* (i.e. no liability for loss of funds).


Author
------
Robert Wikman \<rbw@vault13.org\>
