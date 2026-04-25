# RTW89 Fedora DKMS package

This was created with the assistance of Claude Opus 4.6.

## Summary of what was created

- [rtw89-dkms.spec](rtw89-dkms.spec).

## What the package installs:

| Path                       | Content                                 |
|----------------------------|-----------------------------------------|
| /usr/src/rtw89-7.1/        | 102 source files + Makefile + dkms.conf |
| /etc/modprobe.d/rtw89.conf | blacklists + driver options             |

## Install

First install the dependencies to build the rpm package:

```bash
sudo dnf install rpmdevtools make git-core kernel-devel-matched
```

Then (re)build the package:

```bash
rm -fv ~/rpmbuild/RPMS/noarch/rtw89-dkms-*.noarch.rpm ~/rpmbuild/SRPMS/rtw89-dkms-*.src.rpm
make
sudo dnf install ~/rpmbuild/RPMS/noarch/rtw89-dkms-*.noarch.rpm
```

Verify it worked:

```bash
dkms status   # verify: rtw89/7.1, $(uname -r), $(uname -m): installed
```

Check if the git commit got embedded properly:

```bash
xzcat /usr/lib/modules/$(uname -r)/extra/rtw89_core_git.ko.xz | grep -a "git commit"
```
