import os
import rclpy
from hello_interfaces.msg import MyString  # 仮定するメッセージタイプ
from rclpy.node import Node
import serial
import time

# ROS_DOMAIN_IDを設定
os.environ['ROS_DOMAIN_ID'] = '2'

class MySubscriber(Node):
  def __init__(self):
    super().__init__('serial_node')
    self.serial_port = serial.Serial('/dev/ttyACM0', 250000, timeout=70)

    self.subscription = self.create_subscription(
        MyString, "chatter", self.listener_callback, 10
    )

    if not self.serial_port.isOpen():
      self.get_logger().error('Failed to open the serial port')
      exit(1)

    self.msg = None
    self.last_send_time = time.time()

  def listener_callback(self, msg):
    self.get_logger().info(f"Subscribe {msg.data}")
    self.msg = msg
    self.send_serial_data()  # メッセージを受け取った直後にデータを送信します
    self.last_send_time = time.time()

  def send_serial_data(self):
    if self.msg is not None:
      data_to_send = self.msg.data.replace('\n', '').replace('\r', '') + '|'
      self.serial_port.write(data_to_send.encode())

def main(args=None):
  rclpy.init(args=args)
  my_subscriber = MySubscriber()

  try:
    rclpy.spin(my_subscriber)
  except KeyboardInterrupt:
    pass
  finally:
    my_subscriber.serial_port.close()
    my_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
  main()
