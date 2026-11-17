<p align="center">
  <img src="at0m_icon.webp" alt="At0mSubnet logo" width="160">
</p>

<h1 align="center">&gt; At0mSubnet</h1>

<p align="center">
  <b>⚛️ A lightweight, dark-neon IPv4 subnet calculator for your desktop ⚔️</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8+-00ff15?style=for-the-badge&logo=python&logoColor=white&labelColor=0a0a0f" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/GUI-tkinter-00e5ff?style=for-the-badge&labelColor=0a0a0f" alt="tkinter">
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux-ff2bd6?style=for-the-badge&labelColor=0a0a0f" alt="Windows | Linux">
</p>

---

## 🚀 What is it?

**At0mSubnet** is a desktop app that does the subnetting math for you. Type an IP address and a CIDR prefix, hit **CALCULATE**, and get everything you need in a hacker-style dark UI. No browser, no internet, no dependencies beyond Python's standard library.

## ✨ Features

- 🧮 **Full subnet breakdown:** Network ID, subnet mask (decimal and binary), wildcard mask, broadcast address, usable host range and number of usable hosts
- 🏷️ **IP type:** private, public, loopback, link-local, multicast or reserved
- 🔠 **IP class:** A, B, C, D or E
- 🛡️ **Input validation:** clear in-app error messages and automatic focus on the field you need to fix, so you can just try again
- 🎯 **Edge cases handled:** `/31` (point-to-point links, RFC 3021) and `/32` (single host) are calculated correctly
- 📋 **Copy results** to the clipboard with one click
- ⌨️ **Keyboard shortcuts:** `Enter` to calculate, `Esc` to clear
- 🖥️ **Fixed-size window** with a dark neon theme

## 📦 Download (no Python needed)

### 🪟 Windows

1. Go to the [**latest release**](https://github.com/At0mic-Samurai/At0m-Subnet-Calculator/releases/latest).
2. Download **`At0mSubnet.exe`**.
3. Double-click it. That's it.

> 💡 The first time you run it, Windows may show *"Windows protected your PC"* because the executable is not code-signed. Click **More info** → **Run anyway**.

### 🐧 Linux

1. Go to the [**latest release**](https://github.com/At0mic-Samurai/At0m-Subnet-Calculator/releases/latest).
2. Download **`At0mSubnet-Linux`**.
3. Open a terminal in the folder where you downloaded it, make it executable and run it:
   ```bash
   chmod +x At0mSubnet-Linux
   ./At0mSubnet-Linux
   ```

> 💡 It needs a graphical desktop session. The binary was built on Kali Linux and should run on recent distributions. If it doesn't work on yours, run it from source (see below).

## 🛠️ Run from source

You need **Python 3.8+** with **tkinter**:

- 🪟 **Windows:** the installer from [python.org](https://www.python.org/downloads/) already includes tkinter.
- 🐧 **Debian / Ubuntu:** install it with:
  ```bash
  sudo apt install python3-tk
  ```

Then clone the repo and run it:

```bash
git clone https://github.com/At0mic-Samurai/At0m-Subnet-Calculator.git
cd At0m-Subnet-Calculator
python at0m_subnet_calculator.py
```

> On Linux, use `python3` instead of `python`.

## 🕹️ How to use

1. Enter an **IPv4 address** (e.g. `192.168.1.10`).
2. Enter the **CIDR prefix** (e.g. `24`, a number from 0 to 32).
3. Press **CALCULATE** (or hit `Enter`).

Example for `192.168.1.10/24`:

```text
Network ID:         192.168.1.0/24
Máscara:            255.255.255.0
Máscara (binario):  11111111.11111111.11111111.00000000
Wildcard:           0.0.0.255
Broadcast:          192.168.1.255
Rango utilizable:   192.168.1.1 - 192.168.1.254
Hosts utilizables:  254
Tipo de IP:         Privada
Clase:              C
```

> 🇲🇽 The interface labels are currently in Spanish.

## 🏗️ Build your own executable

Want to package it yourself? Use [PyInstaller](https://pyinstaller.org/):

```bash
pip install pyinstaller
```

🪟 **Windows** (includes the app icon):

```bash
pyinstaller --onefile --windowed --name At0mSubnet --icon At0mSubnet.ico at0m_subnet_calculator.py
```

🐧 **Linux:**

```bash
pyinstaller --onefile --name At0mSubnet at0m_subnet_calculator.py
```

The executable will be in the `dist/` folder.

> ⚠️ PyInstaller does not cross-compile: build the Windows `.exe` on Windows and the Linux binary on Linux.

## 👤 Author

Made by **At0mic-Samurai** ⚛️⚔️
