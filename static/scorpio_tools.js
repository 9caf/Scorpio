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
    //向模态框中传值  
    // $('#stuno').val(stuno);  
    // $('#pass').val(pass);  
    // $('#stuname').val(name);  
    // if (sex == '女') {  
    //     document.getElementById('women').checked = true;  
    // } else {  
    //     document.getElementById('man').checked = true;  
    // }  
    // $('#update').modal('show');  
}  

$("#editinfo").on("hidden.bs.modal", function(){
	$("#editinfo").modal("show");
})
		
$("#myModalLabel").on("hidden.bs.modal", function(){
    $("#myModalLabel").modal("show");
})