$(document).ready(function(){
   draw_jstree();
});

function draw_jstree() {
    $('#container').jstree({
          'core' : {
            'data' : {
              "url" : "/populate_jstree",
              "dataType" : "json" // needed only if you do not supply JSON headers
            }
          }
        });
}
