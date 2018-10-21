function createPorject(pn){
  window.location.href="/project/dashboard?type="+pn
}

function createModule(mn){
  window.location.href="/module/modulelist?type="+mn
}
function createVersion(pname,pid){
  window.location.href="/project/createVersion/"+pid+"/"+pname+"/vcreate"
}
// function broadcast() {
//   window.location.href="/broadcast"
// }
function delpop(pname,pid) {
    // alert("是否需要删除项目："+pname)
    var r = confirm("确定删除" + pname + "项目？");
    if ( r  == true) {
      window.location.href = "/project/delProject/"+pid;
    }
    else {
      window.location.href = "/project/dashboard?type=plist";
    }
}

function delVpop(version,pid,vid) {
  // alert("是否需要删除版本号："+version)
    var r = confirm("确定删除版本" + version + "？");
    if ( r == true) {
      window.location.href ="/project/delVersion/"+vid;
    }
    else {
      window.location.href = "/project/dashboard?type=vlist&pid="+pid;
    }
}

function delmod(m_name,mid) {
    // alert("是否需要删除项目："+pname)
    var r = confirm("确定删除" + m_name + "模块？");
    if (r == true) {
        window.location.href = "/module/delModule/" + mid;
    }
    else {
        window.location.href = "/module/modulelist?type=mlist";
    }
}