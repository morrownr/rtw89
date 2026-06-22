# Use bash syntax, mitigates dash's printf on Debian
SHELL := /usr/bin/bash

VERSION := $(shell grep '^PACKAGE_VERSION=' ../dkms.conf | cut -d'"' -f2)

REQUIRED_PKGS := rpmdevtools git-core kernel-devel-matched

.PHONY: all

all:
	@for i in $(REQUIRED_PKGS); do \
		rpm -q $$i >/dev/null || { \
			printf "Missing '%s', install with:\n\tsudo dnf install %s\n" "$$i" "$(REQUIRED_PKGS)"; \
			exit 1; \
		}; \
	done
	rpmdev-setuptree
	# /usr/src has no .git, so replace the git rev-parse call with the
	# HEAD commit hash captured now, before packing the source tarball.
	# Also strip the deprecated CLEAN directive from dkms.conf.
	commit=$$(git -C .. rev-parse HEAD) && \
	tmpdir=$$(mktemp -d) && \
		trap "rm -rf $$tmpdir" EXIT && \
		git -C .. archive --format=tar --prefix=rtw89-$(VERSION)/ HEAD | tar -C "$$tmpdir" -xf - && \
		sed -i 's|$$(shell git --git-dir=$$(src)/\.git rev-parse HEAD)|'"$$commit"'|' "$$tmpdir/rtw89-$(VERSION)/Makefile" && \
		sed -i '/^CLEAN=/d' "$$tmpdir/rtw89-$(VERSION)/dkms.conf" && \
		rm -rf "$$tmpdir/rtw89-$(VERSION)/firmware" "$$tmpdir/rtw89-$(VERSION)/hostapd" "$$tmpdir/rtw89-$(VERSION)/fedora" && \
		tar -C "$$tmpdir" -czf ~/rpmbuild/SOURCES/rtw89-$(VERSION).tar.gz rtw89-$(VERSION)
	rpmbuild -ba --define "dkms_version $(VERSION)" rtw89-dkms.spec
	@printf '\nNow run sudo dnf install ~/rpmbuild/RPMS/noarch/rtw89-dkms-*.noarch.rpm\n\n'
