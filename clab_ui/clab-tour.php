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

   </head>
   <body class="start">
      <!-- banner section start-->
      <div class="container">
         <div class="col-md-10 col-md-offset-1">
           <div class="video-ring">
            <img src="img/subtraction.png"/>
           <div class="video-play">
           <!-- /  <video src="img/video.mp4" width="100%"  height="410px" controls></video> -->
           <img src="gif/Happy-eye-blink.gif"/>
           </div>
           <div id="animtContHold" style="  position:absolute; bottom: 72px; left: 180px; right:180px; text-align:center; color:#ffffff;">
            <div id="animtCont" >            
            </div>
            </div>                       
            <div class="bottom-ring-section">
                <div class="row">
                <a class=""  href="start-01.php" onclick="buttonClick('clab-tour-page', 'clab-tour-back-button');">
                    <div class="col-md-2">
                    <!-- previous code -->
                        <span style="font-size:20px; font-weight: bold;"><i class="fa fa-angle-left"></i> Back</span> 
                        <!-- <span style='font-size:75px;'>&#8617;</span>  back icon--> 
                        <!-- <span ><i class="fa fa-angle-left"></i>Back</span> -->

                    </div>
                     </a>

                    <div class="col-md-8">
                        <p></p>
                    </div>
                    <a class="" href="product.php" onclick="buttonClick('clab-tour-page', 'clab-tour-skip-button');">
                    <div class="col-md-2">
                    <!-- <a class="" href="product.php">SKIP  <i class="fa fa-angle-right"></i></a>   previous code-->

                    <!-- <span style='font-size:50px;' class="fa">&#xf050;</span> Skip icon -->

                    <span style="font-size:20px; font-weight: bold;">Skip <i class="fa fa-angle-right"></i></span>
                    </div>
                    </a>
                </div>
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
<script>
const txtArr = [
    "We are part of small R&AE team in RNTBCI.", 
	"We are only 4 members who are located in this LAB.",
    "We all know Innovation is important to all of us. If we don't innovate we die. We need to keep pace with fast moving technology and customer demands.", 
    "Mainly 4 areas to concentrate.",
	"1.	Product innovation-this is for our main core business area-making cars",
	"2.	Process Innovation-this is for our plant and manufacturing processes",
	"3.	Logistics or Transportation-SCM or vehicle movement",
	"4.	Marketability idea- improve revenues or improve sales",
"The idea is to promote innovation and creativity among employees. Creative LAB is a common platform available for everyone to come and share their innovative idea.",
"We have similar Labs in TCR France, Brazil, Romania & Korea. International team is setting up labs in Russia and Argentina too.",
"It is important to give an idea, but it is equally important to nurture idea with strong feedback and supportive ecosystem.",
"As you can see, we are well connected with teams inside and outside organization. We work closely with teams inside and are aware about each team's skillset.",
"We are also connected with agencies outside for strong technical support.",
"We encourage our employees to come and participate in different events. It can be:",
"- Technical talks",
"- Brainstorming events",
"- Collaborative work with universities and LABs",
"- Technology exhibitions to ignite that innovative mindset",
"We also arrange technology displays for our employees of technical center. The idea is to bring innovations from other fields like smart homes, well-being or from aerospace for display.",
"This method is used to connect employees with ideas coming from other sectors and to look for automotive solutions. Let's explore the products."

	
];

cnt = 0 ;
var i = 0;
var txt = txtArr[0];
var speed = 50;

function typeWriter() {

    if(i==0) {
        document.getElementById("animtCont").innerHTML = '';

        $("#animtContHold").css({
            bottom: '72px',
            opacity: '1'
        });        
    }

    if (i < txt.length) {
        document.getElementById("animtCont").innerHTML += txt.charAt(i);
        i++;
        setTimeout(typeWriter, speed);
    }
    else {

        i = 0;
        cnt++;
        console.log(cnt);        
        if(cnt==txtArr.length)
            cnt = 0;
        console.log('--'); 
        console.log(cnt);         
        txt = txtArr[cnt];
       
        aniHgt = $("#animtContHold").height();

        $("#animtContHold").animate({
            bottom: '120px',
            opacity: '0'
        },1750, function() {
            typeWriter();
        });        
    }
}
typeWriter();
</script>
