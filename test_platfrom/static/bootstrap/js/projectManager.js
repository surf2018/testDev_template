function createPorject(pn){
  window.location.href="/project/dashboard?type="+pn
}
function createVersion(pname,pid){
  window.location.href="/project/createVersion?type=vcreate&pname="+pname+"&pid="+pid
}
// function broadcast() {
//   window.location.href="/broadcast"
// }
function delpop(pname) {
  alert("是否需要删除项目："+pname)
}

function delVpop(version) {
  alert("是否需要删除版本号："+version)
}
// function search() {
//
//
// }