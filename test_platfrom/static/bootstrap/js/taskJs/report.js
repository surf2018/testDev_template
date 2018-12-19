$(function(){
                $('#myModal').modal("hide");
            });
function dreport(id,name){
    //report name赋值
    $('#myModalLabel').html(name);
    var datas = {
        "report": id
    }
    console.log(datas)
    $.ajax({
        type: "POST",
        url: "/task/queryReportResult/",
        traditional: true,
        data: datas,
        success: function (ret) {
            console.log(ret)
            if (ret.success == "false") {
                $('#reportResult').html(ret.message)
            }
            else {
                console.log(ret.data)
                $('#reportResult').text(ret.data)
            }
        },
        error: function (ret) {
            $('#reportResult').html(ret)

        }
    })
 }