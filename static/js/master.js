$('.submit').on('click',function(event){
    event.preventDefault(); //this is important else page will get submitted
    $.ajax({
     url:'where you want to process data',
     dataType:'html',
     data: your form data as json or whatever type
     success: function(result){
     //here you can update any thing on the frontside
     }
    });
   });