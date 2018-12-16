//addtask.html的项目和模块, 项目和测试用例的联动
$('#pro-dropdown').change(function (e) {
    var values = $(this).val()
    // 模块是否被选中，如果被选中返回属于项目和模块的用例，不选中返回属于项目用例
    // var modVal=$('#mod-dropdown').val()
    var modVal = "-1"
    $.ajax({
        url: '/task/seletAjax/?ppara=' + values + '&mpara=' + modVal,
        type: 'GET',
        success: function (results) {
            console.log(results)
            if (results.success == "false") {
                alert(results.message)
                return;
            }
            else {
                var optionstring = ""
                var caseString = ""
                // 模块信息
                $.each($.parseJSON(results.data)['modList'], function (key, value) {
                    optionstring += "<option id=\"modname\" value=\"" +
                        key + "\">" + value + "</option>"
                })
                $("#mod-dropdown").html("<option id=\"modname\" value=''>请选择模块</option> " + optionstring)
                // 测试用例信息
                $.each($.parseJSON(results.data)['caseList'], function (key, value) {
                    caseString += "<input name=\"casename\" id=\"" + value +
                        "\" type=\"checkbox\" value=\"" + key + "\" onclick=\"loneToAll()\">" +
                        value + "<br />"
                })
                $("#caseListView").html("<label><input id=\"selectAll\" type=\"checkbox\" value=\"-1\" onclick=\"lselectAllCase()\">All</label><br />" + caseString)
            }
        },
        error: function (ret) {
            console.log("debug_ajax fail")
        }
    })
})
//addtask.html的模块的联动, 如果模块的值变动，测试用例重新显示
$('#mod-dropdown').change(function (e) {
    var values = $(this).val()
    // 判断项目是否被选择，如果被选择那么搜索属于项目并且模块的cases;
    // 如果项目没有选择, 那么选择至于与此模块的case
    var proValue = $('#pro-dropdown').val()
    $.ajax({
        url: '/task/seletAjax/?ppara=' + proValue + "&mpara=" + values,
        type: 'GET',
        success: function (results) {
            console.log(results)
            if (results.success == "false") {
                alert(results.message)
                return;
            }
            else {
                var optionstring = ""
                var caseString = ""
                var modId = $.parseJSON(results.data)['modId']
                console.log(modId)
                // 显示选中的模块
                $.each($.parseJSON(results.data)['modList'], function (key, value) {
                    if (key == modId) {
                        optionstring += "<option id=\"modname\" value=\"" +
                            key + " \" selected>" + value + "</option>"
                    }
                    else {
                        optionstring += "<option id=\"modname\" value=\"" +
                            key + "\">" + value + "</option>"
                    }
                })
                $("#mod-dropdown").html("<option id=\"modname\" value='-1'>请选择模块</option> " + optionstring)
                // 测试用例信息
                $.each($.parseJSON(results.data)['caseList'], function (key, value) {
                    caseString += "<input name=\"casename\" id=\"" + value +
                        "\" type=\"checkbox\" value=\"" + key + "\" onclick=\"loneToAll()\">" +
                        value + "<br />"
                })
                $("#caseListView").html("<label><input id=\"selectAll\" type=\"checkbox\" value=\"-1\" onclick=\"lselectAllCase()\">All</label><br />" + caseString)
            }
        },
        error: function (ret) {
            console.log("debug_ajax fail")
        }
    })
})
//保存任务
$('#save').click(function () {
    $('#request-process-patent').html("正在保存数据...")
    // 获取当前需要保存页面信息
    var task_name = $('#taskname').val()
    var task_desp = $('#taskdesp').val()
    // 获取任务的状态和运行结果
    // task状态: 0未执行 、1 执行中，2 执行结束
    var tstatus = $('#taskstat').val()
    var task_status;
    if (tstatus == "未执行") {
        task_status = 0
    }
    else if (tstatus == "执行中") {
        task_status = 1
    }
    else {
        task_status = 2
    }
    // task result: 0: NG 不通过，1: OK通过
    var result = $("#taskresult").val()
    var task_result;
    if (result == "测试OK") {
        task_result = 1
    }
    else {
        task_result = 0
    }
    // 获取用例列表
    var castlist = [];
    $("#checkCaseList>input[name='casename']").each(function (i) {
        if ($(this).is(':checked')) {
            let caseid = $(this).attr('id')
            castlist.push(caseid)
    }
    })
    console.log(castlist)
    // 验证任务名不能为空(判断重名在后台处理）
    if (task_name == "") {
        $('#request-process-patent').html("")
        alert("task名不能为空")
        return false;
    }
    //判断如果没有勾选用例不保存
    if(castlist.length==0){
        alert("请勾选用例再保存")
        return false;
    }
    var datas = {
        "taskName": task_name,
        "taskDesp": task_desp,
        "taskResult": task_status,
        "taskStat": task_status,
        "caseList": castlist
    }
    console.log(datas)
    $.ajax({
        type: "POST",
        url: "/task/save/",
        traditional: true,
        data: datas,
        success: function (ret) {
            console.log(ret)
            if (ret.success == "false") {
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
//更新任务
$('#updateTask').click(function () {
    $('#request-process-patent').html("正在保存更新数据...")
    // 获取当前需要保存页面信息
    var task_id=window.location.pathname.split('/')[3]
    var task_name = $('#taskname').val()
    var task_desp = $('#taskdesp').val()
    // 获取任务的状态和运行结果
    // task状态: 0未执行 、1 执行中，2 执行结束
    var tstatus = $('#taskstat').val()
    var task_status;
    if (tstatus == "未执行") {
        task_status = 0
    }
    else if (tstatus == "执行中") {
        task_status = 1
    }
    else {
        task_status = 2
    }
    // task result: 0: NG 不通过，1: OK通过
    var result = $("#taskresult").val()
    var task_result;
    if (result == "测试OK") {
        task_result = 1
    }
    else {
        task_result = 0
    }
    // 获取用例列表
    var castlist = [];
    $("#checkCaseList>input[name='casename']").each(function (i) {
        if ($(this).is(':checked')) {
            let caseid = $(this).attr('id')
            castlist.push(caseid)
    }
    })
    console.log(castlist)
    // 验证任务名不能为空(判断重名在后台处理）
    if (task_name == "") {
        $('#request-process-patent').html("")
        alert("task名不能为空")
        return false;
    }
    //判断如果没有勾选用例不保存
    if(castlist.length==0){
        alert("请勾选用例再保存")
        return false;
    }
    var datas = {
        'taskid':task_id,
        "taskName": task_name,
        "taskDesp": task_desp,
        "taskResult": task_status,
        "taskStat": task_status,
        "caseList": castlist
    }
    console.log(datas)
    $.ajax({
        type: "POST",
        url: "/task/update/",
        traditional: true,
        data: datas,
        success: function (ret) {
            console.log(ret)
            if (ret.success == "false") {
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

//执行任务
function runTask(taskid,taskname){
    $('#request-process-patent').html("正在执行任务"+taskname+"...")
    // 获取当前需要保存页面信息
    $('tr#'+taskid+'>td#taskstatus').text("执行中")
    // 将用例列表传入后台去执行用例
    var datas = {
        'taskid':taskid,
    }
    console.log(datas)
    $.ajax({
        type: "POST",
        url: "/task/runTask/",
        traditional: true,
        data: datas,
        success: function (ret) {
            console.log(ret)
            if (ret.success == "false") {
                alert(ret.message)
                $('#taskstat').val("执行完")
                $("#taskresult").val("测试NG")
                $('#request-process-patent').html("")
            }
            else {
                alert(ret.data)
                //设置结果
                if(ret.data=="任务运行成功") {
                    $('#taskstat').val("执行完")
                    $("#taskresult").val("测试OK")
                }
                $('#request-process-patent').html("")
            }
        },
        error: function (ret) {
            console.log("debug_ajax fail")
            $('#taskstat').val("执行完")
            $("#taskresult").val("测试NG")
            $('#request-process-patent').html("失败")

        }
    })
}