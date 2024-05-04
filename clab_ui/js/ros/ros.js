ros = new ROSLIB.Ros({
  url : 'ws://localhost:9090'
});


ros.on('connection', function() {
  console.log('Connected to websocket server.');
});

ros.on('error', function(error) {
  console.log('Error connecting to websocket server: ', error);
});

ros.on('close', function() {
  console.log('Connection to websocket server closed.');
});


// Defile all Topics

 var txt_listener = new ROSLIB.Topic({
    ros : ros,
    name : '/flag',
    messageType : 'std_msgs/String'
  });

 
 var launch_start = new ROSLIB.Topic({
  
   ros : ros,
   name : "/start",
   messageType : 'std_msgs/String'
 });

// Topic for Button Feadback 
button_data = new ROSLIB.Topic({
ros: ros,
name: "/button",
messageType: "std_msgs/String",
});

// function for button
// the function passes the page name & button id
function buttonClick(page_id, button_id) {
  console.log("button click fun")
var button = new ROSLIB.Message({
  data:`{"screen_id": "${page_id}", "button": "${button_id}"}`,
});
try {
<<<<<<< HEAD
  console.log("hello")
=======
//   console.log(""data)
>>>>>>> f62a1eb99d2e8a8216c54b381cf9b88dd753edef
  // code to be executed
  button_data.publish(button); // Publishing data for getting which button pressed

 } catch (error) {
   console.error(error);
}
// move.publish(button); // Publishing data for getting which button pressed
}

 // for calling start.php file
launch_start.subscribe(function(){
  console.log("opened start.php page")
  // alert(m)
    window.location.href = "http://localhost/clab/start.php";

    });



