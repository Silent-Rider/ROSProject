#!/usr/bin/env bash
set -e

TURTLES_COUNT=${1:-3}

source /opt/ros/noetic/setup.bash
source "$HOME/catkin_ws/devel/setup.bash"
pids=()

cleanup() {
  for pid in "${pids[@]}"; do
    kill "$pid" 2>/dev/null || true
  done
}
trap cleanup EXIT INT TERM


echo "Spawning turtles..."
for ((i=2; i<=TURTLES_COUNT; i++)); do
  x=$(( (i - 1) % 10 + 1 ))
  y=$(( (i - 1) / 10 + 1 ))

  rosservice call /spawn "{x: ${x}.0, y: ${y}.0, theta: 0.0, name: 'turtle${i}'}" >/dev/null

  leader="turtle$((i-1))"
  follower="turtle${i}"

  rosrun rosproject motion.py _leader:=${leader} _follower:=${follower} &
  pids+=($!)

 # sleep 0.2
done

wait
