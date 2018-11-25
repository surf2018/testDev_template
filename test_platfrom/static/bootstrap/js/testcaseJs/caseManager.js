//创建testcase
function createDebug() {
    window.location.href = "/interface/case_manager/?type=create"
}
//返回到caselist
$('#return').click(function () {
    window.location.href = "/interface/case_manager/?type=caselist"
})

//删除 testcase
function delcase(caseid, casename) {
    // alert("是否需要删除项目：" + pname)
    var r = confirm("确定删除" + casename + " case？")
    if (r == true) {
        window.location.href = "/interface/delCase/" + caseid + "/"
    }
    else {
        window.location.href = "/interface/case_manager/?type=caselist"
    }
}