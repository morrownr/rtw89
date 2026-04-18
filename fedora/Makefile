# Use bash syntax, mitigates dash's printf on Debian
SHELL := /usr/bin/bash

.PHONY: all

all:
	git -C .. archive --format=tar.gz --prefix=rtw89-7.1/ HEAD > ~/rpmbuild/SOURCES/rtw89-7.1.tar.gz
	rpmbuild -ba rtw89-dkms.spec
	@printf '\nNow run sudo dnf install ~/rpmbuild/RPMS/noarch/rtw89-dkms-*.noarch.rpm\n\n'
