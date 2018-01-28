$.urlParam = function(name){
  var results = new RegExp('[\\?&]' + name + '=([^&#]*)').exec(top.window.location.href);
  return (results !== null) ? results[1] : 0;
}

String.prototype.compose = (function (){
var re = /\{{(.+?)\}}/g;
return function (o){
        return this.replace(re, function (_, k){
            return typeof o[k] != 'undefined' ? o[k] : '';
        });
    }
}());



$( document ).ready(function() {


var socket = io("http://" + location.hostname + ":5001");

  var tbody = $('#myTable').children('tbody');
  var table = tbody.length ? tbody : $('#myTable');
  var row = '<tr>'+
      '<td>{{status}}</td>'+
      '<td>{{date}}</td>'+

  '</tr>';


  socket.on('status', function (status) {
    var date = moment().format('MMMM Do YYYY, h:mm:ss a');
          table.prepend(row.compose({
              'status': status,
              'date': date
          }));

  });

  $('#authbutton').click(function() {
    $(this).prop("disabled",true);
    socket.emit("auth", $.urlParam("macaddress"))
  });


//   $.get( "http://10.0.1.29:5000/devices", function( data ) {
//   $.each( JSON.parse(data), function( i, val){
//
//       table.append(row.compose({
//           'macaddress': val.macaddress,
//           'status': val.status,
//           'updated': val.updated
//       }));
//
// });
//
//
//   });

  // //Add row
  // table.append(row.compose({
  //     'id': 3,
  //     'name': 'Lee',
  //     'phone': '123 456 789'
  // }));

});
