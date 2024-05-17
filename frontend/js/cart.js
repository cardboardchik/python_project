$(function() {
    if (window.localStorage.getItem("auth_token") == null){
        window.location.replace("login.html")
    }
    $.ajax({
        url: "https://pythonproject-production-009d.up.railway.app/api/v1/cart/",
        type: 'GET',
        async: false,
        headers: {'Authorization': window.localStorage.getItem("auth_token")},
        dataType: 'json', // added data type
        success: function(res) {
            let total_price = 0
            let items = document.querySelector('#items');
            for (let i=0; i < res.length; i += 1){
                console.log(res[i])
                let total_item_price = parseInt(res[i]["item_descr"]["price"]) * parseInt(res[i]["quantity"])
                total_price += total_item_price
                items.innerHTML += `<tr>
                <td class="align-middle"><img src="https:${res[i]["item_descr"]["img_link"]}" alt="" style="width: 50px;"> ${res[i]["item_descr"]["name"]}</td>
                <td class="align-middle">$${res[i]["item_descr"]["price"]}</td>
                <td class="align-middle">
                ${res[i]["quantity"]}
                </td>
                <td class="align-middle">$${total_item_price}</td>
                <td class="align-middle"><button class="btn btn-sm btn-danger remove" cartitem_id="${res[i]["id"]}"  ><i class="fa fa-times"></i></button></td>
            </tr>`
            }

            $("#stotal").text(`$${total_price}`)
            $("#total").text(`$${total_price + 10}`)
        }
    });
   
    
        
    $(".remove").click(function(){
        let cartitem_id = $(this).attr("cartitem_id")
        $.ajax({
        url: `https://pythonproject-production-009d.up.railway.app/api/v1/cart/items/${cartitem_id}/`,
        type: 'DELETE',
        async: false,
        headers: {'Authorization': window.localStorage.getItem("auth_token")},
        dataType: 'json', // added data type
        });
        window.location.reload()
    })
    
    
    
    
});