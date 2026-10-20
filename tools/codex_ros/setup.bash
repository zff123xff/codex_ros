#!/usr/bin/env bash
# Source from Bash. Preserve the caller's ROS domain and middleware settings.
_codex_ros_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -n "${ROS_DISTRO:-}" ]]; then
    _codex_ros_setup="/opt/ros/$ROS_DISTRO/setup.bash"
else
    _codex_ros_options=(/opt/ros/*/setup.bash)
    if [[ ${#_codex_ros_options[@]} != 1 || ! -r "${_codex_ros_options[0]}" ]]; then
        echo 'Select an installed ROS distribution with ROS_DISTRO before sourcing setup.bash.' >&2
        return 1
    fi
    _codex_ros_setup="${_codex_ros_options[0]}"
fi
if [[ ! -r "$_codex_ros_setup" ]]; then
    echo "ROS setup missing: $_codex_ros_setup" >&2
    return 1
fi
source "$_codex_ros_setup" || return
# Optional workspace, supplied by the agent after inspecting the current project.
if [[ -n "${ROS_WORKSPACE:-}" ]]; then
    if [[ ! -r "$ROS_WORKSPACE/install/setup.bash" ]]; then
        echo "Workspace setup missing: $ROS_WORKSPACE/install/setup.bash" >&2
        return 1
    fi
    source "$ROS_WORKSPACE/install/setup.bash" || return
fi
if [[ -z "${RMW_IMPLEMENTATION:-}" || "$RMW_IMPLEMENTATION" == rmw_fastrtps_cpp ]]; then
    if [[ -z "${FASTRTPS_DEFAULT_PROFILES_FILE:-}" && -z "${FASTDDS_DEFAULT_PROFILES_FILE:-}" ]]; then
        export FASTRTPS_DEFAULT_PROFILES_FILE="$_codex_ros_dir/fastdds_udp.xml"
        export FASTDDS_DEFAULT_PROFILES_FILE="$FASTRTPS_DEFAULT_PROFILES_FILE"
    fi
fi
export ROS_LOG_DIR="${ROS_LOG_DIR:-/tmp/codex-ros-$(id -u)}"
mkdir -p "$ROS_LOG_DIR" || return
unset _codex_ros_dir _codex_ros_setup _codex_ros_options
