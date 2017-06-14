// https://www.w3schools.com/bootstrap/bootstrap_ref_js_collapse.asp
// https://stackoverflow.com/questions/33502419/saving-multiple-blocks-collapsed-state-using-cookies-with-cookie
function setup_collapsible(target_block, button, butt_text)
{
      target_block.on("hide.bs.collapse", function(){
        button.html('<span class="glyphicon glyphicon-collapse-down"></span> ' + butt_text);
            var active = $(this).attr('id');
            var blocks= localStorage.blocks === undefined ? new Array() : JSON.parse(localStorage.blocks);
            if ($.inArray(active,blocks)==-1) //check that the element is not in the array
                blocks.push(active);
            localStorage.blocks=JSON.stringify(blocks);
          });
      target_block.on("show.bs.collapse", function(){
            button.html('<span class="glyphicon glyphicon-collapse-up"></span> ' + butt_text);
            var active = $(this).attr('id');
            var blocks= localStorage.blocks === undefined ? new Array() : JSON.parse(localStorage.blocks);
            var elementIndex=$.inArray(active,blocks);
            if (elementIndex!==-1) //check the array
            {
                blocks.splice(elementIndex,1); //remove item from array
            }
            localStorage.blocks=JSON.stringify(blocks); //save array on localStorage
      });
}

function set_collapsible_initial_state()
{
    var blocks=localStorage.blocks === undefined ? new Array() : JSON.parse(localStorage.blocks); //get all blocks
    for (var i in blocks)
    {
        if ($("#"+blocks[i]).hasClass('collapse')) // check if this is a panel
        {
            $("#"+blocks[i]).collapse("hide");
        }
    }
}