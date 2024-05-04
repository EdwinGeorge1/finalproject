// ROS connection establish
ros = new ROSLIB.Ros({
   url : 'ws://localhost:9090'
 });

//  Checking connectino status
 ros.on('connection', function() {
  console.log('Connected to websocket server.');
  document.getElementById("status").innerHTML = "Connected";

});

ros.on('error', function(error) {
  console.log('Error connecting to websocket server: ', error);
  document.getElementById("status").innerHTML = "Error";

});

ros.on('close', function() {
  console.log('Connection to websocket server closed.');
  document.getElementById("status").innerHTML = "Closed";

});

// Defile all Topics

  var txt_listener = new ROSLIB.Topic({
     ros : ros,
     name : '/flag',
     messageType : 'std_msgs/String'
   });

  
  var open_start = new ROSLIB.Topic({
    ros : ros,
    name : '/start',
    messageType : 'std_msgs/String'
  });

 // Topic for move button
 button_data = new ROSLIB.Topic({
 ros: ros,
 name: "/button",
 messageType: "std_msgs/String",
});

// function for button
// the function passes the page name & button id
function buttonClick(page_id, button_id) {
 var button = new ROSLIB.Message({
   data:`{"screen_id": "${page_id}", "button": "${button_id}"}`,
 });
 button_data.publish(button); // Publishing data for getting which button pressed
}

// this fun created for testing purpose
function moveToGoal() {
  var backBtn = new ROSLIB.Message({
    data: 'Clab-tour-btn',
  });
  move.publish(backBtn);
 }


//  launch_start.subscribe(function (m) {
//   alert(m)
  
  // setTimeout(myURL, 1000);

// } );
open_start.subscribe(function(m){
  alert(m)
  console.log("hhhh")
  // alert('page')
    window.location.href = "http://localhost/clab/start.php";

    });


//   function load() {
//     setTimeout(myURL, 1000);
//     var result = document.getElementById("result");
//     result.innerHTML = `The page will load after delay of 5 seconds using setTimeout()  method.`;
//  }
// var name
//  function myURL() {
//     window.open('http://localhost/clab/start.php', name = self);
//  }