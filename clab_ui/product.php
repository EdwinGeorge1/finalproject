<?php
$imgArr = [
   [ 'title'=>"SPIRE STONE", 'desc'=>"Tired of stress and anxiety??? And to you want track your daily activities so SPIRE STONE help You in managing both. Spires patented respiration sensor measures your breathing patterns all-day to help you keep control and manage stress. Learn where and when you're tense, calm, or productive. Follow your health progress through activity, steps, calories, and more. Washer-resistant, charges wirelessly, and lasts 10 days on a single charge", 'img'=>"image-1.png" ],
   [ 'title'=>"BELKIN WEMO SWITCH", 'desc'=>"Monitor your energy costs and control your home from anywhere with the Wemo Insight WiFi Smart Plug. Using your zexisting home WiFi network, this Smart Plug allows you to control your lights and appliances and set worry-free schedules from a phone or tablet—with no hub or subscription required. The Insight Smart Plug also provides real-time energy reports to show how much energy your devices are consuming, so you can easily track how much your lights and appliances are costing you.", 'img'=>"image-2.png" ],
   [ 'title'=>"DROP STOP", 'desc'=>"The patented DROP STOP prevents keys, phones, change, jewelry, makeup, bottle caps, pens, gum, and more from falling down The Carmuda Triangle. Use it or lose it. No matter what color your car's interior, the gap between the center console and front seat naturally creates a dark shadow. Drop Stop's universal black neoprene casing is a completely streamlined gap blocker, almost invisible once you install it. You won't even know it's there. Drop Stop can be squished and stretched to fit in any size car seat crack (from as tiny as 1/4 inch to 3.5 inches wide) making it the perfect gap filler!", 'img'=>"image-3.png" ],
   [ 'title'=>"GROHE SENSE", 'desc'=>"Grohe Sense is the diligent water sensor. As soon as it is in contact with water, it emits a beeping sound and a red light flashes:  water leaks are instantly detected and communicated on your smartphone via the Ondus application. Grohe Sense also warns you when an abnormal humidity rate persists in your house. As a humidity rate which is too low also involves some risk (irritated sinuses, stinging eyes, etc.), Grohe Sense alerts you when the humidity rate drops below your pre-set humidity level. Equipped with a temperature measuring system, Grohe sense finally alerts you when the room temperature falls below 3 °C and thus allows you to react in case of frost risk in the cellar for example", 'img'=>"image-4.png" ],
   [ 'title'=>"LIVE SCRIBE SMART PEN", 'desc'=>"For those of us who prefer to write notes instead of typing them, write them with this smart pen and everything will instantly show up on your computer. The quickest, simplest way to bring valuable information from paper onto your tablet and smartphone, where it becomes more useful It also works with audio recordings, so anything you say can also be transcribed to your computers. Built-in memory on the smart pen captures and stores your notes, allowing you to sync to up to 4 iOS and Android devices", 'img'=>"image-5.png" ],
   [ 'title'=>"MINI PROJECTOR", 'desc'=>"The Mini projectors category includes the latest projector technology used in ultra-portable projectors, mobile presentations, and smart phone device integration. Mini projectors are commonly lumped in with pocket projectors and pico projectors, though they are a distinct breed. Enjoy and Share Movies, Photos, Music, Text files directly  with mini-HDMI, AV, USB, MicroSD inputs Anytime, anywhere projection with onboard 1800mah premium Lithium-ion battery which will last for 150mins. It can projects image size of 8-100 inches, contrast ratio- 1000:1, LED life: 20000Hrs", 'img'=>"image-6.png" ],
   [ 'title'=>"ROLLR MINI", 'desc'=>"Car generates tons of data every second. ROLLR helps in Processing that data into useful information and transforms Your car to smart car. Plug in the device into the OBD port The data with the help of ROLLR algorithms is processed and Send to cloud which you can access through the smart app This information can be helpful in locating the car, car health Details can be helpful in car diagnostics and maintenance The driving behavior of the user can also be tracked with this", 'img'=>"image-7.png" ],
   [ 'title'=>"VIRTUAL KEYBOARD", 'desc'=>"A virtual keyboard is a computer keyboard that a user operates by typing on or within a wireless- or optical-detectable surface or area rather than by depressing physical keys. The term virtual keyboard is sometimes used to mean a soft keyboard, which appears on a display screen as an image map This is a Virtual laser projection keyboard with Bluetooth speaker Integrated. This has internal rechargeable battery from  600mAh to 1000mAh,This can also be charged  wirelessly", 'img'=>"image-8.png" ],
   [ 'title'=>"SOLAR POWERED PHONE LOGO", 'desc'=>"Use the sun to charge your phone, in the most convenient way ever with this window phone charger its solar- powered . The Solar Window Charger is a convenient hassle free way to charge any smart phone or table. Just press the solar charger to any windows or glass surface and charge your devices using the power of the sun. Perfect for charging your phone at work or your tablet/kindle in the car! You can power your smart phone in l less than 2-3 hours. This lightweight solar window charger is perfect for on the go trips", 'img'=>"image-9.png" ],
   [ 'title'=>"BLUE GLOBE BLACK PLATFORM", 'desc'=>"This levitating globe is much more than an optical illusion. It floats impossibly in mid-air using a combination of science and magic. Two opposing magnets keep the 6 globe hovering in mid-air above the base. Especially the Wireless Transmission tech. You don't need connect anything to light the globe up. Your object will levitate even if the base is turned on its side or upside down, And will light itself when you plug the base, Also you can use the touch control to let the LED light. Globe, Platform Or both of them light off.", 'img'=>"image-10.png" ],
   [ 'title'=>"ZTYLUS STINGER", 'desc'=>"The ZTYLUS Stinger Emergency Tool is a one of a kind, Patented emergency escape tool that can be integrated into everyday life. The spring loaded window punch works easily and quickly to give you the best chance for escaping your vehicle. The Stinger will only break tempered glass. It is not designed to break windshields or laminated glass.The emergency escape tool comes with a razor sharp blade to help you cut your seatbelt if you find yourself unable to release it normally.", 'img'=>"image-11.png" ],

];
?>
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
      <link href="https://cdnjs.cloudflare.com/ajax/libs/OwlCarousel2/2.1.6/assets/owl.carousel.min.css" rel="stylesheet">
      <link href="https://cdnjs.cloudflare.com/ajax/libs/OwlCarousel2/2.2.1/assets/owl.theme.default.min.css" rel="stylesheet">
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
      <!-- <script type="text/javascript" src="http://static.robotwebtools.org/roslibjs/current/roslib.min.js"></script> -->
      <script src= 'js/ros/eventemitter2.min.js'></script>
      <script src= 'js/ros/roslib.min.js'></script>
      
      <script src= 'js/ros/ros.js'></script>
   </head>
   <body class="prdt-page">
      <!-- banner section start-->
      <div class="container">
         <div class="col-md-9 col-md-offset-1">
            <div class="owl-carousel hidden-xs hidden-sm product-scroll-box" id="product-slider-thumb">
                  <?php
                  $cnt = sizeof($imgArr);
                  foreach(array_reverse($imgArr) as $ech) {
                     ?>

                     <div class="item">
                     <div class="row">
                        <div class="col-md-12">
                           <img src="product_images/thumb/<?php echo $ech['img']?>?1=1"  onclick="prdtShow(<?php echo $cnt?>);"/>
                        </div>
                     </div>
                     </div>

                     <?php
                     $cnt--;
                  }
                  ?>
            </div>
         </div>            
         <div class="col-md-10 col-md-offset-1">            
            <div class="clearfix"></div>
            <div class="prdt-scroll-slider">
               <div class="owl-carousel" id="product-slider">

                  <?php
                  foreach($imgArr as $ech) {
                     ?>

                     <div class="item">
                     <div class="row">
                        <div class="col-md-7">
                           <div class="slider-dtl">
                           <h2><?php echo $ech['title']?></h2>
                           <p><?php echo $ech['desc']?></p>
                           </div>
                        </div>
                        <div class="col-md-5">
                           <img src="product_images/big/<?php echo $ech['img']?>?1=1"/>
                        </div>
                     </div>
                     </div>

                     <?php
                  }
                  ?>

               </div>
               <span class="owl-nav"> <span class="owl-prev" id="product-slider-prev" style="font-size:15px; font-weight: bold;"> <i class="fa fa-angle-left hidden-xs"></i>PREV</span> <span class="owl-next" id="product-slider-next" style="font-weight: bold;"> <i class="fa fa-angle-right  hidden-xs"></i>NEXT</span> </span>
            </div>
            <div class="back-to-home">
               <a class="" style="font-weight: bold;" href="start-01.php" onclick="buttonClick('product-page', 'product-home-button');">Home</a>
            </div>
         </div>
      </div>
      <!-- / banner section end -->
      <!-- global plugin scripts  -->
      <?php include_once("includes/global-scripts.php"); ?>
      <!-- / global plugin scripts end -->
      <!-- page level plugin scripts include -->
      <script src="https://cdnjs.cloudflare.com/ajax/libs/OwlCarousel2/2.1.6/owl.carousel.min.js"></script>
      <!-- / page level plugin scripts include end -->
      <!-- page level scripts  -->
      <script>


