$(function() {
    const searchParams = new URLSearchParams(window.location.search);
    const item_id = searchParams.get('id');
    // $.ajax({
    //     url: `https://pythonproject-production-009d.up.railway.app/api/v1/store/item/?&page=${2}`,
    //     type: 'GET',
    //     dataType: 'json', // added data type
    //     success: function(res) {
    //         console.log(res["results"]);
    //         let items = document.querySelector('#carousel');
    //     for (let i=0; i < res["results"].length; i += 1){
    //         let id = res["results"][i]['id']
    //         let name = res["results"][i]['name']
    //         let img = res["results"][i]['img_links']
    //         let price = res["results"][i]['price']
            
    //         items.innerHTML += `<div class="product-item bg-light">
    //         <div class="product-img position-relative overflow-hidden">
    //             <img class="img-fluid w-100" src="https:${img}" alt="">
    //             <div class="product-action">
    //                 <a class="btn btn-outline-dark btn-square" href=""><i class="fa fa-shopping-cart"></i></a>
    //                 <a class="btn btn-outline-dark btn-square" href=""><i class="far fa-heart"></i></a>
    //                 <a class="btn btn-outline-dark btn-square" href=""><i class="fa fa-sync-alt"></i></a>
    //                 <a class="btn btn-outline-dark btn-square" href=""><i class="fa fa-search"></i></a>
    //             </div>
    //         </div>
    //         <div class="text-center py-4">
    //             <a class="h6 text-decoration-none text-truncate" href="detail.html?id=${id}">${name}</a>
    //             <div class="d-flex align-items-center justify-content-center mt-2">
    //                 <h5>$${price}</h5><h6 class="text-muted ml-2"><del>$123.00</del></h6>
    //             </div>
    //             <div class="d-flex align-items-center justify-content-center mb-1">
    //                 <small class="fa fa-star text-primary mr-1"></small>
    //                 <small class="fa fa-star text-primary mr-1"></small>
    //                 <small class="fa fa-star text-primary mr-1"></small>
    //                 <small class="fa fa-star text-primary mr-1"></small>
    //                 <small class="fa fa-star text-primary mr-1"></small>
    //                 <small>(99)</small>
    //             </div>
    //         </div>
    //     </div>`
    //     }
    //     console.log(items.innerHTML)
    //     }
    // });
    $.ajax({
        url: `https://pythonproject-production-009d.up.railway.app/api/v1/store/item/${item_id}`,
        type: 'GET',
        dataType: 'json', // added data type
        success: function(res) {
            console.log(res)
            const product_img = document.querySelector("#product_img")
            const reviews_view = document.querySelector("#reviews_view")
            const details = document.querySelector("#characteristics")

            let img = res["img_links"]
            let name = res["name"]
            let price = res["price"]
            let reviews = res["reviews"]
            let characteristics = res["characteristics"]

            product_img.innerHTML += 
            `<div class="carousel-item active">
                <img class="w-100 h-100" src="https:${img}" alt="Image">
            </div>`;

            $("#product_name").text(name)
            $("#product_price").text(`$${price}`)
            $("#product_reviews_count_1").text(`(${reviews.length} Reviews)`)
            $("#product_reviews_count_2").text(`Reviews (${reviews.length})`)
            $("#product_reviews_count_3").text(`${reviews.length} review for ${name}`)

            for (let i = 0; i < reviews.length; i++){
                reviews_view.innerHTML += 
                `<div class="media mb-4">
                    <img src="https://icons.veryicon.com/png/o/internet--web/prejudice/user-128.png" alt="Image" class="img-fluid mr-3 mt-1" style="width: 45px;">
                    <div class="media-body">
                        <h6>${reviews[i]["user"]}<small> - <i>${reviews[i]["date"]}</i></small></h6>
                        <div class="text-primary mb-2">
                            <b>${reviews[i]["rating"]}/10</b>
                        </div>
                        <p>${reviews[i]["text"]}</p>
                    </div>
                </div>`
            }
            
            for (const [key, value] of Object.entries(characteristics)) {
                details.innerHTML += 
                `<tr>
                    <td>${key}</td>
                    <td>${value}</td>
                </tr>`
              }

        }
    });

    

    let data = {
        "rating": 10,
        "text": "text",
        "item": item_id,
    }
    $("#review_button").click(function(){
        if (window.localStorage.getItem("auth_token") == null){
            window.location.replace("login.html")
        }

        data["rating"] = $("#rating_form").val();
        data["text"] = $("#message").val();
        if (data["rating"] == ""){
            throw alert("input rating cannot be empty")
        }
        $.ajax({
            url: "https://pythonproject-production-009d.up.railway.app/api/v1/store/reviews/",
            type: 'POST',
            headers: {'Authorization': window.localStorage.getItem("auth_token")},
            data: data,
            dataType: 'json',
            success: function(res) {
                // alert(res)
                $("#review_form").fadeOut()
                $.ajax({
                    url: `https://pythonproject-production-009d.up.railway.app/api/v1/store/item/${item_id}`,
                    type: 'GET',
                    dataType: 'json', // added data type
                    success: function(res) {
                        console.log(res)
                        const reviews_view = document.querySelector("#reviews_view")
            
                        let name = res["name"]
                        let reviews = res["reviews"]
            
                        $("#product_reviews_count_1").text(`(${reviews.length} Reviews)`)
                        $("#product_reviews_count_2").text(`Reviews (${reviews.length})`)
                        $("#product_reviews_count_3").text(`${reviews.length} review for ${name}`)
            
                        reviews_view.innerHTML += 
                            `<div class="media mb-4">
                                <img src="https://icons.veryicon.com/png/o/internet--web/prejudice/user-128.png" alt="Image" class="img-fluid mr-3 mt-1" style="width: 45px;">
                                <div class="media-body">
                                    <h6>${reviews.at(-1)["user"]}<small> - <i>${reviews.at(-1)["date"]}</i></small></h6>
                                    <div class="text-primary mb-2">
                                        <b>${reviews.at(-1)["rating"]}/10</b>
                                    </div>
                                    <p>${reviews.at(-1)["text"]}</p>
                                </div>
                            </div>`
                    }  
                });   
            },

            error: function(res){
                alert(res.responseJSON["error"])
            }
        });
    });

    $("#add_to_cart").click(function(){
        if (window.localStorage.getItem("auth_token") == null){
            window.location.replace("login.html")
        }
        let quantity = parseInt($("#quantity").val())
        let data_cart = {
            "quantity": quantity,
            "is_active": "True",
            "item": item_id
        }
        
        $.ajax({
            url: "https://pythonproject-production-009d.up.railway.app/api/v1/cart/items/",
            type: 'POST',
            headers: {'Authorization': window.localStorage.getItem("auth_token")},
            data: data_cart,
            dataType: 'json',
            success: function(res) {
                alert("Ok")
            },
            error: function(res){
                console.log(res)
                alert(res.responseJSON["error"])
            }
        });

        
    });

    

});