$('#send').click(function () {
        $('#request-process-patent').html("正在提交数据...")
        let req_name = $('#req_name').val();
        let req_url = $('#req_url').val();
        let req_method = $('input[name="req_method"]:checked').val();
        let req_type = $('input[name="req_type"]:checked').val();
        let req_header = $('#req_header').val();
        let req_parameter = $('#req_parameter').val();
        if (req_name == '') {
            window.alert("name不能为空");
            $('#request-process-patent').html("")
            return false
        }
        if (req_url == "") {
            window.alert("URL不能为空");
            $('#request-process-patent').html("")
            return false
        }
        //check url
        else {
            //判断URL地址的正则表达式为:http(s)?://([\w-]+\.)+[\w-]+(/[\w- ./?%&=]*)?
            //下面的代码中应用了转义字符"\"输出一个字符"/"
            var Expression = /http(s)?:\/\/([\w-]+\.)+[\w-]+(\/[\w- .\/?%&=]*)?/;
            var objExp = new RegExp(Expression);

            if (objExp.test(req_url) != true) {
                alert("网址格式不正确！请重新输入");
                $('#request-process-patent').html("")
                return false;
            }
        }
        if (req_header == "") {
            req_header = "{}";
        }
        else {
            //单引号转换为双引号
            req_header = req_header.replace(/\'/g, "\"");
        }
        if (req_parameter == "") {
            req_parameter = "{}";
        }
        else {
            //单引号转换为双引号
            req_parameter = req_parameter.replace(/\'/g, "\"");
            // alert(req_parameter)
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
            type: "POST",
            url: "/interface/debug_ajax/",
            data: datas,
            success: function (ret) {
                console.log("debug_ajax success")
                console.log(ret)
                $('#result').val(ret)
                $('#request-process-patent').html("Status:200 OK")
            },
            error: function (ret) {
                console.log("debug_ajax fail")
                $('#request-process-patent').html("失败")

            }
        })
    }
);

function createDebug() {
    window.location.href = "/interface/case_manager/?type=create"
}


$('#return').click(function () {
        window.location.href = "/interface/case_manager/?type=caselist"
    }
)
//update data
$('#update').click(function () {
        $('#request-process-patent').html("正在更新数据...");
        let req_username = $("#navbar_user").text();
        let req_caseid = window.location.href.split('/')[5]
        let req_proid = $("#pro-dropdown").val();
        let req_modid = $('#mod-dropdown').val();
        let req_name = $('#req_name').val();
        let req_url = $('#req_url').val();
        let req_status = $('input[name="req_status"]:checked').val();
        // alert(req_status)
        let req_method = $('input[name="req_method"]:checked').val();
        let req_type = $('input[name="req_type"]:checked').val();
        let req_header = $('#req_header').val();
        let req_parameter = $('#req_parameter').val();
        if (req_proid == "" || req_modid == "") {
            window.alert("请选择模块和项目");
            return false
        }
        if (req_name == '') {
            window.alert("name不能为空");
            $('#request-process-patent').html("");
            return false
        }
        if (req_url == "") {
            window.alert("URL不能为空");
            $('#request-process-patent').html("");
            return false
        }
        //check url
        else {
            //判断URL地址的正则表达式为:http(s)?://([\w-]+\.)+[\w-]+(/[\w- ./?%&=]*)?
            //下面的代码中应用了转义字符"\"输出一个字符"/"
            var Expression = /http(s)?:\/\/([\w-]+\.)+[\w-]+(\/[\w- .\/?%&=]*)?/;
            var objExp = new RegExp(Expression);

            if (objExp.test(req_url) != true) {
                alert("网址格式不正确！请重新输入");
                $('#request-process-patent').html("");
                return false;
            }
        }
        //check header
        if (req_header == "") {
            req_header = "{}";
        }
        else {
            //单引号转换成双引号
            req_header = req_header.replace(/\'/g, "\"");
        }
        if (req_parameter == "") {
            req_parameter = "{}";
        }
        else {
            //单引号转换为双引号
            req_parameter = req_parameter.replace(/\'/g, "\"");
            // alert(req_parameter)
        }
        var datas = {
            "username": req_username,
            "caseid": req_caseid,
            "proid": req_proid,
            "modid": req_modid,
            "name": req_name,
            "url": req_url,
            "status": req_status,
            "method": req_method,
            "type": req_type,
            "header": req_header,
            "parameter": req_parameter
        }
        console.log(datas);
        $.ajax({
            type: "POST",
            url: "/interface/update/",
            data: datas,
            success: function (ret) {
                console.log("debug_ajax success")
                console.log(ret)
                $('#request-process-patent').html("Save ok")
            },
            error: function (ret) {
                console.log("debug_ajax fail")
                $('#request-process-patent').html("Save fail")

            }
        })
    }
);
//save data
$('#save').click(function () {
        $('#request-process-patent').html("正在保存数据...");
        let req_username = $("#navbar_user").text();
        let req_proid = $("#pro-dropdown").val();
        let req_modid = $('#mod-dropdown').val();
        let req_name = $('#req_name').val();
        let req_url = $('#req_url').val();
        let req_status = $('input[name="req_status"]:checked').val();
        let req_method = $('input[name="req_method"]:checked').val();
        let req_type = $('input[name="req_type"]:checked').val();
        let req_header = $('#req_header').val();
        let req_parameter = $('#req_parameter').val();
        if (req_proid == "" || req_modid == "") {
            window.alert("请选择模块和项目");
            return false
        }
        if (req_name == '') {
            window.alert("name不能为空");
            $('#request-process-patent').html("");
            return false
        }
        if (req_url == "") {
            window.alert("URL不能为空");
            $('#request-process-patent').html("");
            return false
        }
        //check url
        else {
            //判断URL地址的正则表达式为:http(s)?://([\w-]+\.)+[\w-]+(/[\w- ./?%&=]*)?
            //下面的代码中应用了转义字符"\"输出一个字符"/"
            var Expression = /http(s)?:\/\/([\w-]+\.)+[\w-]+(\/[\w- .\/?%&=]*)?/;
            var objExp = new RegExp(Expression);

            if (objExp.test(req_url) != true) {
                alert("网址格式不正确！请重新输入");
                $('#request-process-patent').html("");
                return false;
            }
        }
        //check header
        if (req_header == "") {
            req_header = "{}";
        }
        else {
            //单引号转换成双引号
            req_header = req_header.replace(/\'/g, "\"");
        }
        if (req_parameter == "") {
            req_parameter = "{}";
        }
        else {
            //单引号转换为双引号
            req_parameter = req_parameter.replace(/\'/g, "\"");
            // alert(req_parameter)
        }
        var datas = {
            "username": req_username,
            "proid": req_proid,
            "modid": req_modid,
            "name": req_name,
            "url": req_url,
            "status": req_status,
            "method": req_method,
            "type": req_type,
            "header": req_header,
            "parameter": req_parameter
        };
        console.log(datas);
        $.ajax({
            type: "POST",
            url: "/interface/save/",
            data: datas,
            success: function (ret) {
                console.log("debug_ajax success")
                console.log(ret)
                $('#request-process-patent').html("Save ok")
            },
            error: function (ret) {
                console.log("debug_ajax fail")
                $('#request-process-patent').html("Save fail")

            }
        })
    }
);
//select的联动
$('#pro-dropdown').change(function (e) {
    var values = $(this).val();
    $.ajax({
        url: '/interface/seletAjax/?para=' + values,
        type: 'GET',
        success: function (results) {
            console.log(results)
            if (results) {
                var optionstring = "";
                $.each(results, function (key, value) {
                    optionstring += "<option value=\"" + key + "\">" + value + "</option>"
                });
                $("#mod-dropdown").html("<option value=''>请选择模块</option> " + optionstring)
            }
        },
        error: function () {

        }
    })
});

//delete case
function delcase(caseid, casename) {
    // alert("是否需要删除项目："+pname)
    var r = confirm("确定删除" + casename + " case？");
    if (r == true) {
        window.location.href = "/interface/delCase/" + caseid + "/";
    }
    else {
        window.location.href = "/interface/case_manager/?type=caselist";
    }
}

//点击debug,js传送caseid对应的信息给后台,成功后返回case的老数据
function debugCaseAjax(caseid) {
    //跳转到api_debug.html
    window.location.href=''
    var datas = {
        "caseid": caseid,
    };
    $.ajax({
        url: "/interface/debugCase/"+caseid+"/",
        type: 'POST',
        success: function (results) {
            console.log(results)
            if (results) {
                //成功跳转到api_debug.html
                var optionstring = "";
                $.each(results, function (key, value) {
                    optionstring += "<option value=\"" + key + "\">" + value + "</option>"
                });
                $("#mod-dropdown").html("<option value=''>请选择模块</option> " + optionstring)
            }
        },
        error: function () {

        }
    })

}