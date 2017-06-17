$(function(){
    setup_download_csv();
});

function setup_download_csv()
{
    $('#download_csv').click(function(){
        var query_vars = {'csv_reqd':'1' };
        var new_url = append_query_string(window.location.href, query_vars);
        window.location.href = new_url;
    });
}
