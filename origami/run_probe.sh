#!/bin/bash
# Run the bridge probe using Isaac Sim's interpreter (it has the bundled rclpy).
set -e
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$HERE/isaac_env.sh"
exec "$ISAAC_SIM/python.sh" "$HERE/isaac_probe.py" "$@"
