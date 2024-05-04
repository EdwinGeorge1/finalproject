<?php
$imgArr = [
   [ 'title'=>"Spire STONE", 'desc'=>"Washer-resistant, charges wirelessly,and lasts 10 days on a single charge", 'img'=>"Spire-Stone.png" ],
   [ 'title'=>"Roller Mini", 'desc'=>"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.", 'img'=>"Rollr mini.png" ],

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
   </head>
   <body class="prdt-page">
      <!-- banner section start-->
      <div class="container">
         <div class="col-md-10 col-md-offset-1">
            <div class="row">
            <div class="col-md-10">
               <div class="owl-carousel hidden-xs hidden-sm product-scroll-box" id="product-slider-thumb">

                     <div class="item">
                     <div class="row">
                        <div class="col-md-12">
                           <img src="product_images/thumb/<?php echo $imgArr[0]['img']?>"  onclick="prdtShow(1);"/>
                        </div>
                     </div>
                     </div>

                     <?php
                     $cnt = sizeof($imgArr);
                     foreach(array_reverse($imgArr) as $ech) {

                        if($cnt!=1) {
                           ?>

                           <div class="item">
                           <div class="row">
                              <div class="col-md-12">
                                 <img src="product_images/thumb/<?php echo $ech['img']?>"  onclick="prdtShow(<?php echo $cnt?>);"/>
                              </div>
                           </div>
                           </div>

                           <?php
                        }
                        $cnt--;
                     }
                     ?>


               </div>
            </div> 
            </div>                         
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
                           <img src="product_images/big/<?php echo $ech['img']?>"/>
                        </div>
                     </div>
                     </div>

                     <?php
                  }
                  ?>

               </div>
               <span class="owl-nav"> <span class="owl-prev" id="product-slider-prev"> <i class="fa fa-angle-left hidden-xs"></i>PREV</span> <span class="owl-next" id="product-slider-next"> <i class="fa fa-angle-right  hidden-xs"></i>NEXT</span> </span>
            </div>
            <div class="back-to-home">
               <a class="" href="#">Home</a>
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
         curCnt = 1;     
         maxCnt = <?php echo sizeof($imgArr)?>;

         function paragrphSlide() {

            $(".owl-item p").hide();
            $( ".active p" ).slideDown(1500);
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
                  ths.find("img").css( "margin-top", (slCnt*5)+'px' ); 
                  ths.find("img").css( "height", (imgHgt-(slCnt*10))+'px' ); 
                  ths.find("img").css( "width", (imgWdh-(slCnt*10))+'px' );
                  //ths.css( "width", (ths.width()-(slCnt*6))+'px' );                                                                    
                  slCnt++;

            });
            
         }

         function prdtShow(curPdt) {

            if(curPdt<curCnt) {
               for (let i = 0; i < (curCnt-curPdt); i++) {
                  setTimeout(function() {
                     $( "#product-slider-next" ).trigger( "click" );
                  }, ((i*50)+10));
               }
            }

            if(curPdt>curCnt) {
               for (let i = 0; i < (curPdt-curCnt); i++) {
                  setTimeout(function() {
                     $( "#product-slider-prev" ).trigger( "click" );
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
            paragrphSlide(); 
            cntSet(1); 
            slideQueue(1);       
         } )
         
         $( '#product-slider-prev' ).click( function () {
         	serv4.trigger( 'prev.owl.carousel', [ 300 ] );            
            thumb1.trigger( 'next.owl.carousel' );
            paragrphSlide();
            cntSet(-1); 
            slideQueue(-1);            
         } )             
      </script>
      <!-- page level scripts end-->
   </body>
</html>
