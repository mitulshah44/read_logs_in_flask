var getData = function(){
	$(".renderBlock").html("<p>Loading.....</p>");
	var vdata = $('.dropdown').val();
	$.ajax({
	  url: "/api/getcontent",
	  type: "POST",
	  data: JSON.stringify({path : vdata}),
	  dataType : "json",
	  contentType: "application/json; charset=utf-8",
	  success: function(data){
		  renderData(data);
	  },
	  
	});
}

var renderData = function(data){
	$(".renderBlock").html("");
	for (var i in data) {
	  $(".renderBlock").append("<p>" + data[i] + "</p>");
	}
	console.log(data.length)
	if(data.length==0){
		$(".renderBlock").html("<p>No Data Available</p>");
	}
}


$(".dropdown").select2().on("change", function(e) {
	 getData(); 
});

$( document ).ready(function() {
	getData()
});
