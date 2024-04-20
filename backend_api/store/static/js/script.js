



function getStatusKaspiLogin(task_id){
    $.ajax({
        type: 'GET',
        data: {'task_id': task_id},
        
        success: function(response){
            let redirect_url = $("#url").attr("data-url")
            const taskStatus = response.task_status;
            if (taskStatus === 'SUCCESS'){
                $('#load_status').text('SUCCESS')
                window.location.href = redirect_url
                return false
            }
            if (taskStatus === 'FAILURE'){ 
                $('#load_status').text(`Что-то пошло не так. Пожалуйста проверьте соответсвие тому, какой email вы указали при добавлении менеджера в кабинете продавца и какой указали здесь. Если email-ы соответсвуют, то просим подождать минутку). Если после ожидания вы видете эту ошибку, то попробуйте добавить другой ваш email. По всем вопросам писать в телеграм(https://t.me/tkartonchik) или на почту.`)
                return false;
            }
            $('#load_status').text(`${response.task_result['done']} / ${response.task_result['total']} `)
            setTimeout(function() {
                getStatusKaspiLogin(response.task_id);
              }, 1000);
        }
    })
            
}


$(document).on('submit','#kaspi_email_form',function(e){ 
    e.preventDefault();
    $.ajax({ 
        type:'POST',

        data:
        { 
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            kaspi_email: $('input[name="kaspi_email"]').val(),
        },
        success: function (res){
            getStatusKaspiLogin(res.task_id)
        }
        
    })
  
    
}); 

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

    // $(document).ready(function(){
    //     setInterval(function()
    //     {
    //         $.ajax({
    //             type: 'GET',
    
    //            success: function(response){
    
    //                 $('#load_status').text(response.data)
    //             }
                
    //         })
    //     }, 1000)
    // })