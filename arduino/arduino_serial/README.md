# arduino_serial

* Consists of a ROS node and an arduino sketch.
* The ROS node will publish voltage read by the arduino and send WS2812b LED commands to the arduino.
    ```
    arduino_serial/RGBColor 
        uint8 R
        uint8 G
        uint8 B
        uint16 T
    ```
* Flash the arduino sketch and run the ROS node with the arduino connected via serial USB.
* Dont forget to set port and baud rate in the launch file.
* If changing baud rate then make changes to the arduino sketch as well.
* recommended usage:
    Include `serial_node.launch` in your own launch file:
    ```
    <include file=$(find arduino_serial)/launch/serial_node.launch>
        <arg name="port" value="/dev/ttyACM0"/>
        <arg name="baud" value="9600"/>
        <arg name="battery_voltage_topic" value="/battery_voltage"/>
        <arg name="led_control_topic" value="/led_control"/>
    </include>
    ``` 
    **OR**
    Include the launch command for the node in your own launch file:
    ```
    <node name="serial_node" pkg="arduino_serial" type="serial_node" output="screen">
        <param name="port" value="<>"/>
        <param name="baud" value="<>"/>
        <remap from="/battery_voltage" to="<>"/>
        <remap from="/led_control" to="<>"/>
    </node>
    ```

* **Note**: This doesnt use rosserial_arduino. 