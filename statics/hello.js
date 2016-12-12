var say_hello = function(msg) {
    alert(msg);
}

$(document).ready(function() {
    /*$.ajax({
        url: '/photos/',
        method: "GET",
        dataType: "json"
    }).done(function(data){
        console.log(data);
    }).fail(function(data){
        console.log('으앙, 안됨');
    });
    */
    $.getJSON("/photos/", function(data){
        console.log(data);
    });

    $('#filter_nav button').on('click', function(e) {
        var value = $(this).val();

        $('#preview').vintage({
            mime: 'image/png'
        }, vintagePresets[value]);
        return false;
    });

    $('#form-post').on('submit', function(e) {
        var image = $('#preview').attr('src');
        if ( image ) {
            $('input[name="filtered_image"]').val(image);
        }
        else {
            $('input[name="filtered_image"]').val('');
        }
    });

    $('#id_image').on('change', function(e) {
        var reader = new FileReader();

        reader.onerror = function(e) { console.log(e); }
        reader.onloadend = function(e) {
            if ( (/^data\:image\/(png);base64/i).test(e.target.result) ) {
                $('#preview').attr('src', e.target.result);
            }
            else {
                alert('사진을 가져오지 못했거나 허용된 이미지 형식이 아님');
            }
        }

        reader.readAsDataURL(this.files[0]);
    });

});
