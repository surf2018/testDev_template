//js传送caseid对应的信息给后台, 成功后返回case的数据库数据
$(function() {
    var aurl=window.location.pathname
    var caseid=aurl.split('/')[3]
    $.ajax({
        url: "/interface/queryCase/",
        type: 'POST',
        data: {"caseid": caseid},
        success: function(results) {
            console.log(results)
            //选择project
            var projects=results.pros
            var optionstring=""
            $.each($.parseJSON(projects),function (key,value) {
                if(value.fields.name==results.proname){
                     optionstring += "<option value=\"" + value.pk + "\" selected=\"selected\" >" + value.fields.name + "</option>"
                }
                else {
                    optionstring += "<option value=\"" + value.pk + "\">" + value.fields.name + "</option>"
                }
            })
                $("#pro-dropdown").html("<option value=''>请选择项目</option> " + optionstring)
            //选择模块
            var modules=results.mods
            var optionstring=""
            $.each($.parseJSON(modules),function (key,value) {
                if(value.fields.name==results.modname){
                     optionstring += "<option value=\"" + value.pk + "\" selected=\"selected\" >" + value.fields.name + "</option>"
                }
                else {
                    optionstring += "<option value=\"" + value.pk + "\">" + value.fields.name + "</option>"
                }
            })
                $("#mod-dropdown").html("<option value=''>请选择模块</option> " + optionstring)
         //设置name,url,参数,头
            var cases=$.parseJSON(results.cases)
            var caseName=cases[0].fields.name;
            $('#req_name').attr("value",caseName)
            var caseUrl=cases[0].fields.url;
             $('#req_url').attr("value",caseUrl)
            var caseHeader=cases[0].fields.header;
            $('#req_header').attr("value",caseHeader)
            var caseData=cases[0].fields.data;
            $('#req_parameter').attr("value",caseData)
            //设置状态，请求方法，类型
            var caseStatus=cases[0].fields.status;
            $(":radio[name='req_status'][value='" + caseStatus + "']").prop("checked", "checked");
            var caseMethod=cases[0].fields.method;
            $(":radio[name='req_method'][value='" + caseMethod + "']").prop("checked", "checked");
            var caseType=cases[0].fields.type;
            $(":radio[name='req_type'][value='" + caseType + "']").prop("checked", "checked");
        },
        error: function() {
        }
    })

})
