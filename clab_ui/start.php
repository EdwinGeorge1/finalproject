<!DOCTYPE html>
<html lang="en">
   <head>
      <meta charset="utf-8">
      <meta http-equiv="X-UA-Compatible" content="IE=edge">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
      <title>C-Lab</title>
      <!-- global level styles -->
      <?php include_once("includes/global-styles.php"); ?>
      <!-- / global level styles end -->
      <!-- page level plugin styles -->
      <!-- / page level plugin styles end -->
      <!-- Website theme style sheet -->
      <?php include_once("includes/website-theme.php"); ?>
      <!-- / Website theme style sheet end-->
      <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
      <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
      <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
      <![endif]-->
      <!-- <script type="text/javascript" src="http://static.robotwebtools.org/EventEmitter2/current/eventemitter2.min.js"></script>
      <script type="text/javascript" src="http://static.robotwebtools.org/roslibjs/current/roslib.min.js"></script> -->
      <script src= 'js/ros/eventemitter2.min.js'></script>
      <script src= 'js/ros/roslib.min.js'></script>
      
      <script src= 'js/ros/ros.js'></script>
      <!-- <script  src= 'js/ros/ros_clab.js'></script> -->
   </head>
   <body class="start">
      <!-- banner section start-->
      <div class="container">
         <div class="col-md-10 col-md-offset-1">
            <a class="" href="video.php" onclick="buttonClick('start-page', 'start-button');">
               <div class="start-section">
                  <img src="gif/start.gif"/>
               </div>
            </a>
         </div>
      </div>
      <!-- / banner section end -->
      <!-- global plugin scripts  -->
      <?php include_once("includes/global-scripts.php"); ?>
      <!-- / global plugin scripts end -->
      <!-- page level plugin scripts include -->
      <!-- / page level plugin scripts include end -->
      <!-- page level scripts  -->
      <!-- page level scripts end-->
   </body>
</html>
