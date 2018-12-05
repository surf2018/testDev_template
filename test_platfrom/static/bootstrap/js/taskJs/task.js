//获取到taskid，显示task的值
$(function () {
    var aurl = window.location.pathname
    var taskid = aurl.split('/')[-1]
    console.log(taskid)
    $.ajax({
        url: "/task/querytask/",
        type: 'POST',
        data: {"taskid": taskid},
        success: function (results) {
            console.log(results)
        },
        error: function () {
        }
    })
})
   var setting = {
      async: {
         enable: true,
         autoParam:["id"], //异步请求，点击节点时，自动提交name属性，服务端可以通过request.POST.get(name)；注意，第一次初始化的时候，传的是空
         type: "post",
         url: "/ztree/dirlist/"
      }
};
   $(document).ready(function(){
      $.fn.zTree.init($("#treeDemo"), setting);
   });
