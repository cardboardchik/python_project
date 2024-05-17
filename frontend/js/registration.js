$(function() {
    if (window.localStorage.getItem("auth_token") != null){
        window.location.replace("shop.html")
    }
    let data = {
        "email": "text",
        "password": "",
    }
    $("#reg_btn").click(function(){
        data["email"] = $("#exampleInputEmail1").val();
        data["password"] = $("#exampleInputPassword1").val();

        $.ajax({
            url: "https://pythonproject-production-009d.up.railway.app/api/v1/auth/users/",
            type: 'POST',
            headers: {},
            data: data,
            dataType: 'json',
            success: function(res) {
                $("#reg_form").fadeOut()
                window.location.replace("login.html"); 
            },

            error: function(res){
                alert(res["responseText"])
            }
        });
    });
});