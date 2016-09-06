
console.log('loading')

// var searchID = 'adventure' //change to search input

function getSearchImages(searchID){
	var animalRef = firebase.database().ref('data/'+searchID+'/');
	animalRef.on('value', function(snapshot) {
  		console.log(snapshot.val()[0][0])
  
  		var response = snapshot.val();
  		console.log(response)

  		for (var index in response) {
    		console.log(response[index][1])
    		addImage(response[index][1]);
  		}
	});
};




// fill with photos

function addImage(url){
  $('.image').append("<img src="+url+">");
}


// remove all images

function clearImages(){
  $('.image').empty();
}



$(function() {
	var nameRef = firebase.database().ref('labels/')
	nameRef.on('value', function(snapshot) {
		var names = snapshot.val()
		console.log(names)

	    $("#tags").autocomplete({
	    	source: names,
	    	focus: function( event, ui ) {
		    	$( "#tags" ).val( ui.item.label );
		      	return false;
		    },
	    	select: function(event, ui){
	    		var searchID = ui.item.value
	    		clearImages();
	    		getSearchImages(searchID);
			}
		})
	})
});

  
