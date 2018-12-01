//点击debug,send当前数据到后台获得response结果
$('#send').click(function () {
        $('#request-process-patent').html("正在提交数据...")
        let req_name = $('#req_name').val()
        let req_url = $('#req_url').val()
        let req_method = $('input[name="req_method"]:checked').val()
        let req_type = $('input[name="req_type"]:checked').val()
        let req_header = $('#req_header').val()
        let req_parameter = $('#req_parameter').val()
        if (req_name == '') {
            window.alert("name不能为空")
            $('#request-process-patent').html("")
            return false
        }
//check url
        if (req_url == "") {
            window.alert("URL不能为空")
            $('#request-process-patent').html("")
            return false
        } else {
            // 判断URL地址的正则表达式为: http(s)?: // ([\w-] +\.)+[\w-]+(/[\w - . /?% &= ]*)?
            // 下面的代码中应用了转义字符"\"输出一个字符" /"
            // var Expression = / http(s)?: \/\/([\w-] +\.)+[\w-]+(\/ [\w - .\/?% &=]*)?/
            // var objExp=new RegExp(Expression)
            var Expression = "((https|http|ftp|rtsp|mms)?://)" +
                "?(([0-9a-z_!~*'().&=+$%-]+: )?[0-9a-z_!~*'().&=+$%-]+@)?" // ftp的user@ +
            "(([0-9]{1,3}\.){3}[0-9]{1,3}" // IP形式的URL - 199.194.52.184 +
            "|" // 允许IP和DOMAIN（域名） +
            "([0-9a-z_!~*'()-]+\.)*" // 域名 - www. +
            "([0-9a-z][0-9a-z-]{0,61})?[0-9a-z]\." // 二级域名 +
            "[a-z]{2,6})" // first level domain - .com or .museum +
            "(:[0-9]{1,4})?" // 端口 - : 80 +
            "((/?)|" // a slash isn't required if there is no file name +
            "(/[0-9a-z_!~*'().;?:@&=+$,%#-]+)+/?)$"
            var objExp = new RegExp(Expression)
            if (objExp.test(req_url) != true) {
                alert("网址格式不正确！请重新输入")
                $('#request-process-patent').html("")
                return false
            }
        }
//check header
        if (req_header == "") {
            req_header = "{}"
        } else {
            // 单引号转换为双引号
            req_header = req_header.replace(/\'/g, "\"")
        }
//check post 参数
        if (req_parameter == "") {
            req_parameter = "{}"
        } else {
            // 单引号转换为双引号
            req_parameter = req_parameter.replace(/\'/g, "\"")
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
        console.log(datas)
        $.ajax({
            type: "POST",
            url: "/interface/debug_ajax/",
            data: datas,
            success: function (ret) {
                console.log(ret)
                if(ret.success=="false") {
                    alert(ret.message)
                     $('#request-process-patent').html("")
                }
                else {
                    $('#result').val(JSON.stringify(ret.data))
                    $('#request-process-patent').html("<p><font color=\"red\" size=\"10\">"+ret.message+"</font></p>")
                }
            },
            error: function (ret) {
                console.log("debug_ajax fail")
                $('#request-process-patent').html("<p><font color=\"red\" size=\"10\">"+ret.message+"</font></p>")

            }
        })
    }
);
//更新 testcase 数据
$('#update').click(function () {
    $('#request-process-patent').html("正在更新数据...")
    let proName = $('option[id="proname"]:selected').val()
    let modNmae = $('option[id="modname"]:selected').val()
    let req_username = $("#navbar_user").text()
    let req_caseid = window.location.href.split('/')[5]
    let req_proid = $("#pro-dropdown").val()
    let req_modid = $('#mod-dropdown').val()
    let req_name = $('#req_name').val()
    let req_url = $('#req_url').val()
    let req_status = $('input[name="req_status"]:checked').val()
    let assertResult = $("#assertResult").val()
    // alert(req_status)
    let req_method = $('input[name="req_method"]:checked').val()
    let req_type = $('input[name="req_type"]:checked').val()
    let req_header = $('#req_header').val()
    let req_parameter = $('#req_parameter').val()
    if (req_proid == "" || req_modid == "") {
        window.alert("请选择模块和项目")
        return false
    }
//check project and module
    if (proName == "-1" || modNmae == "-1") {
        window.alert("请选择project和模块")
        return false
    }
    if (req_name == '') {
        window.alert("name不能为空")
        $('#request-process-patent').html("")
        return false
    }
    // check url
    if (req_url == "") {
        window.alert("URL不能为空")
        $('#request-process-patent').html("")
        return false
    } else {
        // 判断URL地址的正则表达式为: http(s)?: // ([\w-] +\.)+[\w-]+(/[\w - . /?% &= ]*)?
        // 下面的代码中应用了转义字符"\"输出一个字符" /"
        // var Expression = / http(s)?: \/\/([\w-] +\.)+[\w-]+(\/ [\w - .\/?% &=]*)?/
        // var objExp=new RegExp(Expression)
        var Expression = "((https|http|ftp|rtsp|mms)?://)" +
            "?(([0-9a-z_!~*'().&=+$%-]+: )?[0-9a-z_!~*'().&=+$%-]+@)?" // ftp的user@ +
        "(([0-9]{1,3}\.){3}[0-9]{1,3}" // IP形式的URL - 199.194.52.184 +
        "|" // 允许IP和DOMAIN（域名） +
        "([0-9a-z_!~*'()-]+\.)*" // 域名 - www. +
        "([0-9a-z][0-9a-z-]{0,61})?[0-9a-z]\." // 二级域名 +
        "[a-z]{2,6})" // first level domain - .com or .museum +
        "(:[0-9]{1,4})?" // 端口 - : 80 +
        "((/?)|" // a slash isn't required if there is no file name +
        "(/[0-9a-z_!~*'().;?:@&=+$,%#-]+)+/?)$"
        var objExp = new RegExp(Expression)
        if (objExp.test(req_url) != true) {
            alert("网址格式不正确！请重新输入")
            $('#request-process-patent').html("")
            return false
        }
    }
    // check header
    if (req_header == "") {
        req_header = "{}"
    } else {
        // 单引号转换成双引号
        req_header = req_header.replace(/\'/g, "\"")
    }
    if (req_parameter == "") {
        req_parameter = "{}"
    } else {
        // 单引号转换为双引号
        req_parameter = req_parameter.replace(/\'/g, "\"")
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
        "parameter": req_parameter,
        "assert": assertResult
    }
    console.log(datas)
    $.ajax({
        type: "POST",
        url: "/interface/update/",
        data: datas,
        success: function (ret) {
            console.log("debug_ajax success")
            console.log(ret)
            if(ret.success=="false") {
                    alert(ret.message)
                    $('#request-process-patent').html("")
                }
                else {
                    $('#result').val(ret.data)
                    $('#request-process-patent').html(ret.message)
                }
            },
        error: function (ret) {
            console.log("debug_ajax fail")
            $('#request-process-patent').html("失败")

        }
    })
});
//保存 testcase 的新数据
$('#save').click(function () {
    $('#request-process-patent').html("正在保存数据...")
    let proName = $('option[id="proname"]:selected').val()
    let modNmae = $('option[id="modname"]:selected').val()
    let req_username = $("#navbar_user").text()
    let req_proid = $("#pro-dropdown").val()
    let req_modid = $('#mod-dropdown').val()
    let req_name = $('#req_name').val()
    let req_url = $('#req_url').val()
    let req_status = $('input[name="req_status"]:checked').val()
    let req_method = $('input[name="req_method"]:checked').val()
    let req_type = $('input[name="req_type"]:checked').val()
    let req_header = $('#req_header').val()
    let req_parameter = $('#req_parameter').val()
    let assertResult = $("#assertResult").val()
    if (req_proid == "" || req_modid == "") {
        window.alert("请选择模块和项目")
        return false
    }
//check project and module
    if (proName == "-1" || modNmae == "-1") {
        $('#request-process-patent').html("")
        window.alert("请选择project和模块")
        return false
    }
    if (req_name == '') {
        window.alert("name不能为空")
        $('#request-process-patent').html("")
        return false
    }
    if (req_url == "") {
        window.alert("URL不能为空")
        $('#request-process-patent').html("")
        return false
    }
    // check url
    else {
        // 判断URL地址的正则表达式为: http(s)?: // ([\w-] +\.)+[\w-]+(/[\w - . /?% &= ]*)?
        // 下面的代码中应用了转义字符"\"输出一个字符" /"
        // var Expression = / http(s)?: \/\/([\w-] +\.)+[\w-]+(\/ [\w - .\/?% &=]*)?/
        // var objExp=new RegExp(Expression)
        var Expression = "((https|http|ftp|rtsp|mms)?://)" +
            "?(([0-9a-z_!~*'().&=+$%-]+: )?[0-9a-z_!~*'().&=+$%-]+@)?" // ftp的user@ +
        "(([0-9]{1,3}\.){3}[0-9]{1,3}" // IP形式的URL - 199.194.52.184 +
        "|" // 允许IP和DOMAIN（域名） +
        "([0-9a-z_!~*'()-]+\.)*" // 域名 - www. +
        "([0-9a-z][0-9a-z-]{0,61})?[0-9a-z]\." // 二级域名 +
        "[a-z]{2,6})" // first level domain - .com or .museum +
        "(:[0-9]{1,4})?" // 端口 - : 80 +
        "((/?)|" // a slash isn't required if there is no file name +
        "(/[0-9a-z_!~*'().;?:@&=+$,%#-]+)+/?)$"
        var objExp = new RegExp(Expression)
        if (objExp.test(req_url) != true) {
            console.log(req_url)
            alert("网址格式不正确！请重新输入")
            $('#request-process-patent').html("")
            return false
        }
    }
    // 处理header
    if (req_header == "") {
        req_header = "{}"
    }
    else {
        // 单引号转换成双引号
        req_header = req_header.replace(/\'/g, "\"")
    }
    // 处理post的参数
    if (req_parameter == "") {
        req_parameter = "{}"
    }
    else {
        // 单引号转换为双引号
        req_parameter = req_parameter.replace(/\'/g, "\"")
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
        "parameter": req_parameter,
        "assert": assertResult
    }
    console.log(datas)
    $.ajax({
        type: "POST",
        url: "/interface/save/",
        data: datas,
        success: function (ret) {
            console.log("debug_ajax success")
            console.log(ret)
            if(ret.success=="false") {
                    alert(ret.message)
                    $('#request-process-patent').html("")
                }
                else {
                     $('#request-process-patent').html("<p><font color=\"red\" size=\"10\">"+ret.data+"</font></p>")
                }
            },
        error: function (ret) {
            console.log("debug_ajax fail")
            $('#request-process-patent').html("保存失败")

        }
    })
})
//api_debug.html的项目和模块的联动
$('#pro-dropdown').change(function (e) {
    var values = $(this).val()
    $.ajax({
        url: '/interface/seletAjax/?para=' + values,
        type: 'GET',
        success: function (results) {
            console.log(results)
            if(results.success=="false") {
                    alert(ret.message)
                    return;
                }
            else {
                var optionstring = ""
                $.each(results, function (key, value) {
                    optionstring += "<option id=\"modname\" value=\"" + key + "\">" + value + "</option>"
                })
                $("#mod-dropdown").html("<option id=\"modname\" value='-1'>请选择模块</option> " + optionstring)
            }
        },
        error: function (ret) {
            console.log("debug_ajax fail")
        }
    })
})
//验证结果：将预期结果和实际结果都发送给后台验证
$('#assert').click(function () {
    $('#request-process-patent').html("正在验证数据...")
    // 获取验证结果里的数据和返回结果数据
    var assertResult = $('#assertResult').val()
    var returnResult = $('#result').val()
    // 验证两个结果是否为空
    if (assertResult == "") {
        $('#request-process-patent').html("")
        alert("验证结果不能为空")

        return false
    }
    if (returnResult == "") {
        $('#request-process-patent').html("")
        alert("返回结果为空")
        return false
    }
    var datas = {
        "assertResult": assertResult,
        "returnResult": returnResult,
    }
    console.log(datas)
    $.ajax({
        type: "POST",
        url: "/interface/assert/",
        data: datas,
        success: function (ret) {
            console.log(ret)
            if(ret.success=="false") {
                    alert(ret.message)
                    $('#request-process-patent').html("")
                }
            else {
                    alert(ret.data)
                    $('#request-process-patent').html("")
                }
            },
        error: function (ret) {
            console.log("debug_ajax fail")
            $('#request-process-patent').html("失败")

        }
    })
})
