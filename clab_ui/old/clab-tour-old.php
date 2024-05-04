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
                    <div class="col-md-2">
                        <a class="" href="start-01.php"><i class="fa fa-angle-left"></i> Back</a>
                    </div>
                    <div class="col-md-8">
                        <p></p>
                    </div>
                    <div class="col-md-2">
                    <a class="" href="product.php">SKIP  <i class="fa fa-angle-right"></i></a>
                    </div>
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
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam posuere nec nunc ac aliquam. Curabitur elementum finibus consequat. Suspendisse volutpat ligula at convallis faucibus.", 
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam posuere nec nunc ac aliquam. Curabitur elementum finibus consequat. Suspendisse volutpat ligula at convallis faucibus."
];

cnt = 0 ;
var i = 0;
var txt = txtArr[0];
var speed = 25;

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
            bottom: '150px',
            opacity: '0'
        },3000, function() {
            typeWriter();
        });        
    }
}
typeWriter();
</script>
