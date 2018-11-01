$(function () {
    var li = $(".nav.nav-sidebar").children("li");
    var aurl=window.location.href
    var url=aurl.split('/')[3]
    for (var i = 0; i < li.length; i++) {
        if (url == li[i].id) {
            li[i].className = "active";
            // li[i].firstChild.className = "active";

        } else {
            li[i].className = "";
            // li[i].firstChild.className = "";
        }
    }
})