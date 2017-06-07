$(document).ready(function(){
   $('#container').jstree();
   draw_jstree();
});

function draw_jstree() {
//   alert('in draw_jstree()')
   var data;
   $.ajax({       
       url: "/populate_jstree",             
       dataType: "json",
       success: function(response){                    
            data = response;
        }
      console.log(data)
   })
   $('#container').jstree(true).settings.core.data = data;
   /*
   $('#container').jstree(true).refresh();
    $('#container').jstree({
          'core' : {
            'data' : {
              "url" : "/populate_jstree",
              "dataType" : "json" // needed only if you do not supply JSON headers
            }
          }
        });
  */
}
