# rtw89

### Supported chips
RTL8851BE, RTL8852AE, RTL8852BE, RTL8852CE and RTL8922AE

### Prerequisites

git, make, gcc, kernel-headers, dkms and mokutil (dkms and mokutil are optional)

### Installation Guide

1. Create a clone of this repo in your local machine

   ```git clone https://github.com/a5a5aa555oo/rtw89```

2. Change the working directory to rtw89

   ```cd rtw89```

3. Search and remove other out-of-tree rtw89 drivers. If your system has [Larry's rtw89 driver](https://github.com/lwfinger/rtw89) installed, you must run this command to remove it, or this driver won't work as expected.

   ```sudo make cleanup_target_system```

4. Build and install the driver

   * _via dkms (Recommended especially Secure Boot is enabled on your system)_

     ```sudo dkms install $PWD```

   * _via make_

     ```make clean modules && sudo make install```

5. Install the firmware needed for the driver

   ```sudo make install_fw```


6. Enroll the MOK (Machine Owner Key). This is needed if [Secure Boot](https://wiki.debian.org/SecureBoot) is enabled on your system. Please see [the guides](https://www.google.com/search?q=mokutil+how+to+enroll+mok) on Internet for details.

   ```sudo mokutil --import /var/lib/dkms/mok.pub```

### Note

Kernel 6.6 ~ 6.14 are supported. For kernel 5.15 ~ 6.5 users, use the rtw89 driver in [6.6-lts branch](https://github.com/a5a5aa555oo/rtw89/tree/6.6-lts) instead.

Tested with RTL8852BE on Arch Linux (kernel version: 6.6.83-1-lts66 / 6.12.19-1-lts) and it works.
