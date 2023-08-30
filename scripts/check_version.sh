#!/usr/bin/bash

if [ -n "$(git branch | grep '* main')" ]
then
    # no need to check version increment if this is being run on main branch
    exit 0
fi

get_version() {
    local VERSION=$(grep '^version = "[[:digit:]]\+.[[:digit:]]\+.[[:digit:]]\+"$' pyproject.toml)
    VERSION=$(echo $VERSION | cut -d'"' -f2)
    echo $VERSION
}

THIS_BRANCH_VERSION=$(get_version)

cd ..
git clone -b main --single-branch https://github.com/chessticulate/tictactoe.git tictactoe_main > /dev/null
cd tictactoe_main

MAIN_BRANCH_VERSION=$(get_version)

# mini python script to compare versions
python -c "from sys import argv, exit;from pkg_resources import parse_version;exit(0) if parse_version(argv[1]) < parse_version(argv[2]) else exit(1)" \
$MAIN_BRANCH_VERSION $THIS_BRANCH_VERSION

EXIT_CODE=$?

if [ "$EXIT_CODE" != "0" ]
then
    echo "'${THIS_BRANCH_VERSION}' not greater than '${MAIN_BRANCH_VERSION}'"
fi

exit $EXIT_CODE
