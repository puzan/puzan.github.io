#!/bin/bash

CONTENTDIR="./content"
EXCLUDE="images pages extra"
CATEGORIES=""

read -p "Title: " NAME

if [ -z "${NAME}" ]; then
    echo "Name is empty"
    exit 1
fi

for i in ${CONTENTDIR}/*; do
    cur_category=$(basename $i)
    if [[ "$EXCLUDE" =~ "$cur_category" ]]; then
        continue
    fi
    CATEGORIES="${CATEGORIES}${cur_category} "
done

echo "Available categories: ${CATEGORIES}"

read -p "Category: " CATEGORY

if [ -z "${CATEGORY}" ]; then
    echo "Use default linux category"
    CATEGORY=linux
fi

if ! [[ "$CATEGORIES" =~ "$CATEGORY" ]]; then
    echo "Unknown category: ${CATEGORY}"
    exit 1
fi

make newpost NAME="$NAME" CATEGORY="$CATEGORY"
