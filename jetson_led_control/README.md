## Jetson LED Control

Use Custom message type:
```
jetson_led_control/RGBColor 
uint8 R
uint8 G
uint8 B
```
Topic Name and Number of LEDs must be set throught nodes private params:
```
<node name="led_control_node" pkg="jetson_led_control" type="led_control_node.py" output="screen">
    <param name="LED_number" value="$(arg LED_number)" type="int"/>
    <param name="topic_name" value="$(arg topic_name)"/>
</node>
```

Follow setup guide to get started: [guide](https://docs.google.com/document/d/1HSGdoZYJhikLTxjXR2FesAU0v8keSMLYkWx0o3X5qlc/edit?usp=sharing)