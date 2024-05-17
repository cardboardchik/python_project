$(function() {
    
    const searchParams = new URLSearchParams(window.location.search);
    let page = parseInt(searchParams.get('page'));
    let filter = ""
    if (searchParams.get('filters')){
        filter = encodeURI(searchParams.get('filters').toString()).replace("&", "%26")
    }
    console.log(page)
    console.log(filter)
    if (!page){
        page = 1;
    };
    $("#next_btn").click(function(){
        page += 1
        window.location.replace(`shop.html?page=${page}&filters=${filter}`)
    })
    $("#previous_btn").click(function(){
        if (page > 1){
            page -= 1
            window.location.replace(`shop.html?page=${page}&filters=${filter}`)
        }
    })

    $.ajax({
        url: `https://pythonproject-production-009d.up.railway.app/api/v1/store/item/?filters=${filter}&page=${page}`,
        type: 'GET',
        dataType: 'json', // added data type
        success: function(res) {
            console.log(res["results"]);
            let items = document.querySelector('#items');
        for (let i=0; i < res["results"].length; i += 1){
            let id = res["results"][i]['id']
            let name = res["results"][i]['name']
            let img = res["results"][i]['img_links']
            let price = res["results"][i]['price']
            
            items.innerHTML += `<div class='col-lg-4 col-md-6 col-sm-6 pb-1'> <div class='product-item bg-light mb-4'> <div class='product-img position-relative overflow-hidden'> <img class='img-fluid w-100' src='https:${img}' alt=''> <div class='product-action'> <a class='btn btn-outline-dark btn-square' ><i class='fa fa-shopping-cart'></i></a> </div> </div> <div class='text-center py-4'> <a class='h6 text-decoration-none text-truncate' href='detail.html?id=${id}'>${name}</a> <div class='d-flex align-items-center justify-content-center mt-2'> <h5>$${price}</h5><h6 class='text-muted ml-2'><del>$${price}</del></h6> </div> <div class='d-flex align-items-center justify-content-center mb-1'> <small class='fa fa-star text-primary mr-1'></small> <small class='fa fa-star text-primary mr-1'></small> <small class='fa fa-star text-primary mr-1'></small> <small class='fa fa-star text-primary mr-1'></small> <small class='fa fa-star text-primary mr-1'></small> <small>(99)</small> </div> </div> </div> </div>`;
        }
        
        }
    });
});