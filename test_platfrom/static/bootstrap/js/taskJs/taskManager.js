//创建task
function createTask() {
    window.location.href = "/task/task_manager/?type=create"
}
//返回到tasklist
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
//判断左边框all是否勾选
function lselectAllCase() {
    //请选择用例的All是否勾选
    if ($('#caseListView input#selectAll').is(':checked')) {
        // alert("请选择用例的All被勾选")
        $("#caseListView>input[name='casename']").prop('checked', true)
    }
    else {
        console.log("请选择用例的ALL没有勾选")
        $("#caseListView>input[name='casename']").prop('checked', false)
    }
}
function rselectAllCase() {
    //已选择用例的All是否勾选
     if($('#checkCaseList input#selectAll').is(':checked')){
        console.log("已选择用例的All被勾选")
        $("#checkCaseList input[name='casename']").prop('checked',true)
    }
    else{
        console.log("请选择用例的ALL没有勾选")
        $("#checkCaseList input[name='casename']").prop('checked',false)
    }
}

//check测试用例如果有一条没有被选中，all就取消勾选
function loneToAll() {
    var lcheckAll=0
    var lall=0
    $("#caseListView input[name='casename']").each(function (i) {
        lall += 1
        if ($(this).is(':checked')) {
            lcheckAll += 1
        }
    })
    if(lcheckAll==lall){
        console.log("请选择测试用例框的试用例全部选择")
        //当用例被全选中，那么All会被勾选
        $("#caseListView input#selectAll").prop("checked",true)
    }
    else{
        console.log("用例没有全部选中")
        $("#caseListView input#selectAll").prop("checked",false)
    }
}

function roneToAll(){
      //已选择用例框的判断
    var rcheckAll=0
    var rall=0
    $("#checkCaseList input[name='casename']").each(function (i) {
        rall += 1
        if ($(this).is(':checked')) {
            rcheckAll += 1
        }
    })
    if(rcheckAll==rall){
        console.log("已选择测试用例框的试用例全部选择")
        //当用例被全选中，那么All会被勾选
        $("#checkCaseList input#selectAll").prop("checked",true)
    }
    else{
        console.log("已选择测试用例框用例没有全部选中")
        $("#checkCaseList input#selectAll").prop("checked",false)
    }
}
//如果addcase的button被点击，在右边显示出增加的用例名
$('#addCase').click(function () {
    //将已选择的case记录到checkCaseList中，新的case将追加到列表中
    var checkCaseList=[];
    $("#checkCaseList>input[name='casename']").each(function (i) {
        let name=$(this).val()
        checkCaseList.push(name)
    })
    var operString="";
    //check 请选择用例框，将新选择用例加入到checkCaseList中,如果有用例选择已经添加将不再添加'
    $("#caseListView>input[name='casename']").each(function (i) {
        if ($(this).is(':checked')) {
            //如果被选中，加入数组
            let caseName = $(this).attr('id')
            if($.inArray(caseName, checkCaseList)==-1){
                checkCaseList.push(caseName)
            }
            else{
                alert(caseName+"已经存在了，不再添加")
            }
        }
    })
    console.log(checkCaseList)
    //遍历数组中的元素，显示在已选case的框中
    for(var i=0; i < checkCaseList.length; i++) {
        // alert(checkCaseList[i])
        let val=checkCaseList[i]
        operString += "<input name=\"casename\" id=\""+val+"\" type=\"checkbox\" value=\""+val+"\" onclick=\"roneToAll()\">"+val+"<br />"
    }
    var operStr="<label><input id=\"selectAll\" type=\"checkbox\" value=\"-1\" onclick=\"rselectAllCase()\">All</label><br />"+operString
    // alert(operStr)
    $("#checkCaseList").html(operStr)
})
//从已选择的框中删除case
$('#delCase').click(function (){
    var lastCheck=[]
    var operString=""
    //获取当前所有的caselist,勾选的不加入数组，最后显示数组达到删除效果
    $("#checkCaseList>input[name='casename']").each(function () {
        if(!$(this).is(":checked")){
            let val=$(this).val()
            lastCheck.push(val)
            operString += "<input name=\"casename\" id=\""+val+"\" type=\"checkbox\" value=\""+val+"\" onclick=\"roneToAll()\">"+val+"<br />"
        }
    })
     var operStr="<label><input id=\"selectAll\" type=\"checkbox\" value=\"-1\" onclick=\"rselectAllCase()\">All</label><br />"+operString
    $("#checkCaseList").html(operStr)
})
