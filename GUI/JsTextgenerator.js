function FbuttonGenerate(event){
	event.preventDefault()
	
	var textInput = document.getElementsByName("textFromHtml")[0].value;
	var lengthInput = document.getElementsByName("lenght")[0].value; 
	
	fetch('http://127.0.0.1:8080/start?textFromHtml=' + encodeURIComponent(textInput))
    .then(function(response) {
		response.json().then(function (json){
			
			// for( var i=0; i<json.length; i++ )
				// {
					// document.write(json[i] + '<br />');
				// }

			console.debug(json);
			document.getElementById('result').innerHTML=json;
			document.getElementById('length').innerHTML=lengthInput;
		})        
    })
}



