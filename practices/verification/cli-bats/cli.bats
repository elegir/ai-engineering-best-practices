#!/usr/bin/env bats
# bats-core: tests for shell scripts / CLIs. Install: npm i -D bats  (or apt/brew install bats)
# Run: npx bats test/cli.bats
#
# Make scripts testable: put the main logic in run_main() and guard the call:
#   if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then run_main "$@"; fi
# so bats can `source` the script and test functions individually.

setup() {
  export DRY_RUN=1                               # scripts with side effects must honor this
  export TMPWORK="$(mktemp -d)"
  source "<<scripts/fleet.sh>>"
}

teardown() { rm -rf "$TMPWORK"; }

@test "help exits 0 and prints usage" {
  run bash "<<scripts/fleet.sh>>" --help
  [ "$status" -eq 0 ]
  [[ "$output" == *"Usage"* ]]
}

@test "refuses to run against production without --confirm" {
  run bash "<<scripts/fleet.sh>>" deploy --env production
  [ "$status" -ne 0 ]
  [[ "$output" == *"--confirm"* ]]
}

@test "dry run lists actions and changes nothing" {
  run bash "<<scripts/fleet.sh>>" sync --site example.test
  [ "$status" -eq 0 ]
  [[ "$output" == *"DRY RUN"* ]]
  [ -z "$(ls -A "$TMPWORK")" ]
}

@test "unit: <<parse_site_list>> handles blank lines and comments" {
  printf 'a.test\n\n# comment\nb.test\n' > "$TMPWORK/sites.txt"
  run parse_site_list "$TMPWORK/sites.txt"
  [ "$status" -eq 0 ]
  [ "${lines[0]}" = "a.test" ]
  [ "${lines[1]}" = "b.test" ]
}
