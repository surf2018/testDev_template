//addtask.html的项目和模块的联动
$('#pro-dropdown').change(function (e) {
    var values = $(this).val()
    $.ajax({
        url: '/task/seletAjax/?para=' + values,
        type: 'GET',
        success: function () {
            console.log(results)
            if(results.success=="false") {
                    alert(results.message)
                    return;
                }
            else {
                var optionstring = ""
                $.each(results, function (key, value) {
                    optionstring += "<option id=\"modname\" value=\"" + key + "\">" + value + "</option>"
                })
                $("#mod-dropdown").html("<option id=\"modname\" value=''>请选择模块</option> " + optionstring)
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
