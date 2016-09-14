function FbuttonGenerate(event){
	event.preventDefault()
	
	var textInput = document.getElementsByName("textFromHtml")[0].value;
	
	fetch('http://127.0.0.1:8080/start?textFromHtml=' + encodeURIComponent(textInput))
    .then(function(response) {
		response.json().then(function (json){
			console.debug(json);
			document.getElementById('result').innerHTML=json;
		})        
    })
}



