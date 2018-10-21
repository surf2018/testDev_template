$(function () {
    var url = window.location.pathname;
    var url = url.split("/")[1];
    var li = $(".nav.nav-sidebar").children("li");
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