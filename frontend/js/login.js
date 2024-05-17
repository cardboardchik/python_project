$(function() {
    if (window.localStorage.getItem("auth_token") != null){
        window.location.replace("shop.html")
    }
    let data = {
        "email": "text",
        "password": "",
    }
    $("#login_btn").click(function(){
        data["email"] = $("#exampleInputEmail1").val();
        data["password"] = $("#exampleInputPassword1").val();

        $.ajax({
            url: "https://pythonproject-production-009d.up.railway.app/auth/token/login/",
            type: 'POST',
            headers: {},
            data: data,
            dataType: 'json',
            success: function(res) {
                $("#login_form").fadeOut()
                window.localStorage.setItem("auth_token", `Token ${res["auth_token"]}`)
                window.location.replace("shop.html"); 
            },

            error: function(res){
                alert(res["responseText"])
            }
        });
    });
});