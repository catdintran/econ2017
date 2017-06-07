$(document).ready(function(){
 //  $('#container').jstree();
   draw_jstree();
   $('.jstree-checkbox').hide();
   $('#checkbox_btn').click(function(){
        show_hide_checkbox($(this));
   });
   $('#collapse_expand_btn').click(function(){
        collapse_expand_node($(this));
   });
   $('#download_btn').click(function(){
        download_checked_items();
   });
 
});

function download_checked_items(){
     idList = $('.jstree-clicked').map(function(){
                    return this.id
             }).toArray();
     console.log(idList);
}

function collapse_expand_node(data){
   if($(data).text() == 'Expand'){
      $('#container').jstree('open_all');
      $(data).text('Collapse');
   }else{
      $('#container').jstree('close_all');
      $(data).text('Expand');
   }
} 
function show_hide_checkbox(data){
   if($(data).text() == 'Checkbox'){
         $(data).text('Hide Checkbox');
         $('.jstree-checkbox').show();
         $('#download_btn').show();
   }else{
         $(data).text('Checkbox');
         $('.jstree-checkbox').hide();
         $('#download_btn').hide();
   }
} 

function draw_jstree() {
//   alert('in draw_jstree()')
   
    $('#container').jstree({
          'core' : {
            'data' : {
              "url" : "/populate_jstree",
              "dataType" : "json" // needed only if you do not supply JSON headers
            }
          },
          "plugins" : ["checkbox"]
        });
  
}
