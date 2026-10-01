#!/usr/bin/env bash
# Stop hook: the agent may not finish while the fast test subset is red.
# Guards against infinite loops with stop_hook_active.

INPUT="$(cat)"
if printf '%s' "$INPUT" | grep -q '"stop_hook_active"[[:space:]]*:[[:space:]]*true'; then
  exit 0   # we already ran once for this stop; let it end
fi

# Keep this FAST (< ~60 s). Full suites belong in CI.
TEST_CMD="<<npm test -- --silent>>"          # Node example
# TEST_CMD="<<pytest -q -x tests/unit>>"     # Python example
# TEST_CMD="<<vendor/bin/phpunit --testsuite unit>>"  # PHP example

OUT="$(eval "$TEST_CMD" 2>&1)"
STATUS=$?
if [ $STATUS -ne 0 ]; then
  TAIL="$(printf '%s' "$OUT" | tail -n 40 | sed 's/\\/\\\\/g; s/"/\\"/g' | awk '{printf "%s\\n", $0}')"
  cat <<EOF
{"decision":"block","reason":"Tests are failing; you cannot declare the task done. Fix them, then stop again. Last lines:\n$TAIL"}
EOF
  exit 0
fi
exit 0
