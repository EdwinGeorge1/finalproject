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
      <script src= 'js/ros/eventemitter2.min.js'></script>
      <script src= 'js/ros/roslib.min.js'></script>
      
      <script src= 'js/ros/ros.js'></script>

   </head>
   <body class="start-01">
      <!-- banner section start  -->
      <div class="container">
         <div class="col-md-10 col-md-offset-1">
           <div class="start-click">
            <div class="comp comp-01">
                <a class="" href='clab-tour.php' onclick="buttonClick('home-page', 'clab-tour-button');"><img src="img/Component1.png"/></a>
            </div>
            <div class="comp comp-02">
                <a class="" href="team-members.php" onclick="buttonClick('home-page', 'clab-team-member');"><img src="img/Component3.png"/></a>
            </div>
            <img src="img/logo.png"/>
            <div class="comp comp-03">
                <a class="" href="fab-lab-support.php" onclick="buttonClick('home-page', 'fab_lab-support-button');"><img src="img/Component2.png"/></a>
            </div>
            <div class="comp comp-04">
                <a class="" href="gamba.php" onclick="buttonClick('home-page', 'gimba-button');"><img src="img/Component4.png"/></a>
            </div>
           </div>
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
