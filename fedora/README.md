# RTW89 Fedora packages

Two packaging methods are provided:

| Method | Spec | Works on Kinoite/Silverblue? | Notes |
|--------|------|------------------------------|-------|
| **akmod** (recommended) | `rtw89-kmod.spec` | **Yes** | Built via `kmodtool`/`akmods`. Modules are rebuilt on the target for every kernel. |
| DKMS (legacy) | `rtw89-dkms.spec` | No | DKMS cannot install modules into the read-only `/usr` of an immutable OS. |

On immutable / rpm-ostree systems (Fedora Kinoite, Silverblue, Bluefin, ...)
DKMS does not work because it tries to copy the built `*.ko` into
`/lib/modules/<kver>/extra/`, which lives under the read-only `/usr`. The
official replacement is `akmods`, which is what the akmod package below uses.

## What the akmod packages install

| Package | Arch | Content |
|---------|------|---------|
| `akmod-rtw89` | arch | Source SRPM in `/usr/src/akmods/` + akmods trigger |
| `rtw89-kmod-common` | noarch | `/etc/modprobe.d/rtw89.conf` (blacklists + options) |
| `kmod-rtw89` | arch | Metapackage tracking the newest kernel |

On rpm-ostree, `akmod-rtw89`'s `%post` calls `akmods-ostree-post`, which builds
the modules for every deployed kernel and bakes the resulting `*.ko` into the
new ostree commit's `/usr/lib/modules/<kver>/extra/rtw89/`. On traditional
systems `akmods.service` rebuilds them on boot / kernel update instead.

## Build (in a Fedora toolbox or any Fedora host)

Install build dependencies:

```bash
sudo dnf install rpmdevtools make git-core kmodtool akmods kernel-devel-matched
```

Build the akmod packages:

```bash
make            # or: make akmod
```

The RPMs land in `~/rpmbuild/RPMS/`.

## Install on Fedora Kinoite / Silverblue (rpm-ostree)

`kernel-devel` must be layered so akmods can compile against the kernel.

```bash
sudo rpm-ostree install \
  ~/rpmbuild/RPMS/$(uname -m)/akmod-rtw89-*.$(uname -m).rpm \
  ~/rpmbuild/RPMS/noarch/rtw89-kmod-common-*.noarch.rpm \
  kernel-devel
systemctl reboot
```

After reboot, verify the modules were baked into the deployment:

```bash
ls /usr/lib/modules/$(uname -r)/extra/rtw89/
modinfo rtw89_core_git | head
# check the embedded git commit:
modinfo rtw89_core_git | grep -iE 'git|version'
```

## Install on a traditional (mutable) Fedora Workstation

```bash
sudo dnf install \
  ~/rpmbuild/RPMS/$(uname -m)/akmod-rtw89-*.$(uname -m).rpm \
  ~/rpmbuild/RPMS/noarch/rtw89-kmod-common-*.noarch.rpm
# akmods builds on next boot, or trigger it now:
sudo akmods --force
```

## Secure Boot

If Secure Boot is enabled, the akmods-signed modules need their MOK enrolled:

```bash
sudo kmodgenca -a
sudo mokutil --import /etc/pki/akmods/certs/public_key.der
# reboot and complete enrollment in the MOK manager
```

## Other build targets

```bash
make akmod      # akmod packages (default, recommended)
make kmod       # binary kmod-rtw89-<kver> for the current kernel-devel
make dkms       # legacy DKMS package (does NOT work on rpm-ostree)
```

---

The DKMS path is documented for completeness only; on Kinoite use the akmod
packages above.
