$('#send').click(function () {
        $('#request-process-patent').html("正在提交数据...")
        let req_name = $('#req_name').val();
        let req_url = $('#req_url').val();
        let req_method = $('input[name="req_method"]:checked').val();
        let req_type = $('input[name="req_type"]:checked').val();
        let req_header = $('#req_header').val();
        let req_parameter = $('#req_parameter').val();
        if(req_name==''){
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
        else{
            //判断URL地址的正则表达式为:http(s)?://([\w-]+\.)+[\w-]+(/[\w- ./?%&=]*)?
            //下面的代码中应用了转义字符"\"输出一个字符"/"
            var Expression=/http(s)?:\/\/([\w-]+\.)+[\w-]+(\/[\w- .\/?%&=]*)?/;
            var objExp=new RegExp(Expression);

            if(objExp.test(req_url) != true){
                alert("网址格式不正确！请重新输入");
                $('#request-process-patent').html("")
                return false;
            }
        }
        if(req_header==""){
            req_header="{}";
        }
        else {
            //单引号转换为双引号
            req_header = req_header.replace(/\'/g,"\"");
        }

        if (req_parameter == "") {
            req_parameter = "{}";
        }
        else {
            //单引号转换为双引号
            req_parameter = req_parameter.replace(/\'/g,"\"");
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
            type:"POST",
            url:"/interface/debug_ajax/",
            data:datas,
            success: function(ret){
                    console.log("debug_ajax success")
                    console.log(ret)
                    $('#result').val(ret)
                    $('#request-process-patent').html("Status:200 OK")
                    },
            error:function (ret) {
                console.log("debug_ajax fail")
                $('#request-process-patent').html("失败")

            }

        })
    }
    );

function createDebug(){
  window.location.href="/interface/case_manager/?type=create"
}

//save data
$('#save').click(function () {
        $('#request-process-patent').html("正在保存数据...")
        let req_name = $('#req_name').val();
        let req_url = $('#req_url').val();
        let req_method = $('input[name="req_method"]:checked').val();
        let req_type = $('input[name="req_type"]:checked').val();
        let req_header = $('#req_header').val();
        let req_parameter = $('#req_parameter').val();
        if(req_name==''){
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
        else{
            //判断URL地址的正则表达式为:http(s)?://([\w-]+\.)+[\w-]+(/[\w- ./?%&=]*)?
            //下面的代码中应用了转义字符"\"输出一个字符"/"
            var Expression=/http(s)?:\/\/([\w-]+\.)+[\w-]+(\/[\w- .\/?%&=]*)?/;
            var objExp=new RegExp(Expression);

            if(objExp.test(req_url) != true){
                alert("网址格式不正确！请重新输入");
                $('#request-process-patent').html("")
                return false;
            }
        }
        //check header
        if(req_header==""){
            req_header="{}";
        }
        else{
            //单引号转换成双引号
            req_header = req_header.replace(/\'/g,"\"");
        }
        if (req_parameter == "") {
            req_parameter = "{}";
        }
        else {
            //单引号转换为双引号
            req_parameter = req_parameter.replace(/\'/g,"\"");
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
            type:"POST",
            url:"/interface/save/",
            data:datas,
            success: function(ret){
                    console.log("debug_ajax success")
                    console.log(ret)
                    $('#request-process-patent').html("Save ok")
                    },
            error:function (ret) {
                console.log("debug_ajax fail")
                $('#request-process-patent').html("Save fail")

            }

        })
    }
    );

//select的联动

$('#pro-dropdown').change(function (e) {
    var values=$(this).val();
    $.ajax({
            url: '/interface/seletAjax/?para=' + values,
            type: 'GET',
            success: function (result) {
                if (result.code == 100) {
                    var _fullinfo = "<option value=\"0\">请选择<\/option>";
                    $.each(result.data, function (i, thread) {
                        _fullinfo += '<option value=\"' + thread.id + '\">' + thread.name + '<\/option>';
                    })
                    $('#country').html(_fullinfo);
                    $('#province').html("<option value=\"0\">请选择<\/option>");
                    $('#city').html("<option value=\"0\">请选择<\/option>");
                }
            },
            error: function () {

            }
        }

    )

})