function getStatus(task_id){
    $.ajax({
        type: 'GET',
        data: {'task_id': task_id},

        success: function(response){
            const taskStatus = response.task_status;
            if (taskStatus === 'SUCCESS'){ 
                $('#load_status').text('SUCCESS')
                window.location.reload()
                return false;
            }
            if (taskStatus === 'FAILURE'){ 
                $('#load_status').text('FAILURE')
                return false;
            }
            $('#load_status').text(`${response.task_result['done']} / ${response.task_result['total']} `)
            setTimeout(function() {
                getStatus(response.task_id);
              }, 1000);
        }
    })
            
}

const user_name = JSON.parse(document.getElementById('user_name').textContent);
$(`li[seller_name=${user_name}]`).css("color", "green")


$(document).on('submit','#refresh_form',function(e){ 
    e.preventDefault();
    $.ajax({ 
        type:'POST',
        
        data:
        { 
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val() 
        },
        success: function (res){
            getStatus(res.task_id)
            
        }
        
    })
  
});

function show_product_price_btns(id){
    $(`input[product-price-id=${id}]`).css('display', 'block')
    $(`input[product-cancel-price-btn-id=${id}]`).css('display', 'block')
}
function hide_product_price_btns(id){
    $(`input[product-price-id=${id}]`).css('display', 'none')
    $(`input[product-cancel-price-btn-id=${id}]`).css('display', 'none')

    def_value_product_min_price = $(`input[product-min-price-id=${id}]`).attr('def-value')
    def_value_product_max_price = $(`input[product-max-price-id=${id}]`).attr('def-value')
    def_value_product_step_price = $(`input[product-step-price-id=${id}]`).attr('def-value')

    console.log(def_value_product_min_price)
    $(`input[product-min-price-id=${id}]`).val(def_value_product_min_price)
    $(`input[product-max-price-id=${id}]`).val(def_value_product_max_price)
    $(`input[product-step-price-id=${id}]`).val(def_value_product_step_price)
}


$(document).on('click','#save_product_price_btn',function(e){ 
    var product_price_id = $(this).attr('product-price-id')
    if ($(`input[product-min-price-id=${product_price_id}]`).val() <= $(`input[product-max-price-id=${product_price_id}]`).val()){
        var product_price_id = $(this).attr('product-price-id')
        e.preventDefault();
        $.ajax({ 
            type:'POST',
            url: $(this).attr('update-url'),
            data:
            { 
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                product_price_id: product_price_id,
                product_min_price: $(`input[product-min-price-id=${product_price_id}]`).val(),
                product_max_price: $(`input[product-max-price-id=${product_price_id}]`).val(),
                product_step_price: $(`input[product-step-price-id=${product_price_id}]`).val(),
                
            },
            success: function (res){
                $(`input[product-price-id=${product_price_id}]`).css('display', 'none')
                $(`input[product-cancel-price-btn-id=${product_price_id}]`).css('display', 'none')
                
                $(`input[product-min-price-id=${product_price_id}]`).css('border-color', '#212529')
                $(`input[product-max-price-id=${product_price_id}]`).css('border-color', '#212529')
                if (res.meta == 'true'){
                    $('#liveToast').toast('show')
                    $('#info_body').text(res.data)
                }

            }
            
        })
    }
    else{
        $(`input[product-min-price-id=${product_price_id}]`).css('border-color', '#ff0000')
        $(`input[product-max-price-id=${product_price_id}]`).css('border-color', '#ff0000')
    }
});

