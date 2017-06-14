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
    $(function () {

        $(".wmd-view-topscroll").scroll(function () {
            $(".wmd-view")
            .scrollLeft($(".wmd-view-topscroll").scrollLeft());
        });

        $(".wmd-view").scroll(function () {
            $(".wmd-view-topscroll")
            .scrollLeft($(".wmd-view").scrollLeft());
        });

    });

    $(window).load(function () {
        $('.scroll-div').css('width', $('.dynamic-div').outerWidth() );
    });
    
  
    $('#container').on("select_node.jstree", function (e, data) {
       if(data.node.children.length == 0){
         $.ajax({
            type: 'POST',
            url: '/display_file',
            data: JSON.stringify({'id' : data.node.id}),
            contentType: "application/json; charset=utf-8",            
            success: function(data) {
                console.log(data);
                console.log($.type(data));
                $('#content').empty();
                $('#content').text(data);
            },
            error: function(error) {
                console.log(error);
            }
        });
          
       } 
    });
 
    // slide_btn on click: change V -> ^ and call slide function
    $('.slide_btn').click(function(){
       // change V -> ^ and vice versa
       text = $(this).text();
       console.log(text);
       updateText = text.indexOf('&#9650;') >= 0  ? text.replace('&#9650;', '&#9660;')   : text.replace('&#9660;', '&#9650;' );
       console.log(updateText);
       $(this).text(updateText);
       // slide child element
       console.log('#' + $(this).data('child'));
       $('#' + $(this).data('child')).slideToggle();
       
    })
     
});


function download_checked_items(){
     selected = $('#container').jstree('get_selected');
     idList = []
     $(selected).each(function(){
                    if(this.indexOf('/') != -1){
                      idList.push(this);
                    } 
             });
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
