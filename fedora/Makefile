# Use bash syntax, mitigates dash's printf on Debian
SHELL := /usr/bin/bash

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
		git -C .. archive --format=tar --prefix=rtw89-7.1/ HEAD | tar -C "$$tmpdir" -xf - && \
		sed -i 's|$$(shell git --git-dir=$$(src)/\.git rev-parse HEAD)|'"$$commit"'|' "$$tmpdir/rtw89-7.1/Makefile" && \
		sed -i '/^CLEAN=/d' "$$tmpdir/rtw89-7.1/dkms.conf" && \
		rm -rf "$$tmpdir/rtw89-7.1/firmware" "$$tmpdir/rtw89-7.1/hostapd" "$$tmpdir/rtw89-7.1/fedora" && \
		tar -C "$$tmpdir" -czf ~/rpmbuild/SOURCES/rtw89-7.1.tar.gz rtw89-7.1
	rpmbuild -ba rtw89-dkms.spec
	@printf '\nNow run sudo dnf install ~/rpmbuild/RPMS/noarch/rtw89-dkms-*.noarch.rpm\n\n'
