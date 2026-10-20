<!-- codex-ros:begin -->
## ROS communication

When a user requests ROS inspection or robot control, interact directly using shell ROS commands or rclpy. Do not ask the user to relay commands that available tools can run.

- For ROS 2, source `${CODEX_HOME:-$HOME/.codex}/ros/setup.bash` in each tool shell. It selects the installed distribution and provides Fast DDS UDP transport when no custom DDS profile is already configured. ROS 1 requires its own environment; do not mix distributions.
- Preserve inherited ROS_DOMAIN_ID, RMW_IMPLEMENTATION, ROS discovery and DDS configuration. Never globally assume domain 30 or namespace robot. If the target is not found, inspect the project's launch/environment settings and relevant variables of the running ROS processes; use the target's actual domain. Ask only when the target cannot be identified from available evidence. Unset ROS_DOMAIN_ID means the ROS default domain, not proof that the robot uses that domain.
- Source the project's built workspace and dependencies as needed (ROS_WORKSPACE can select a workspace for the helper). Keep environment setup and ROS calls in the same shell. The global helper contains no project paths.
- Verify network socket access, discovery, then receipt of an actual topic message or service response. Discovery alone does not prove communication. Use bounded timeouts; for ROS 2 discovery diagnostics prefer `ros2 topic list --no-daemon --spin-time 5`. Select a known live topic, its actual type and suitable QoS for a bounded echo.
- If discovery works but data fails with Fast DDS, investigate shared memory isolation and try the installed UDP profile within the task shell. Preserve custom configuration unless a deliberate, explained diagnostic override is necessary.
- A request to move authorizes the requested movement. Before publishing, identify the correct robot, inspect fresh pose/TF and navigation readiness, and calculate relative goals from current heading. Observe the current action and final position; publishing alone is not arrival. Do not initiate motion for a communication test.
- Report actual permission or networking errors accurately. Global instructions cannot override managed sandbox policy. Do not disable collision checks or publish fabricated localization to work around failures.
<!-- codex-ros:end -->
