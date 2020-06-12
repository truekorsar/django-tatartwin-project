$('.btn-secondary').on('click', function () {
     let form =  $('#id_word')
     let val_1 = form.val();
     let max_length = form.attr('maxlength');
     if (val_1.length<max_length){
         let pos = form[0].selectionStart;
         let val_2 = form.val().slice(0,pos)+$(this).text()+form.val().slice(pos);
         form.val(val_2);
         form[0].selectionStart=pos+1;
     }
})

function has_word() {
    let url = new URL(window.location.href);
    return url.searchParams.get('word') !== null;
}

function hide_wait() {
    let wait_gif = $('#wait');
    wait_gif.animate({opacity:0},100, function () {
        wait_gif.css('display','block');
    });
}

function before_send(){
    let wait_gif = $('#wait');
    wait_gif.css('display','block');
    wait_gif.animate({opacity:1},100);
    let wait = wait_gif.offset().top;
    $("html, body").animate({scrollTop:wait}, 200);
}

$(document).ready(function () {
    if($("div").is('#description')){
        let desc = $('#description').offset().top;
        $("html, body").animate({scrollTop:desc},200);
    }
    if($("div").is('#errors')){
        let errors = $('#tatar_errors').offset().top;
        $("html, body").animate({scrollTop:errors},200);
    }

    $('#wordform').submit(function (e) {
        e.preventDefault();
        $('#gettatar').attr('disabled', true);
        $("#messages").remove();
        $.ajax({
            url: $(this).attr('action'),
            type: 'GET',
            data: $(this).serialize(),
            cache: false,
            beforeSend: function(){
                $('#tatar_errors').html('');
                $('#tatar_info').html('');
                before_send();
        },
            success: function (data) {
                $('#gettatar').attr('disabled', false);
                if (data['status'] === 'OK'){
                    $('#tatar_info').html(data['info']);
                    let desc = $('#description').offset().top;
                    $("html, body").animate({scrollTop:desc},100);
                }else{
                    $('#tatar_errors').html(data['info']);
                    let errors = $('#tatar_errors').offset().top;
                    $("html, body").animate({scrollTop:errors},100);
                }
                let word = $('#id_word').val();
                window.history.pushState('','','?word='+word);
                hide_wait();

            }
        })
    })

})

