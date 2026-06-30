# Use bash syntax, mitigates dash's printf on Debian
SHELL := /usr/bin/bash

VERSION := $(shell grep '^PACKAGE_VERSION=' ../dkms.conf | cut -d'"' -f2)

# Common build tooling.
REQUIRED_PKGS     := rpmdevtools git-core
# DKMS path additionally needs a matched kernel-devel; the akmod/kmod path
# needs kmodtool + akmods (and kernel-devel only when building binary kmods).
DKMS_REQUIRED_PKGS  := $(REQUIRED_PKGS) kernel-devel-matched
KMOD_REQUIRED_PKGS  := $(REQUIRED_PKGS) kmodtool akmods kernel-devel-matched

.PHONY: all akmod kmod dkms tarball check-kmod-deps check-dkms-deps

# Default target builds the akmod package, which is what works on immutable /
# rpm-ostree systems (Fedora Kinoite, Silverblue, ...).
all: akmod

# ---------------------------------------------------------------------------
# Shared: build the source tarball into ~/rpmbuild/SOURCES/.
#
# /usr/src has no .git, so replace the git rev-parse call in the driver
# Makefile with the HEAD commit hash captured now, before packing the tarball.
# Also strip the deprecated CLEAN directive from dkms.conf.
# ---------------------------------------------------------------------------
tarball:
	rpmdev-setuptree
	commit=$$(git -C .. rev-parse HEAD) && \
	tmpdir=$$(mktemp -d) && \
		trap "rm -rf $$tmpdir" EXIT && \
		git -C .. archive --format=tar --prefix=rtw89-$(VERSION)/ HEAD | tar -C "$$tmpdir" -xf - && \
		sed -i 's|$$(shell git --git-dir=$$(src)/\.git rev-parse HEAD)|'"$$commit"'|' "$$tmpdir/rtw89-$(VERSION)/Makefile" && \
		sed -i '/^CLEAN=/d' "$$tmpdir/rtw89-$(VERSION)/dkms.conf" && \
		rm -rf "$$tmpdir/rtw89-$(VERSION)/firmware" "$$tmpdir/rtw89-$(VERSION)/hostapd" "$$tmpdir/rtw89-$(VERSION)/fedora" && \
		tar -C "$$tmpdir" -czf ~/rpmbuild/SOURCES/rtw89-$(VERSION).tar.gz rtw89-$(VERSION)
	# Extra sources referenced by the specs (rtw89-kmod.spec Source1).
	cp -f ../rtw89.conf ~/rpmbuild/SOURCES/

check-kmod-deps:
	@for i in $(KMOD_REQUIRED_PKGS); do \
		rpm -q $$i >/dev/null || { \
			printf "Missing '%s', install with:\n\tsudo dnf install %s\n" "$$i" "$(KMOD_REQUIRED_PKGS)"; \
			exit 1; \
		}; \
	done

check-dkms-deps:
	@for i in $(DKMS_REQUIRED_PKGS); do \
		rpm -q $$i >/dev/null || { \
			printf "Missing '%s', install with:\n\tsudo dnf install %s\n" "$$i" "$(DKMS_REQUIRED_PKGS)"; \
			exit 1; \
		}; \
	done

# ---------------------------------------------------------------------------
# akmod: recommended for Fedora Kinoite / Silverblue. Produces noarch
# rtw89-kmod-common + akmod-rtw89 (+ kmod-rtw89 meta). Modules build on the
# target via akmods (ostree %post or akmods.service).
# ---------------------------------------------------------------------------
akmod: check-kmod-deps tarball
	# The akmod %install re-runs rpmbuild -bs against %{_specdir}/%{name}.spec,
	# so the spec must live in ~/rpmbuild/SPECS/.
	cp -f rtw89-kmod.spec ~/rpmbuild/SPECS/
	rpmbuild -ba \
		--define "kmod_version $(VERSION)" \
		--define "buildforkernels akmod" \
		~/rpmbuild/SPECS/rtw89-kmod.spec
	@printf '\nBuilt akmod packages in ~/rpmbuild/RPMS/.\n'
	@printf 'On Fedora Kinoite install with:\n'
	@printf '\tsudo rpm-ostree install \\\n'
	@printf '\t  ~/rpmbuild/RPMS/$(shell uname -m)/akmod-rtw89-*.$(shell uname -m).rpm \\\n'
	@printf '\t  ~/rpmbuild/RPMS/noarch/rtw89-kmod-common-*.noarch.rpm \\\n'
	@printf '\t  kernel-devel\n'
	@printf 'then reboot.\n\n'

# ---------------------------------------------------------------------------
# kmod: build a binary kmod-rtw89-<kver> for the kernel-devel present now.
# Tied to one kernel version; useful for traditional (mutable) systems.
# ---------------------------------------------------------------------------
kmod: check-kmod-deps tarball
	rpmbuild -ba \
		--define "kmod_version $(VERSION)" \
		--define "buildforkernels current" \
		rtw89-kmod.spec
	@printf '\nBuilt binary kmod packages in ~/rpmbuild/RPMS/$(shell uname -m)/.\n\n'

# ---------------------------------------------------------------------------
# dkms: legacy DKMS package. NOTE: does not work on immutable / rpm-ostree
# systems because DKMS cannot install modules into the read-only /usr.
# ---------------------------------------------------------------------------
dkms: check-dkms-deps tarball
	rpmbuild -ba --define "dkms_version $(VERSION)" rtw89-dkms.spec
	@printf '\nNow run sudo dnf install ~/rpmbuild/RPMS/noarch/rtw89-dkms-*.noarch.rpm\n\n'
