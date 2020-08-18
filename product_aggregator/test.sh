#!/usr/bin/env bash

chmod 777 "$PWD/test.sh"
ln -sf "$PWD/test.sh" "$PWD/.git/hooks/pre-push"

echo '╔═══════════════════════╗'
echo '║executing pre-push hook║'
echo '╚═══════════════════════╝'

if [ -f "$PWD/venv/bin/activate" ]; then
    echo 'activating virtual environment'
    echo ''
    source "$PWD/venv/bin/activate"
fi

black --check --target-version py37 -l 120 --exclude venv .

if [ "$?" == 0 ]
then
    echo '╔════════════╗'
    echo '║black passed║'
    echo '╚════════════╝'
else
    echo '╔═══════════════════════════════════════════════════╗'
    echo '║black failed so push blocked                       ║'
    echo '║please run something like:                         ║'
    echo '║black --target-version py37 -l 120 --exclude venv .║'
    echo '╚═══════════════════════════════════════════════════╝'
    exit 1
fi

pylint app --ignore migrations

if [ "$?" == 0 ]
then
    echo '╔═════════════╗'
    echo '║pylint passed║'
    echo '╚═════════════╝'
else
    echo '╔═════════════════════════════╗'
    echo '║pylint failed so push blocked║'
    echo '╚═════════════════════════════╝'
    exit 1
fi

python manage.py check

if [ "$?" == 0 ]
then
    echo '----------------------------------------------------------------------'
    echo ''
    echo '╔═══════════════════╗'
    echo '║django check passed║'
    echo '╚═══════════════════╝'
    echo ''
else
    echo '╔═══════════════════════════════════╗'
    echo '║django check failed so push blocked║'
    echo '╚═══════════════════════════════════╝'
    exit 1
fi

python manage.py test

if [ "$?" == 0 ]
then
    echo '╔═══════════════════╗'
    echo '║django tests passed║'
    echo '╚═══════════════════╝'
else
    echo '╔═══════════════════════════════════╗'
    echo '║django tests failed so push blocked║'
    echo '╚═══════════════════════════════════╝'
    exit 1
fi
