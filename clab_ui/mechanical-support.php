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


      <script src= 'js/ros/eventemitter2.min.js'></script>
      <script src= 'js/ros/roslib.min.js'></script>
      
      <script src= 'js/ros/ros.js'></script>

   </head>
   <body class="start-02">
      <!-- banner section start-->
      <div class="container">
         <div class="col-md-10 col-md-offset-1">
            <div class="fab-lab-supports">
               <h2>FAB-LAB SUPPORT</h2>
               <p>Please select  the employee, and I will guide you.</p>
               <h3><i class="fa fa-dot-circle-o" aria-hidden="true"></i><a class="" href="#" style="text-decoration:none">MECHANICAL SUPPORT</a></h3>
               
                 <div class="row">
                  <div class="col-md-4 col-sm-4 col-xs-12">
                     <a class="" href="#" onclick="buttonClick('mech-support-page', 'sujith-button');">
                        <div >
                           <img src="img/Sujith.png"/>
                        </div>
                        </a>
                  </div>
                  <div class="col-md-4 col-sm-4 col-xs-12">
                     <a class="" href="#" onclick="buttonClick('mech-support-page', 'deepak-button');">
                        <div >
                           <img src="img/Deepak.png"/>
                        </div>
                        </a>
                  </div>
               </div>
               <br>
        
               <!--<div class="row">
                  <div class="col-md-4 col-sm-4 col-xs-12">
                     <a class="" href="#">
                        <div >
                           <img src="img/Sujith.png"/>
                        </div>
                        </a>
                  </div>
                  <div class="col-md-4 col-sm-4 col-xs-12">
                  <a class="" href="#"> <div >
                  <img src="img/Deepak.png"/>
                  </div></a>
                  </div>
               </div>-->
               <div class="back-section">
                  <a class="btn back-btn" href="fab-lab-support.php" onclick="buttonClick('mech-support-page', 'mech-support-back-button');">
                    <i class="fa fa-angle-left" aria-hidden="true"></i> Back
                  </a>
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
