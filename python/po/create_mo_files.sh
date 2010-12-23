#!/bin/sh

export LANG="en_US"

for pofile in *.po; do
    outfile=${pofile%.po}.mo
    msgfmt ${pofile} --output-file=${outfile}
done
