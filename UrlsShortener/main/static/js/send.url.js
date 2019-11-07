$('#send_url').on('click', function(e){
    e.preventDefault();
    long_url = $('#long_url').val()
    if(long_url != "") {
        life_span = $('#life_span').val()
        data = {
            long_url: long_url,
            life_span: life_span,
        }
        $.ajax({
            type : "GET",
            url : '/short_url' ,
            data : data,
            success : function(data){
                if (data.req == "200"){
                    $('#short-url').attr("href", data.short_url)
                    $('#short-url').text(data.short_url)
                    $('#label-text').hide("slow")
                    $('#short-url-text').show("slow")
                    $("#long_url").toggleClass("is-invalid", false)
                    $('#long_url').addClass('is-valid')
                    $('#life_span').addClass('is-valid')
                    $('#long_url_feedback').text()
                }
                else{
                    error = "Something went wrong"
                    if(data.req == "411")
                        error = "URL must be longer than 20 characters"
                    if(data.req == "400")
                        error = "Invalid URL"


                    $('#long_url').addClass('is-invalid')
                    $('#life_span').toggleClass('is-valid', false)
                    $('#long_url_feedback').text(error)
                    $('#short-url-text').hide("slow")
                    $('#label-text').show("slow")
                }

            }
        })
    }

})
