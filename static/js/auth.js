$(function(){
    $("#auth").click(function(){
        $.ajax({
            type: 'POST',
            url: '/auth',
            data: JSON.stringify({"user_name":$("#inputUsername").val(),
                                  "password":$("#inputPassword").val()
                                }),
            contentType: 'application/json',
            success: function(response){
                if(response == "0"){
                    $("#alert").css('display','')
                    $("#alert").html("auth failed.")
                }else{
                    $("#inputUsername").val("")
                    $("#inputPassword").val("")
                }
            },
            error: function(response){
                console.log("application error")
            }
        })
    })
})