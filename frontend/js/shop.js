$.ajax({
    url: "https://pythonproject-production-009d.up.railway.app/api/v1/store/item/",
    headers: {  'Access-Control-Allow-Origin': '*' },
    type: 'GET',
    dataType: 'json', // added data type
    success: function(res) {
        console.log(res);
        alert(res);
    }
});