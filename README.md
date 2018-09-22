 ```                  
  ___ ___ _ _ _ ___ ___ ___ 
 |   | .'| | | | .'|   | . |
 |_|_|__,|_____|__,|_|_|___|
            100% OSS, BSD-2
```

Nawano is a lightweight, secure and fast [REPL](https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop) command-line application that provides a simple and intuative interface for managing Nano funds.

Seeds are encrypted with AES-256 and stored along with information about derivate keys locally.

Please bare in mind that—just as the official Nano software—Nawano uses the *BSD 2-Clause License* (i.e. no liability for loss of funds).



Demo
----

Shows some common wallet operations

[![asciicast](https://asciinema.org/a/HevbcFFyi2OT7KJ6kpLyVbqJo.png)](https://asciinema.org/a/HevbcFFyi2OT7KJ6kpLyVbqJo)


Project status: Development
--------------

While Nawano works, it should be considered unstable / unsafe / alpha, as it lacks Documentation, Unit Tests and sufficient volume of actual use.

**Todo -> stable**

**Quality improvements**
- [ ] API documentation
- [ ] Usage documentation
- [ ] Add *Unit Tests*
- [ ] Test more OSes

**Features**
- [ ] Transaction history
- [ ] Application logging
- [ ] Support for Websocket backends


Usage
=====

Ubuntu Linux
--------
```bash
$ sudo apt-get install libb2-dev
$ sudo pip3 install nawano
$ nawano
```

MacOS
-----
Work in progress


Windows
-------
Work in progress


Author
------
Robert Wikman \<rbw@vault13.org\>
