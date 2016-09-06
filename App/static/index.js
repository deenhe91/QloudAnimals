
console.log('loading')

var searchID = 'air force' //change to search input

var animalRef = firebase.database().ref(searchID+'/');

animalRef.on('value', function(snapshot) {
  console.log(snapshot.val()[0][0])
  
  var response = snapshot.val();
  console.log(response)

  for (var index in response) {
    console.log(response[index][1])
    addImage(response[index][1]);
  
  }
});


// fill with photos

function addImage(url){
  $('.image').append("<img src="+url+">");
}


// remove all images

when event(search) happens,
remove all images. 


$(function() {
  $( "#tags" ).autocomplete({
    source: availableFish,
     focus: function( event, ui ) {
      $( "#tags" ).val( ui.item.label );
      return false;
    },
    select: function(event, ui){
      $.ajax({
        type: "POST",
        url: '/api/searchbyfish',
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify(ui, null, '\t'),
        success: function(data) { 

        }
      });
    }
  });
});



