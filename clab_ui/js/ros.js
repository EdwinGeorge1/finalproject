var ros = new ROSLIB.Ros({
   url : 'ws://localhost:9090'
 });

 ros.on('connection', function() {
   document.getElementById("status").innerHTML = "Connected";
 });

 ros.on('error', function(error) {
   document.getElementById("status").innerHTML = "Error";
 });

 ros.on('close', function() {
   document.getElementById("status").innerHTML = "Closed";
 });

 var txt_listener = new ROSLIB.Topic({
   ros : ros,
   name : '/button',
   messageType : 'std_msgs/String'
 });

 txt_listener.subscribe(function(m) {
   document.getElementById("msg").innerHTML = m.data;
 });

 // Topic for button
 move = new ROSLIB.Topic({
 ros: ros,
 name: "/button",
 messageType: "std_msgs/String",
});

// function for button
// the function passes the page name & button id
function buttonClick(page_id, button_id) {
 var button = new ROSLIB.Message({
   data:`{"page_id": "${page_id}", "button_id": "${button_id}"}`,
 });
 move.publish(button); // Publishing data for getting feedback to main
}

// this fun created for testing purpose
function moveToGoal() {
  var backBtn = new ROSLIB.Message({
    data: 'Clab-tour-btn',
  });
  move.publish(backBtn);
 }
