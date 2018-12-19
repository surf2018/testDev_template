$(function(){
  getData();
  setInterval(function(){
   getData();
  }, 10000);
 });
function getData(){
    //查询中的taskid
    var task_id=""
    $.each($("#taskstatus"), function(i,value) {
        v = $(this).text()
        if (v == "执行中") {
            task_id = $(this).attr('value')
            // alert(task_id)
            return false;
        }
    })
    if(task_id==""){
         $('#request-process-patent1').html("没有任务执行")
    }
    else {
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
                    $('tr#' + task_id + '>td#taskstatus').text("执行结束")
                    $('#request-process-patent').html("")
                }
                else {
                    $('tr#' + task_id + '>td#taskresult').text(ret.data)
                    $('tr#' + task_id + '>td#taskstatus').text("执行结束")
                    $('#request-process-patent').html("")
                }
            },
            error: function (ret) {
                console.log("debug_ajax fail")
                $('tr#' + task_id + '>td#taskstatus').text("执行结束")
                $('#request-process-patent').html("失败")

            }
        })
    }
 };