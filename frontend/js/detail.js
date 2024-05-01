$(function() {
    const searchParams = new URLSearchParams(window.location.search);
    const item_id = searchParams.get('id');
    $.ajax({
        url: `https://pythonproject-production-009d.up.railway.app/api/v1/store/item/${item_id}`,
        type: 'GET',
        dataType: 'json', // added data type
        success: function(res) {
            console.log(res)
            const product_img = document.querySelector("#product_img")
            const reviews_view = document.querySelector("#reviews_view")

            let img = res["img_links"]
            let name = res["name"]
            let price = res["price"]
            let reviews = res["reviews"]

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
        }
    });
});