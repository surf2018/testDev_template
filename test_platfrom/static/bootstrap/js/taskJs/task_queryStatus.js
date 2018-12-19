$(function(){
  getData();
  setInterval(function(){
   getData();
  }, 3000);
 });
function getData(){
    //查询中的taskid
    var task_id=""
    var flag=0
    $.each($("#taskstatus"), function(i,value) {
        v = $(this).text()
        if (v == "执行中") {
            flag=1
            task_id = $(this).attr('value')
            return false;
        }
    })
    if(flag==1) {
        var datas = {
            'taskid': task_id
        }
        $.ajax({
            type: "POST",
            url: "/task/getStatus/",
            data: datas,
            traditional: true,
            success: function (ret) {
                console.log(ret)
                if (ret.success == "false") {
                    $('td#' + task_id + '_taskstatus').text("执行结束")
                    $('#request-process-patent').html("")
                }
                else {
                    $('td#' + task_id + '_taskresult').text(ret.data)
                    $('td#' + task_id + '_taskstatus').text("执行结束")
                    $('#request-process-patent').html("")
                }
            },
            error: function (ret) {
                console.log("debug_ajax fail")
                $('td#tasktaskstatus').text("执行结束")
                $('#request-process-patent').html("失败")

            }
        })
    }
 };