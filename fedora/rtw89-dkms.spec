%global dkms_name rtw89
%global dkms_version 7.1

Name:           %{dkms_name}-dkms
Version:        %{dkms_version}
Release:        5%{?dist}
Summary:        Out-of-tree DKMS driver for Realtek rtw89 WiFi chips
License:        GPL-2.0-only OR BSD-3-Clause
URL:            https://github.com/morrownr/rtw89
Source0:        %{dkms_name}-%{dkms_version}.tar.gz
BuildArch:      noarch

Requires:       dkms
Requires:       realtek-firmware

%description
Out-of-tree DKMS kernel modules for Realtek rtw89-series WiFi adapters
(RTW8851B, RTW8852A/B/BT/C, RTW8922A and their USB/PCIe variants).

Modules are built automatically for every installed kernel >= 6.6 via DKMS.
Module names carry a _git suffix (e.g. rtw89_core_git) to avoid clashing
with the in-kernel rtw89 driver. Blacklist rules in /etc/modprobe.d/ suppress
the in-kernel modules so only this driver loads.

%prep
%setup -q -n %{dkms_name}-%{dkms_version}

%build
# No compilation here; DKMS builds modules at kernel install time.

%check
# No check here.

%install
# 1. DKMS source tree -> /usr/src/rtw89-7.1/
install -d %{buildroot}%{_usrsrc}/%{dkms_name}-%{dkms_version}
cp -a *.c *.h Makefile dkms.conf %{buildroot}%{_usrsrc}/%{dkms_name}-%{dkms_version}/

# 2. modprobe config -> /etc/modprobe.d/
install -Dm 0644 rtw89.conf       %{buildroot}%{_sysconfdir}/modprobe.d/rtw89.conf
# usb_storage.conf is only needed for kernels < 6.17, fedora 43 and 44 use kernel-6.19+.

%post
# Register with DKMS; --rpm_safe_upgrade removes old version on upgrade:
dkms add -m %{dkms_name} -v %{dkms_version} --rpm_safe_upgrade || :
# Rebuild and make available for the currently running kernel:
dkms build -m %{dkms_name} -v %{dkms_version} -q --force
dkms install -m %{dkms_name} -v %{dkms_version} -q --force

%preun
dkms remove -m %{dkms_name} -v %{dkms_version} -q --all --rpm_safe_upgrade

%files
%dir %{_usrsrc}/%{dkms_name}-%{dkms_version}
%{_usrsrc}/%{dkms_name}-%{dkms_version}/*.c
%{_usrsrc}/%{dkms_name}-%{dkms_version}/*.h
%{_usrsrc}/%{dkms_name}-%{dkms_version}/Makefile
%{_usrsrc}/%{dkms_name}-%{dkms_version}/dkms.conf
%config(noreplace) %{_sysconfdir}/modprobe.d/rtw89.conf

%changelog
* Tue Apr 21 2026 Doncho Nikolaev Gunchev <dgunchev@gmail.com> - 7.1-5
- Initial package based on morrownr/rtw89 version 7.1
