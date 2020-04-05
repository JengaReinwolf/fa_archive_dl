#!/bin/sh

echo "Setting up environment"
if ! /srv/fa_archive_dl/env_setup.py; then
    exit $?
fi
echo "Setting up Tor"
/usr/bin/tor --quiet &
/srv/fa_archive_dl/fa_archive_dl.py $@
exit $?
