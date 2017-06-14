function disable_old_links(links)
{
    links.each(function(ind, item){
        if (ind != 0)
        {
            var text = $(item).html();
            $(item).parent().html(text)
        }
    });
}