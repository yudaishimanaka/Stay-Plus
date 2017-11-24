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
                    console.log("register success")
                }else if(response == "1"){
                    console.log("既に同じメールアドレスまたはMACアドレスが登録されています。")
                }else{
                    console.log("register failed")
                }
            },
            error: function(response){
                console.log("application error")
            }
        })
    })
})