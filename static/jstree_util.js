$(document).ready(function(){
 //  $('#container').jstree();
   
     draw_jstree(); 
           
   $('#checkbox_btn').click(function(){
        show_hide_checkbox($(this));
   });
   $('#collapse_expand_btn').click(function(){
        collapse_expand_node($(this));
   });
   $('#download_btn').click(function(){
        download_checked_items();
   });
    $('.jstree-checkbox').hide();
    
    // show processing icon when form submit
    $('#submit_files').submit(function(e){
      $('#processing_icon').show();
      return true;
    })
 
 
});

function download_checked_items(){
     selected = $('#container').jstree('get_selected')
     idList = $(selected).map(function(){
                    if(this.includes('/')){
                      return this
                    } 
             }).toArray();
//     console.log(idList);
     $('<form>', {
       "method": "POST",
       "id": "idList_form",
       "html": '<input type="hidden" name="idList" value="' + idList + '" />',
       "action": '/download'
     }).appendTo(document.body).submit().remove();
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
