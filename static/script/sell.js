$(document).ready(function(){

    var form = $("#form");

    form.find("input[name=use]").each(function(iter, child){
        child.onclick = function(event){
            courseInput = $("input[name=course]");
            postTags = $("#id_tags");

            if(this.value !== '1'){
                courseInput.prop('disabled', true);
                courseInput.val('N/A');

                if(this.value === '0'){
                    if(postTags.val().indexOf("office") === -1)
                        postTags.val(postTags.val() + " office");

                    postTags.val(postTags.val().replace("others", ""));
                    postTags.val(postTags.val().replace("academic", ""));
                }else if(postTags.val().indexOf("others") === -1) {
                    postTags.val(postTags.val() + " others");

                    postTags.val(postTags.val().replace("office", ""));
                    postTags.val(postTags.val().replace("academic", ""));
                }

            }else{
                courseInput.prop('disabled', false);
                courseInput.val('');

                if(postTags.val().indexOf("academic") === -1)
                    postTags.val(postTags.val() + " academic");

                postTags.val(postTags.val().replace("office", ""));
                postTags.val(postTags.val().replace("others", ""));
            }
        };
    });

    form.on('submit', function (event) {
        event.preventDefault();

        var data = new FormData($("#form"));

        form.find("input,textarea").each(function(iter, child){
            var allowed = true;

            for(var x in data.keys())
                if(child.name === x)
                    allowed = false;

            if(allowed)
                if(child.type === 'file')
                    data.append(child.name, child.files[0]);
                else
                    data.append(child.name, child.value)

        });
        data.append('ajax', true);

        $.ajax({
            url: '/posts/sell/act/',
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
                        $.each(data.error, function(iter, item){
                            errDiv.innerHTML = "<strong>Error: </strong> " + item;
                            $("#errors").append(errDiv);
                        })
                    }
                }

            }
        });
    })

});