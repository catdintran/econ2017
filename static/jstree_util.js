$(document).ready(function(){
   $(function() {
        $('#container').jstree({
          'core' : {
            'data' : {
              "url" : "/populate_jstree",
              "dataType" : "json" // needed only if you do not supply JSON headers
            }
          }
        });
   });
});
