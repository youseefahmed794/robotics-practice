import rclpy
from std_msgs.msg import Float64
from motion_control.motion_decision import decide_motion

def main():
    rclpy.init()
    node = rclpy.create_node("distance_listener")
    def on_distance(msg):
        distance = msg.data
        decision = decide_motion(distance)
        node.get_logger().info(f"Distance: {distance} m -> {decision}")

    node.create_subscription(Float64, "/distance", on_distance, 10)
    node.get_logger().info("Node started")


    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()