function displayPost(data){
    var modal = $("#modal");
    var d = data[0];
    console.log(d);

    $.ajax({
        url: '/posts/get/item/',
        method: 'GET',
        data: {id: d.fields.item},
        success: function (data){
            if(data.success){
                var item = JSON.parse(data.item)[0].fields;
                var use = "Office";

                if(item.use === 1)
                    use = "Academic";
                else if(item.use === 2)
                    use = "Other";

                modal.find("#title").empty().append(item.name);
                modal.find("#quantity").empty().append("In Stock: " + item.quantity);
                modal.find("#description").empty().append("Description: " + d.fields.description);
                modal.find("#use").empty().append("Type: For " + use + " Use");

                if(item.use === 1)
                    modal.find("#course").empty().append("Course: " + item.course);
                else
                    modal.find("#course").empty();

                modal.find("#tags").empty().append("Tags: <br/>");
                tags = d.fields.tags;
                tags = tags.split(" ");

                for(i = 0; i < tags.length; i++){
                    modal.find("#tags").append("<a href='/posts/?tags=" + tags[i] + "' class='sub'>" + tags[i] + "</a> ");
                }

                modal.find("#img").attr('src', "/media/" + item.picture);
                $.ajax({
                    url: '/posts/get/user/',
                    method:'GET',
                    data: {id: d.fields.user},
                    success: function (dat){
                        if(dat.success){
                            var user = JSON.parse(dat.user)[0].fields;
                            modal.find("#owner").empty().append("Owner: " + user.name);
                        }
                    }
                });
            }
        }
    });

    modal.fadeIn(250);
}

function goToUser(link){
    var email = link.innerHTML;

    window.location.href = "/users/view/?email=" + email;
}

$(document).ready(function(){
    $("#close").on('click', function(){
        $("#modal").fadeOut(250);
    });
});