$(function() {
    if (window.localStorage.getItem("auth_token") == null){
        window.location.replace("login.html")
    }
    $("#logout_btn").click(function() {
        window.localStorage.clear()
        window.location.replace("shop.html")
    })
    
});