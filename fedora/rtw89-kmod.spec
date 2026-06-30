# rtw89 out-of-tree kernel modules, packaged the RPM Fusion "kmod" way so it
# works on immutable / rpm-ostree systems (Fedora Kinoite, Silverblue, ...)
# through akmods.
#
# Building this SRPM produces (by default, buildforkernels=akmod):
#   * rtw89-kmod-common  - noarch, the modprobe blacklist/options config.
#   * akmod-rtw89        - the source + akmods trigger. On rpm-ostree its %post
#                          runs akmods-ostree-post, which builds the modules for
#                          every deployed kernel and bakes the resulting *.ko
#                          into the new ostree commit's
#                          /usr/lib/modules/<kver>/extra/rtw89/. On traditional
#                          systems akmods.service rebuilds on boot / kernel
#                          update instead.
#   * kmod-rtw89         - metapackage tracking the newest kernel.
#
# Pass --define "buildforkernels current" (or "newest") to instead build a
# binary kmod-rtw89-<kver> for the kernel-devel present at build time.

%global kmod_name rtw89

# These out-of-tree modules carry no useful debuginfo for end users and the
# kmod packaging does not ship a debugsource list; disable debug packaging.
%global debug_package %{nil}

# akmod (default) | current | newest
%{!?buildforkernels: %global buildforkernels akmod}

# Upstream version (sourced from dkms.conf via fedora/Makefile --define).
%{!?kmod_version: %global kmod_version 7.2}

Name:           %{kmod_name}-kmod
Version:        %{kmod_version}
Release:        1%{?dist}
Summary:        Out-of-tree kernel modules for Realtek rtw89 WiFi chips
License:        GPL-2.0-only OR BSD-3-Clause
URL:            https://github.com/morrownr/rtw89
Source0:        %{kmod_name}-%{kmod_version}.tar.gz
Source1:        %{kmod_name}.conf

BuildRequires:  kmodtool
BuildRequires:  gcc
BuildRequires:  make
%{?AkmodsBuildRequires:BuildRequires: %{AkmodsBuildRequires}}

# When building binary kmods (buildforkernels != akmod) we target the kernels
# whose kernel-devel is installed; for akmod we must NOT pass --for-kernels.
%if "%{buildforkernels}" != "akmod"
%{!?kernels:%global kernels %(ls /usr/src/kernels 2>/dev/null)}
%endif

# Let kmodtool generate the kmod / akmod / meta subpackages and macros.
# - akmod mode: --akmod, no --for-kernels -> akmod-rtw89 + kmod-rtw89 meta.
# - otherwise : --for-kernels "<kvers>"   -> binary kmod-rtw89-<kver>.
%{expand:%(kmodtool --target %{_target_cpu} --repo %{kmod_name} --kmodname %{name} %{?kernels:--for-kernels "%{?kernels}"}%{!?kernels:--%{buildforkernels}} 2>/dev/null) }

# --- common subpackage: shared modprobe config -----------------------------
%package -n %{kmod_name}-kmod-common
Summary:        Common files for the rtw89 kernel modules
BuildArch:      noarch

%description -n %{kmod_name}-kmod-common
Shared files for the out-of-tree rtw89 kernel modules: modprobe blacklist
rules that suppress the in-kernel rtw89 driver plus default module options.

%files -n %{kmod_name}-kmod-common
%config(noreplace) %{_sysconfdir}/modprobe.d/%{kmod_name}.conf
# ---------------------------------------------------------------------------

%description
Out-of-tree kernel modules for Realtek rtw89-series WiFi adapters
(RTW8851B, RTW8852A/B/BT/C, RTW8922A and their USB/PCIe variants).

Module names carry a _git suffix (e.g. rtw89_core_git) to avoid clashing
with the in-kernel rtw89 driver. Blacklist rules in /etc/modprobe.d/ suppress
the in-kernel modules so only this driver loads.

%prep
# kmodtool sanity check (errors out via %{kmodtool_check} if any).
%{?kmodtool_check}

# Print kmodtool's view for the build log (debugging aid).
kmodtool --target %{_target_cpu} --repo %{kmod_name} --kmodname %{name} %{?kernels:--for-kernels "%{?kernels}"}%{!?kernels:--%{buildforkernels}} 2>/dev/null

# Unpack Source0 (rtw89-%{version}/...) without a top create dir clobber.
%setup -q -c -T -a 0

# kmodtool builds one tree per kernel variant in _kmod_build_<kver>.
for kernel_version in %{?kernel_versions} ; do
    cp -a %{kmod_name}-%{version} _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version in %{?kernel_versions} ; do
    make -C "${kernel_version##*___}" M="${PWD}/_kmod_build_${kernel_version%%___*}" \
        KVER="${kernel_version%%___*}" KDIR="${kernel_version##*___}" modules
done

# Number of modules the driver Makefile is expected to produce (21: core +
# per-chip + per-bus variants). Guards against silent packaging drift if the
# upstream Makefile gains/loses an obj-m target.
%global expected_modules 21

%install
for kernel_version in %{?kernel_versions} ; do
    builddir="_kmod_build_${kernel_version%%___*}"
    # Fail loudly if the build produced an unexpected module set (uncompressed
    # *.ko at this point; kmodtool's __spec_install_post does the xz later).
    n=$(find "${builddir}" -maxdepth 1 -name '*.ko' | wc -l)
    if [ "${n}" -ne "%{expected_modules}" ]; then
        echo "ERROR: built ${n} modules, expected %{expected_modules} for ${kernel_version%%___*}" >&2
        exit 1
    fi
    install -d "%{buildroot}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}"
    install -m 0755 "${builddir}"/*.ko \
        "%{buildroot}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}"
done

# In akmod mode, drop the SRPM into /usr/src/akmods/ (kmodtool macro).
%{?akmod_install}

# Common subpackage payload.
install -Dm 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/modprobe.d/%{kmod_name}.conf

%changelog
* Tue Jun 30 2026 jim60105 - 7.2-1
- Initial kmod/akmod package based on morrownr/rtw89 version 7.2.
- Works on immutable / rpm-ostree systems (Fedora Kinoite) via akmods.
