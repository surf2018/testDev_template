// function getCookie(name) {
//     var cookieValue = null;
//     if (document.cookie && document.cookie != '') {
//         var cookies = document.cookie.split(';');
//         for (var i = 0; i < cookies.length; i++) {
//             var cookie = jQuery.trim(cookies[i]);
//             // Does this cookie string begin with the name we want?
//             if (cookie.substring(0, name.length + 1) == (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }
// function csrfSafeMethod(method) {
// // these HTTP methods do not require CSRF protection
//     return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
// }

$('#send').click(function () {
        $('#request-process-patent').html("正在提交数据...")
        var req_name = $('#req_name').val();
        var req_url = $('#req_url').val();
        var req_method = $('input[name="req_method"]:checked').val();
        var req_type = $('input[name="req_type"]:checked').val();
        var req_header = $('#req_header').val();
        var req_parameter = $('#req_parameter').val();
        if(req_name==''){
            window.alert("name不能为空");
        }
        else if (req_url == "") {
            window.alert("URL不能为空");
        }
        else if (req_parameter == "") {
            req_parameter = "{}";
        }
        var datas = {
            "name": req_name,
            "url": req_url,
            "method": req_method,
            "type": req_type,
            "header": req_header,
            "parameter": req_parameter
        }
        console.log(datas);
        $.ajax({
            type:"POST",
            url:"/interface/debug_ajax/",
            data:datas,
            success: function(ret){
                    console.log("debug_ajax success")
                    $('#result').val(ret)
                     },
            error:function (ret) {
                console.log("debug_ajax fail")

            }

        })
    }
    )

function debug(){
  window.location.href="/interface/case_manager/?type=debug"
}

function delmod(m_name,mid) {
    // alert("是否需要删除项目："+pname)
    var r = confirm("确定删除" + m_name + "模块？");
    if (r == true) {
        window.location.href = "/module/delModule/" + mid+"/";
    }
    else {
        window.location.href = "/module/modulelist/?type=mlist";
    }
}