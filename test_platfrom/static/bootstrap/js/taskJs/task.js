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
//    var setting = {
//       async: {
//          enable: true,
//          autoParam:[pid,mid], //异步请求，点击节点时，自动提交name属性，服务端可以通过request.POST.get(name)；注意，第一次初始化的时候，传的是空
//          type: "post",
//          url: "/task/ztree/dirlist/"
//       }
// };
//    $(document).ready(function(){
//       $.fn.zTree.init($("#treeInfo"), setting);
//    });
