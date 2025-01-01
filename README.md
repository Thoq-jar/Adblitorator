# Adblitorator

A network or device wide proxy to block ads
before they can even reach your browser.

## Setup

This uses the [MITM](https://mitmproxy.org) proxy library.

You may need to install the
certificate for [MITM](https://mitmproxy.org).

To do so follow the instructions at: [mitm.it](https://mitm.it).

There will be an automated installer in the future.

To access the site you may need to run the proxy!

Speaking of running:

You will need:

- [Python](https://python.org) (and pip)
- macOS/Linux (Windows may work, not tested yet)

Download code

```bash
git clone https://github.com/Thoq-jar/Adblitorator.git
```

Enter the directory

```bash
cd Adblitorator
```

Install dependencies

```bash
bin/bootstrap
```

Run Adblitorator

```bash
bin/run
```
