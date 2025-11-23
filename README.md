## The Mission of this Repo:

To code, test and upstream great quality Linux Standards compliant (mac80211) USB WiFi drivers for the Realtek RTW89 driver series.

## Compatibility

Compatible with **Linux kernel versions 6.6 and newer** as long as your distro hasn't modified any kernel APIs. RHEL and all distros based on RHEL will have modified kernel APIs and are unlikely to be compatible with this driver.

#### Supported chips
- **USB** : RTL8831BU, RTL8851BU, RTL8832AU, RTL8852AU, RTL8832BU, RTL8852BU
- **USB** : RTL8832CU, RTL8852CU, RTL8912AU, RTL8922AU (no MLO yet)
- **PCIe**: RTL8851BE, RTL8852AE, RTL8852BE(-VS, -VT), RTL8852CE, RTL8922AE(-VS)

Note: If you own a USB WiFi adapter with any of the above supported
chips and your adapter is single-state (no Windows driver on board) and
single-function (no bluetooth support), please start an issue and post
the brand, name and chip of your adapter as well as a link to the 
product. This will allow us to make a list of preferred adapters.

## Prerequisites

git, make, gcc, kernel-headers, dkms and mokutil (dkms and mokutil are optional.)

## Installation Guide

1. Create a clone of this repo in your local machine

   ```
   git clone https://github.com/morrownr/rtw89
   ```

2. Change the working directory to rtw89

   ```
   cd rtw89
   ```

3. Search and remove previously installed out-of-kernel rtw89 drivers. If your system has [Larry's rtw89 driver](https://github.com/lwfinger/rtw89) installed, you must run this command to remove it, or this driver won't work as expected.

   ```
   sudo make cleanup_target_system
   ```

3. Build and install the driver

   * _via dkms (Recommended especially if Secure Boot is enabled in your system)_

     ```
     sudo dkms install $PWD
     ```

   * _via make_ 

     ```
     make clean modules && sudo make install
     ```

4. Install the firmware necessary for the driver

   ```
   sudo make install_fw
   ```

5. Copy the configuration file `rtw89.conf` to /etc/modprobe.d/
   ```
   sudo cp -v rtw89.conf /etc/modprobe.d/
   ```
   
   Note: The above step will blacklist in-kernel drivers that can conflict with drivers in this repo.

6. Enroll the MOK (Machine Owner Key). This is needed **ONLY IF** [Secure Boot](https://wiki.debian.org/SecureBoot) is enabled in your system. Please see [this guide](https://github.com/dell/dkms?tab=readme-ov-file#secure-boot) for details.

   ```
   sudo mokutil --import /var/lib/dkms/mok.pub
   ```

   For Ubuntu-based distro users, run this command instead.

   ```
   sudo mokutil --import /var/lib/shim-signed/mok/MOK.der
   ```

## Uninstallation Guide

For users who installed the driver via `DKMS`,

1. Check the version of the rtw89 driver installed in your system.
```
sudo dkms status rtw89
```

2. Remove the rtw89 driver and its source code (Change the driver version accordingly)
```
sudo dkms remove rtw89/6.15 --all
```
```
sudo rm -rf /usr/src/rtw89-6.15
```

3. Remove the configuration file
```
sudo rm -f /etc/modprobe.d/rtw89.conf
```

For users who installed the driver via `make`, run these commands in the rtw89 source directory
```
sudo make uninstall
```
```
sudo rm -f /etc/modprobe.d/rtw89.conf
```

## Q&A

### Q1. Bluetooth is still not working after installing this driver, why?

   The `rtw89` driver is the **Wi-Fi** driver for Realtek Wi-Fi 6/7 adapters and has nothing to do with Bluetooth.

### Q2. How to update the driver installed via DKMS?

   1. Check the version of the rtw89 driver installed in your system.
      ```
      sudo dkms status rtw89
      ```   
   2. Remove the rtw89 driver. (Change the driver version accordingly)
      ```
      sudo dkms remove rtw89/6.15 --all
      ```
      ```
      sudo rm -rf /usr/src/rtw89-6.15/
      ```

   3. Run this command in the rtw89 source directory to pull the latest code
      ```
      git pull
      ```

   4. Build, sign and install the rtw89 driver from the latest code.
      ```
      sudo dkms install $PWD
      ```

### Q3. How to update the driver installed via `make`?

   1. Run this command in the rtw89 source directory to pull the latest code
      ```
       git pull
      ```
  
   2. Rebuild and reinstall the driver from the latest code
      ```
      make clean modules && sudo make install
      ```

### Q4. How to update the firmware in my system?

   1. Run this command in the rtw89 source directory to pull the latest code and firmware
      ```
      git pull
      ```

   2. Update the firmware files in your system
      ```
      sudo make install_fw
      ```

### Q5. I see my USB Wi-Fi adapter is in Driver CDROM Mode when running `lsusb`, what should I do?

Install `usb-modeswitch` (or usb_modeswitch), a tool that can switch your adapter to Wi-Fi mode.


### Q6. My computer takes a very long time to boot when the Wi-Fi dongle is pre-inserted, how to fix it?

   1. Copy [usb_storage.conf](https://github.com/morrownr/rtw89/blob/main/usb_storage.conf) to `/etc/modprobe.d/`. This file will tell the culprit `usb_storage` not to touch the Wi-Fi dongles.
      ```
      sudo cp usb_storage.conf /etc/modprobe.d/
      ```

   2. Regenerate initramfs images. The following command is only applicable to Debian/Ubuntu and their variants. Please consult the manual if you are running other distros.
      ```
      sudo update-initramfs -u -k all
      ```

## The Main Menu for this site contains a lot of information regarding USB WiFi Adapters

https://github.com/morrownr/USB-WiFi
