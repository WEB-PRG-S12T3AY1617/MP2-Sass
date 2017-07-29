$(document).ready(function(){

    var form = $("#form");

    form.on('submit', function (event) {
        event.preventDefault();

        $.ajax({
            url: '/users/login/act/',
            data: form.serialize() + "&ajax=true",
            method: "POST",
            dataType: "JSON",
            success: function (data){
                $("#errors").empty();
                var errDiv = $("<div class=\"alert alert-danger\"><strong>Error: </strong> </div>");

                if(data.success){
                    window.location.href = '/users/login/';
                }else{
                    if(typeof data.error === "string"){
                        errDiv.append(data.error);
                        $("#errors").append(errDiv);
                    }else{
                        $.each(data, function(iter, item){
                            errDiv.innerHTML = "<strong>Error: </strong> " + item;
                            $("#errors").append(errDiv);
                        })
                    }
                }

            }
        });
    })

});