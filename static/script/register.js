$(document).ready(function(){

    var form = $("#form");

    form.on('submit', function (event) {
        event.preventDefault();

        var data = new FormData($("#form"));

        form.find("input, select").each(function(iter, child){
            if(child.type === 'file')
                data.append(child.name, child.files[0]);
            else if(child.type === 'select')
                data.append(child.name, child.val());
            else
                data.append(child.name, child.value)
        });

        data.append('ajax', true);

        $.ajax({
            url: '/users/register/act/',
            data: data,
            method: "POST",
            cache: false,
            processData: false,
            contentType: false,
            type: form.attr('method'),
            dataType: "JSON",
            success: function (data){
                $("#errors").empty();
                var errDiv = $("<div class=\"alert alert-danger\"><strong>Error: </strong> </div>");

                if(data.success){
                    window.location.href = '/users/';
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