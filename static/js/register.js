$(function(){
    $("#register").click(function(){
        $.ajax({
            type: 'POST',
            url: '/register',
            data: JSON.stringify({"email":$("#inputEmail").val(),
                                  "user_name":$("#inputUsername").val(),
                                  "password":$("#inputPassword").val(),
                                  "mac_address":$("#inputMacAddress").val()
                                }),
            contentType: 'application/json',
            success: function(response){
                if(response == "2"){
                    $("#inputEmail").val("")
                    $("#inputUsername").val("")
                    $("#inputPassword").val("")
                    $("#inputMacAddress").val("")
                    $("#success").css('display','')
                    $("#success").html("Sign up is successfully")
                }else if(response == "1"){
                    $("#alert").css('display','')
                    $("#alert").html("The same user name or MAC address is already in use.")

                }else{
                    $("#alert").css('display','')
                    $("#alert").html("register failed.")
                }
            },
            error: function(response){
                console.log("application error")
            }
        })
    })
})