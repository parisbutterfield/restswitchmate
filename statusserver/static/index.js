String.prototype.compose = (function (){
var re = /\{{(.+?)\}}/g;
return function (o){
        return this.replace(re, function (_, k){
            return typeof o[k] != 'undefined' ? o[k] : '';
        });
    }
}());

function process (macaddress) {
window.open('http://' + location.hostname + ':5001/auth?macaddress=' + macaddress , '_blank')

}


$( document ).ready(function() {


  var tbody = $('#myTable').children('tbody');
  var table = tbody.length ? tbody : $('#myTable');
  var row = '<tr>'+
      '<td>{{macaddress}}</td>'+
      '<td>{{status}}</td>'+
      '<td>{{updated}}</td>'+
       '<td> <button onclick=process(\'{{macaddress}}\')> Authenticate </button> </td>'+
  '</tr>';

  $.get( "http://" + location.hostname + ":5000/devices", function( data ) {
  $.each( JSON.parse(data), function( i, val){

      table.append(row.compose({
          'macaddress': val.macaddress,
          'status': val.status,
          'updated': val.updated
      }));

});


  });



});
