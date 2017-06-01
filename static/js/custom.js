var getData = function(filepath, isNewFile){
	// $(".renderBlock").html("<p>Loading.....</p>");
	$.ajax({
	  url: "/api/getcontent",
	  type: "POST", 
	  data: JSON.stringify({path : filepath, isNewFile:isNewFile}),
	  dataType : "json",
	  contentType: "application/json; charset=utf-8",
	  success: function(data){
		  renderData(data);
	  },
	  
	});
};



var renderData = function(data){
    console.log(data['modified'])
    if(data['modified'] == true){
        $(".renderBlock").html("");
        for (var i in data['lines']) {
          $(".renderBlock").append("<p>" + data['lines'][i] + "</p>");
        }
        if(data.length==0){
            $(".renderBlock").html("<p>No Data Available</p>");
        }
     }
}; 


setInterval(function() {
	var filepath = $('.dropdown').val();
		getData(filepath, false);
 }, 3000); 



$(".dropdown").select2().on("change", function(e) {	
	var filepath = $('.dropdown').val(); 
	getData(filepath, true);
});

$( document ).ready(function() {
	var filepath = $('.dropdown').val(); 
	getData(filepath, true);
});


