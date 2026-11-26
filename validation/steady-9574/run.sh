#!/bin/sh
# Steadiness check for 9574: the saved check, 10 times on the last working commit and 10 times on the guilty one.
#   sh validation/steady-9574/run.sh
cd "$(dirname "$0")/../.."
for sha in 34737f4e 3889a2a0; do
  git -C clones/hunt-tiddlywiki-9574 checkout -q --force $sha
  GUMSHOE_STEADY=10 node tools/judge.ts validation/steady-9574/bug.json validation/steady-9574/runs
  echo "exit $sha $?"
done