// This fun for the next product trigger
txt_listener.subscribe(function () {
            // console.log(m)
         	serv4.trigger( 'next.owl.carousel' );
         	thumb1.trigger( 'prev.owl.carousel', [ 300 ] ); 
            cntSet(1); 
            paragrphSlide();            
            slideQueue(1);       
         } );



function nextProductShow() {
         	serv4.trigger( 'next.owl.carousel' );
         	thumb1.trigger( 'prev.owl.carousel', [ 300 ] ); 
            cntSet(1); 
            paragrphSlide();            
            slideQueue(1);       
         } 
         curCnt = 1;     
         maxCnt = <?php echo sizeof($imgArr)?>;

         txtCont = [
            <?php
            $ij = 0;
            foreach($imgArr as $ech) {
               $ij++;
               echo '"'.$ech['desc'].'"'.(($ij==sizeof($imgArr))?'':",\r\n");
            }
            ?>
         ];

         var i = 0;
         var txt = '';
         var speed = 75;
         var timeSet;
         function typeWriter() {
            try {
            if(i==0) {
               $( ".active p" ).html('');
               console.log("------");
               console.log(curCnt);
               txt = txtCont[(curCnt-1)];        
            }

            if (i < txt.length) {
               $( ".active p" ).html($( ".active p" ).html()+txt.charAt(i));
               i++;
               timeSet = setTimeout(typeWriter, speed);
            }
            else {
               i = 0;
            }
            }
            catch(err) {
               timeSet = setTimeout(typeWriter, speed);
            }
         }         

         function paragrphSlide() {

            //$(".owl-item p").hide();
            //$( ".active p" ).slideDown(1500);
            clearTimeout(timeSet);
            txt = '';
            i = 0;
            typeWriter();
         }

         function cntSet(it) {

            if(it==1){

               if(curCnt==maxCnt)
                  curCnt = 1;
               else
                  curCnt++;
            }
            else  {

               if(curCnt==1)
                  curCnt = maxCnt;
               else
                  curCnt--;               
            }
            console.log(curCnt);
         }         

         var serv4 = $( '#product-slider' ).owlCarousel( {
         	loop: true,
         	margin: 30,
         	responsiveClass: true,
         	nav: false,
         	responsive: {
         		0: {
         			items: 1
         		},
         		600: {
         			items: 1
         		},
         		1000: {
         			items: 1
         		}
         	}
         } )
         

         var thumb1 = $( '#product-slider-thumb' ).owlCarousel( {
         	loop: true,
         	margin: 5,            
         	responsiveClass: true,
         	nav: false,
         	responsive: {
         		0: {
         			items: 1
         		},
         		600: {
         			items: 4
         		},
         		1000: {
         			items: 8
         		}
         	}
         } );  
         
         crslWidth = $("#product-slider-thumb.owl-carousel").width();         
         itmWidth = $("#product-slider-thumb.owl-carousel .owl-item.active").first().width();
         imgHgt = $("#product-slider-thumb.owl-carousel .owl-item.active").first().find("img").height();
         imgWdh = $("#product-slider-thumb.owl-carousel .owl-item.active").first().find("img").width();

         function slideQueue(val) {

            var slCnt = 0;
            $("#product-slider-thumb.owl-carousel .owl-item.active img").css( "height", imgHgt+'px' );
            $("#product-slider-thumb.owl-carousel .owl-item.active img").css( "width", imgWdh+'px' );
            //$("#product-slider-thumb.owl-carousel .owl-item.active").css( "width", itmWidth+'px' );
            $($("#product-slider-thumb.owl-carousel .owl-item.active")
               .get()
               .reverse())
               .each(function() {
                  ths = $(this); 
                  ths.find("img").css( "margin-top", (slCnt*4)+'px' ); 
                  ths.find("img").css( "height", (imgHgt-(slCnt*8))+'px' ); 
                  ths.find("img").css( "width", (imgWdh-(slCnt*8))+'px' );
                  //ths.css( "width", (ths.width()-(slCnt*6))+'px' );                                                                    
                  slCnt++;

            });
            
         }

         function prdtShow(curPdt) {

            if(curPdt<curCnt) {
               for (let i = 0; i < (maxCnt-curCnt+curPdt); i++) {
                  setTimeout(function() {
                     $( "#product-slider-next" ).trigger( "click" );
                  }, ((i*50)+10));
               }
            }

            if(curPdt>curCnt) {
               for (let i = 0; i < (curPdt-curCnt); i++) {
                  setTimeout(function() {
                     $( "#product-slider-next" ).trigger( "click" );
                  }, ((i*50)+10));
               }
            }
         }

         setTimeout(function() {
            slideQueue(0);
         }, 100);         

         $( '#product-slider-next' ).click( function () {
         	serv4.trigger( 'next.owl.carousel' );
         	thumb1.trigger( 'prev.owl.carousel', [ 300 ] ); 
            cntSet(1); 
            paragrphSlide();            
            slideQueue(1);       
         } )
         
         $( '#product-slider-prev' ).click( function () {
         	serv4.trigger( 'prev.owl.carousel', [ 300 ] );            
            thumb1.trigger( 'next.owl.carousel' );
            cntSet(-1);
            paragrphSlide();            
            slideQueue(-1);            
         } )             
      </script>
      <!-- page level scripts end-->
   </body>
</html>
