//创建task
function createTask() {
    window.location.href = "/task/task_manager/?type=create"
}
//返回到caselist
$('#return').click(function () {
    window.location.href = "/task/task_manager/?type=tasklist"
})

//删除 task
function deltask(taskid, taskname) {
    var r = confirm("确定删除" + taskname + " 任务？")
    if (r == true) {
        window.location.href = "/task/delTask/" + taskid + "/"
    }
    else {
        window.location.href = "/task/task_manager/?type=tasklist"
    }
}
//判断all是否勾选
function selectAllCase() {
    //如果selectAll被选中
    if($('#selectAll').is(':checked')){
        console.log("selectAll被勾选")
        $("input[name='casename']").prop('checked',true)
    }
    else{
        alert("ALL没有勾选")
        $("input[name='casename']").prop('checked',false)
    }
}
//check测试用例如果有一条没有被选中，all就取消勾选
function oneToAll() {
    var checkAll=0
    var all=0
    $("input[name='casename']").each(function (i) {
        all += 1
        if ($(this).is(':checked')) {
            checkAll += 1
        }
    })
    if(checkAll==all){
        console.log("测试用例全部选择")
        //当用例被全选中，那么All会被勾选
        $("#selectAll").prop("checked",true)
    }
    else{
        console.log("用例没有全部选中")
        $("#selectAll").prop("checked",false)
    }
}
//如果addcase的button被点击，在右边显示出增加的用例名
$('#addCase').click(function () {
    $("input[name='casename']").each(function (i) {
        if ($(this).is(':checked')) {
            checkAll += 1
        }
    })
})