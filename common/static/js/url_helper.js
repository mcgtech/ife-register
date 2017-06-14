// http://www.anattatechnologies.com/q/2014/03/javascript-appending-to-query-string/
function append_query_string(url, queryVars)
{
    var firstSeperator = (url.indexOf('?')==-1 ? '?' : '&');
    var queryStringParts = new Array();
    for(var key in queryVars) {
        queryStringParts.push(key + '=' + queryVars[key]);
    }
    var queryString = queryStringParts.join('&');
    return url + firstSeperator + queryString;
}

function get_query_string()
{
    return window.location.search;
}

function get_list_query(list)
{
    return list.length > 0 ? list : -1;
}