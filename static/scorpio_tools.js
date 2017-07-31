function query_here(obj) {  
    var id = $(obj).attr("id");  
    //获取表格中的一行数据 
    url =  "query/" + id;
    $.get(url, function(data, success){
    	var number = data.create_time.substr(0,4) * 10000 + data.id * 1;
		$("#id").text(number);
		$("#item").text(data.item);
		$("#remark").text(data.remark);
		$("#create_time").text(data.create_time);
		$("#operator").text(data.operator);
	});
}  

function create_new(obj) {
    $("#createNewForm").submit();
    // $.post("new", {inputItem:$("#inputItem").val(), inputRemark:$("#inputRemark").val()}, function(data){
    //     alert("数据: \n" + data + "\n状态: " + status);
    // }, "json");
}

//将form转为AJAX提交
function ajaxSubmit(frm, fn) {
    var dataPara = getFormJson(frm);
    $.ajax({
        url: frm.action,
        type: frm.method,
        data: dataPara,
        success: fn
    });
}

//将form中的值转换为键值对
function getFormJson(frm) {
    var o = {};
    var a = $(frm).serializeArray();
    $.each(a, function () {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } 
        else {
            o[this.name] = this.value || '';
        }
    });
    return o;
}

$(document).ready(function(){
    $('#createNewForm').bind('submit', function(){
        ajaxSubmit(this, function(data){
            var number = data.create_time.substr(0,4) * 10000 + data.id * 1;
            $("#id").text(number);
            $("#item").text(data.item);
            $("#remark").text(data.remark);
            $("#create_time").text(data.create_time);
            $("#operator").text(data.operator);
        });
        return false;
    });
});


$("#myModalLabel").on("hidden.bs.modal", function(){
    $("#myModalLabel").modal("show");
})

function reflash(){
    window.location.reload();
}