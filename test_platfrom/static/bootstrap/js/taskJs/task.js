//获取到taskid，显示已选择的caselist
$(function () {
    var aurl = window.location.pathname
    var taskid = aurl.split('/')[3]
    $.ajax({
        url: "/task/queryTask/",
        type: 'POST',
        data: {"taskid": taskid},
        success: function (results) {
            console.log(results)
            if(results.success=='true'){
                //显示tasksName and task description
                let task_name=results.data.taskname;
                let task_desp=results.data.taskDesp;
                $('#taskname').val(task_name);
                $('#taskdesp').val(task_desp);
                let checkCaseList=results.data.cases;
                var operString='';
                //显示已经选择的taskCase
                for (var i = 0; i < checkCaseList.length; i++) {
                    operString += "<input name=\"casename\" id=\""+checkCaseList[i].caseid+"\" type=\"checkbox\" value=\""+checkCaseList[i].casename+"\" onclick=\"roneToAll()\"  checked='checked'>"+checkCaseList[i].casename+"</input><br />"
                    console.log(operString)
                }
                // alert(operStr)
                var operS="<label><input id=\"selectAll\" type=\"checkbox\" value=\"-1\" onclick=\"rselectAllCase()\" checked=\"checked\" >All</label><br />"+operString
                $("#checkCaseList").html(operS)
            }
        },
        error: function () {
        }
    })
})
//ztree设置
var setting = {
    check: {
        enable: true,
        autoCheckTrigger: true,
        chkStyle: "checkbox",
        chkboxType: { "Y": "ps", "N": "s" }
    },
    async:{
        enable:true,
        otherParam:{//传入查询参数
            //注意，要传入动态变化的参数必须用return的方式
            "taskid":function(){
                return window.location.pathname.split('/')[3]
            }
        },
        type:'post',
        url:"/task/getZtreeList/"
    },
   data: {
        simpleData: {
        enable: true,

        }
    },
    callback:{
        beforeCheck:true,
        onCheck:onCheck //监听ztree
    }
};
//初始化ztree
$(document).ready(function(){
    $.fn.zTree.init($("#treeInfo"), setting);
});

function onCheck(e,treeId,treeNode){
    var treeObj = $.fn.zTree.getZTreeObj('treeInfo');
    var nodes = treeObj.getCheckedNodes(true)
    var id1 = "",pid1="",modid="",cs="",cur_caseid='',casename='';
    var checkedCaseArray=[];
    //得到mod和pro的关系
    for (var i = 0; i < nodes.length; i++) {
        id1 = nodes[i].id;
        pid1=nodes[i].pId;
        cs=nodes[i].checked;
        var testmodList={};
        if (id1 >= 40000 && cs==true) {
            cur_caseid=id1/40000;
            casename=nodes[i].name;
            testmodList={'caseid':cur_caseid,'casename':casename}
            checkedCaseArray.push(testmodList);
        }
    }
    console.log(checkedCaseArray)
    var operString='';
    for (var j = 0; j < checkedCaseArray.length; j++){
        operString += "<input name=\"casename\" id=\""+checkedCaseArray[j].caseid+"\" type=\"checkbox\" value=\""+checkedCaseArray[j].casename+"\" onclick=\"roneToAll()\"  checked='checked'>"+checkedCaseArray[j].casename+"</input><br />"
    }
    // alert(operStr)
    var operS="<label><input id=\"selectAll\" type=\"checkbox\" value=\"-1\" onclick=\"rselectAllCase()\" checked=\"checked\" >All</label><br />"+operString
    $("#checkCaseList").html(operS)
}