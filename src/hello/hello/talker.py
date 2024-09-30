import rclpy
from hello_interfaces.msg import MyString
from rclpy.node import Node
from pyPS4Controller.controller import Controller
import os
import subprocess
# os.environ['ROS_DOMAIN_ID'] = '2'

class MyController(Controller, Node):
  def __init__(self, **kwargs):
    Controller.__init__(self, **kwargs)
    Node.__init__(self, 'ps4_controller_node')
    self.publisher_ = self.create_publisher(MyString, 'chatter', 1)
    self.timer = self.create_timer(0.01, self.timer_callback)

  def timer_callback(self):
    self.listen(timeout=5)

  def on_playstation_button_press(self):
    msg = MyString()
    msg.data = "psON"
    self.publisher_.publish(msg)
    self.get_logger().info("Published: " + msg.data)

  def on_playstation_button_release(self):
    msg = MyString()
    msg.data = "psOFF"
    self.publisher_.publish(msg)
    self.get_logger().info("Published: " + msg.data)

  # オムニ停止
  def on_x_press(self):
    msg = MyString()
    msg.data = "cross"
    self.publisher_.publish(msg)
    self.get_logger().info("Published: " + msg.data)

  
  # id wo kimeru  
  # def change_id(self, domain_id):
  #   subprocess.run(
  #       f"export ROS_DOMAIN_ID={domain_id} && ros2 run hello talker", shell=True)
  #   # self.get_logger().info(f"ROS_DOMAIN_ID={id}")

  def on_right_arrow_press(self):
    self.get_logger().info("finish")
    subprocess.run(
        "export ROS_DOMAIN_ID=1 && ros2 run hello talker", shell=True)

  def on_up_arrow_press(self):
    self.get_logger().info("finish")
    subprocess.run(
        "export ROS_DOMAIN_ID=2 && ros2 run hello talker", shell=True)
  
  def on_left_arrow_press(self):
    self.get_logger().info("finish")
    subprocess.run(
        "export ROS_DOMAIN_ID=3 && ros2 run hello talker", shell=True)
    
  # def on_down_arrow_press(self):
  
  # ジャンプ機構
  def on_L1_press(self):
    msg = MyString()
    msg.data = "L1ON"
    for _ in range(3):
      self.publisher_.publish(msg)
    self.get_logger().info("Published: " + msg.data)

  def on_L1_release(self):
    msg = MyString()
    msg.data = "L1OFF"
    for _ in range(3):
      self.publisher_.publish(msg)
    self.get_logger().info("Published: " + msg.data)

  def on_R1_press(self):
    msg = MyString()
    msg.data = "R1ON"
    for _ in range(3):
      self.publisher_.publish(msg)
    self.get_logger().info("Published: " + msg.data)

  def on_R1_release(self):
    msg = MyString()
    msg.data = "R1OFF"
    for _ in range(3):
      self.publisher_.publish(msg)
    self.get_logger().info("Published: " + msg.data)

  # 三輪オムニの制御
  def on_R3_left(self, value):
    if -3000 < value < 3000:
      value = 0
    msg = MyString()
    msg.data = f"R3_x: {value}"
    self.publisher_.publish(msg)
    self.get_logger().info("Published: R3_x: " + str(value))

  def on_R3_right(self, value):
    if -3000 < value < 3000:
      value = 0
    msg = MyString()
    msg.data = f"R3_x: {value}"
    self.publisher_.publish(msg)
    self.get_logger().info("Published: R3_x: " + str(value))

  def on_R3_up(self, value):
    if -3000 < value < 3000:
      value = 0
    msg = MyString()
    msg.data = f"R3_y: {value}"
    self.publisher_.publish(msg)
    self.get_logger().info("Published: R3_y: " + str(value))

  def on_R3_down(self, value):
    if -3000 < value < 3000:
      value = 0
    msg = MyString()
    msg.data = f"R3_y: {value}"
    self.publisher_.publish(msg)
    self.get_logger().info("Published: R3_y: " + str(value))

  def on_L3_left(self, value):
    if -3000 < value < 3000:
      value = 0
    msg = MyString()
    msg.data = f"L3_x: {value}"
    self.publisher_.publish(msg)
    self.get_logger().info("Published: L3_x: " + str(value))

  def on_L3_right(self, value):
    if -3000 < value < 3000:
      value = 0
    msg = MyString()
    msg.data = f"L3_x: {value}"
    self.publisher_.publish(msg)
    self.get_logger().info("Published: L3_x: " + str(value))

  def on_L3_up(self, value):
    if -3000 < value < 3000:
      value = 0
    msg = MyString()
    msg.data = f"L3_y: {-value}"
    self.publisher_.publish(msg)
    self.get_logger().info("Published: L3_y: " + str(-value))

  def on_L3_down(self, value):
    if -3000 < value < 3000:
      value = 0
    msg = MyString()
    msg.data = f"L3_y: {-value}"
    self.publisher_.publish(msg)
    self.get_logger().info("Published: L3_y: " + str(-value))

def main(args=None):
  rclpy.init(args=args)
  controller = MyController(interface="/dev/input/js0",
                            connecting_using_ds4drv=False)
  rclpy.spin(controller)  # コントローラーとROS2ノードを同時に実行

  # コントローラが停止したら、ノードを破棄してROS通信をシャットダウンする
  controller.destroy_node()
  rclpy.shutdown()

if __name__ == "__main__":
  main()
