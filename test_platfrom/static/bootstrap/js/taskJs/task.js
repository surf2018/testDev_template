//获取到taskid，显示task的值
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
                var caseinfo={};
                //显示已经选择的taskCase
                for (var i = 0; i < checkCaseList.length; i++) {
                // alert(checkCaseList[i])
                    operString += "<input name=\"casename\" id=\""+checkCaseList[i].caseid+"\" type=\"checkbox\" value=\""+checkCaseList[i].name+"\" onclick=\"roneToAll()\" >"+checkCaseList[i].proname+"-->"+checkCaseList[i].modname+"-->"+checkCaseList[i].casename+"</input><br />"

                }
                // alert(operStr)
                var operS="<label><input id=\"selectAll\" type=\"checkbox\" value=\"-1\" onclick=\"rselectAllCase()\">All</label><br />"+operString
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
        enable: true
        }
    }
};
// var zNodes =[
//   { id:1, pId:0, name:"湖北省", open:true},
//   { id:11, pId:1, name:"武汉市", open:true},
//   { id:111, pId:11, name:"汉口"},
//   { id:112, pId:11, name:"武昌"},
//   { id:12, pId:1, name:"黄石市", open:true},
//   { id:121, pId:12, name:"黄石港区"},
//   { id:122, pId:12, name:"西塞山区"},
//   { id:2, pId:0, name:"湖南省", open:true},
//   { id:21, pId:2, name:"长沙市"},
//   { id:22, pId:2, name:"株洲市", open:true},
//   { id:221, pId:22, name:"天元区"},
//   { id:222, pId:22, name:"荷塘区"},
//   { id:23, pId:2, name:"湘潭市"}
// ];
$(document).ready(function(){
  $.fn.zTree.init($("#treeInfo"), setting);
});