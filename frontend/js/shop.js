$(function() {
    $.ajax({
        url: 'https://pythonproject-production-009d.up.railway.app/api/v1/store/item/',
        type: 'GET',
        dataType: 'json', // added data type
        success: function(res) {
            // console.log(res);
            let items = document.querySelector('#items');
        for (let i=0; i < res.length; i += 30){
            let name = res[i]['name']
            let img = res[i]['img_links']
            let price = res[i]['price']
            
            items.innerHTML += `<div class='col-lg-4 col-md-6 col-sm-6 pb-1'> <div class='product-item bg-light mb-4'> <div class='product-img position-relative overflow-hidden'> <img class='img-fluid w-100' src='https:${img}' alt=''> <div class='product-action'> <a class='btn btn-outline-dark btn-square' href=''><i class='fa fa-shopping-cart'></i></a> <a class='btn btn-outline-dark btn-square' href=''><i class='far fa-heart'></i></a> <a class='btn btn-outline-dark btn-square' href=''><i class='fa fa-sync-alt'></i></a> <a class='btn btn-outline-dark btn-square' href=''><i class='fa fa-search'></i></a> </div> </div> <div class='text-center py-4'> <a class='h6 text-decoration-none text-truncate' href=''>${name}</a> <div class='d-flex align-items-center justify-content-center mt-2'> <h5>$${price}</h5><h6 class='text-muted ml-2'><del>$${price}</del></h6> </div> <div class='d-flex align-items-center justify-content-center mb-1'> <small class='fa fa-star text-primary mr-1'></small> <small class='fa fa-star text-primary mr-1'></small> <small class='fa fa-star text-primary mr-1'></small> <small class='fa fa-star text-primary mr-1'></small> <small class='fa fa-star text-primary mr-1'></small> <small>(99)</small> </div> </div> </div> </div>`;
        }
        
        }
    });
});