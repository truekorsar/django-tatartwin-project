
$('.btn-secondary').on('click', function () { //insert tatar letter
     let form =  $('#id_word')
     let val_1 = form.val()
     let max_length = form.attr('maxlength');
     if (val_1.length<max_length){
         let pos = form[0].selectionStart
         let val_2 = form.val().slice(0,pos)+$(this).text()+form.val().slice(pos)
         form.val(val_2)
         form[0].selectionStart=pos+1
     }
})

//hide awaiting gif
function hide_wait() {
    let wait_gif = $('#wait')
    wait_gif.animate({opacity:0},500, function () {
        wait_gif.css('display','block')
    })
}

//clear all info and show awaiting gif before performing AJAX
function before_send(){
    $('#tatar_errors').html('')
    $('#tatar_info').html('')
    let wait_gif = $('#wait')
    wait_gif.css('display','block')
    let wait = wait_gif.offset().top
    wait_gif.animate({opacity:1},100)
    $("html, body").animate({scrollTop:wait}, 1000)
}

//move to info panel when requested not via AJAX
try {
    let block = $("div").is('#description') ? '#description' : '#errors'
    let to_move = $(block).offset().top
    $("html, body").animate({scrollTop: to_move}, 200)
}catch (err) {}

//AJAX request handling
$('#wordform').submit(function (e) {
    e.preventDefault()
    $('#gettatar').attr('disabled', true)
    $("#messages").remove()
    $.ajax({
        url: $(this).attr('action'),
        type: 'GET',
        data: $(this).serialize(),
        cache: false,
        beforeSend: function(){
            before_send()
        },
        success: function (data) {
            hide_wait()
            $('#gettatar').attr('disabled', false)
            let block = data['status'] === 'OK' ? '#tatar_info' : '#tatar_errors'
            $(block).html(data['info'])
            let to_move = $(block).offset().top
            $("html, body").animate({scrollTop:to_move},100)
            let word = $('#id_word').val()
            window.history.pushState('','','?word='+word)

        },

    })
})
