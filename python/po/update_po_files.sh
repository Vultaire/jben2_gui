#!/bin/bash

sources_list="xgettext_sources.txt"
potfile="jben.pot"
langs="en ja"

export LANG="en_US"

rm ${sources_list} ${potfile}

find ../jben -iname '*.py' > ${sources_list}
xgettext -f ${sources_list} -L python -o ${potfile}

for lang in ${langs}; do
    outfile="${lang}.po"
    if [ -e ${outfile} ]; then
        msgmerge ${outfile} ${potfile} --output-file=${outfile}.new
        mv ${outfile} ${outfile}.bak
        mv ${outfile}.new ${outfile}
    else
        msginit --locale=${lang} \
            --input=${potfile} --output-file=${outfile}
    fi
done
