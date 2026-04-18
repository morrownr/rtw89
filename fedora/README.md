# RTW89 Fedora DKMS package

This was created with the assistance of Claude Oppus 4.6.

## Summary of what was created

- [rtw89-dkms.spec](fedora/rtw89-dkms.spec).

## What the package installs:

|               Path               |                 Content                 |
|----------------------------------|-----------------------------------------|
| /usr/src/rtw89-7.1/              | 110 source files + Makefile + dkms.conf |
| /usr/lib/firmware/rtw89/*.bin    | 6 firmware binaries                     |
| /etc/modprobe.d/rtw89.conf       | blacklists + driver options             |
| /etc/modprobe.d/usb_storage.conf | USB quirks                              |

## Install

To rebuild the tarball after new commits (bump Release: in the spec too):
```
git -C .. archive --format=tar.gz --prefix=rtw89-7.1/ HEAD > ~/rpmbuild/SOURCES/rtw89-7.1.tar.gz
rpmbuild -ba rtw89-dkms.spec
sudo dnf install ~/rpmbuild/RPMS/noarch/rtw89-dkms-*.noarch.rpm
```
Verify it worked:
```
dkms status   # verify: rtw89/7.1, <kernel>: installed
```
