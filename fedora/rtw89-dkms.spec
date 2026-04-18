# git -C .. archive --format=tar.gz --prefix=rtw89-7.1/ HEAD > ~/rpmbuild/SOURCES/rtw89-7.1.tar.gz
# rpmbuild -ba rtw89-dkms.spec

%global dkms_name    rtw89
%global dkms_version 7.1

Name:           %{dkms_name}-dkms
Version:        %{dkms_version}
Release:        2%{?dist}
Summary:        Out-of-tree DKMS driver for Realtek rtw89 WiFi chips
License:        GPL-2.0-only OR BSD-3-Clause
URL:            https://github.com/morrownr/rtw89
Source0:        %{dkms_name}-%{dkms_version}.tar.gz
BuildArch:      noarch

BuildRequires:  sed

Requires:       dkms
Requires:       kernel-devel
Requires:       gcc
Requires:       make
Recommends:     realtek-firmware

%description
Out-of-tree DKMS kernel modules for Realtek rtw89-series WiFi adapters
(RTW8851B, RTW8852A/B/BT/C, RTW8922A and their USB/PCIe variants).

Modules are built automatically for every installed kernel >= 6.6 via DKMS.
Module names carry a _git suffix (e.g. rtw89_core_git) to avoid clashing
with the in-kernel rtw89 driver. Blacklist rules in /etc/modprobe.d/ suppress
the in-kernel modules so only this driver loads.

%prep
%setup -q -n %{dkms_name}-%{dkms_version}
# Fix GIT_COMMIT: /usr/src has no .git; replace the git rev-parse call with
# the static package version string so the DKMS build does not fail.
sed -i \
    's|$(shell git --git-dir=$(src)/\.git rev-parse HEAD)|%{dkms_version}|' \
    Makefile

%build
# No compilation here; DKMS builds modules at kernel install time.

%install
# 1. DKMS source tree -> /usr/src/rtw89-7.1/
install -d %{buildroot}%{_usrsrc}/%{dkms_name}-%{dkms_version}
cp -a *.c *.h Makefile dkms.conf %{buildroot}%{_usrsrc}/%{dkms_name}-%{dkms_version}/

# 2. Firmware -> /usr/lib/firmware/rtw89/
install -d %{buildroot}/usr/lib/firmware/rtw89
install -m 0644 firmware/*.bin %{buildroot}/usr/lib/firmware/rtw89/

# 3. License file
install -Dm 0644 firmware/LICENCE.rtlwifi_firmware.txt \
    %{buildroot}%{_licensedir}/%{name}/LICENCE.rtlwifi_firmware.txt

# 4. modprobe config -> /etc/modprobe.d/
install -Dm 0644 rtw89.conf       %{buildroot}%{_sysconfdir}/modprobe.d/rtw89.conf
install -Dm 0644 usb_storage.conf %{buildroot}%{_sysconfdir}/modprobe.d/usb_storage.conf

%post
# Register with DKMS; --rpm_safe_upgrade removes old version on upgrade.
dkms add --rpm_safe_upgrade -m %{dkms_name} -v %{dkms_version} &>/dev/null || :
dkms autoinstall -m %{dkms_name} -v %{dkms_version} &>/dev/null || :

%preun
# Only deregister on final removal ($1==0), not on upgrade ($1==1).
if [ "$1" -eq 0 ]; then
    dkms remove --rpm_safe_upgrade -m %{dkms_name} -v %{dkms_version} --all &>/dev/null || :
fi

%files
%license %{_licensedir}/%{name}/LICENCE.rtlwifi_firmware.txt
%dir %{_usrsrc}/%{dkms_name}-%{dkms_version}
%{_usrsrc}/%{dkms_name}-%{dkms_version}/*.c
%{_usrsrc}/%{dkms_name}-%{dkms_version}/*.h
%{_usrsrc}/%{dkms_name}-%{dkms_version}/Makefile
%{_usrsrc}/%{dkms_name}-%{dkms_version}/dkms.conf
%{_prefix}/lib/firmware/rtw89/*.bin
%config(noreplace) %{_sysconfdir}/modprobe.d/rtw89.conf
%config(noreplace) %{_sysconfdir}/modprobe.d/usb_storage.conf

%changelog
* Sat Apr 18 2026 Doncho Gunchev <dgunchev@gmail.com> - 7.1-2
- Cleanup, simplify.

* Fri Apr 17 2026 Claude Opus <claude@claude.ai> - 7.1-1
- Initial package based on morrownr/rtw89 version 7.1
