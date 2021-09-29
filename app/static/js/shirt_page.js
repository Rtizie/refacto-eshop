var selectName = $('select').attr('name');

// add a hidden element with the same name as the select
var hidden = $('<input type="hidden" name="'+selectName+'">');
hidden.val($('select').val());
hidden.insertAfter($('select'));

$("select option").unwrap().each(function() {
    var btn = $('<div class="size">'+$(this).text()+'</div>');
    if($(this).is(':checked')) btn.addClass('on');
    $(this).replaceWith(btn);
});

$(document).on('click', '.size', function() {
    $('.size').removeClass('on');
    $(this).addClass('on');
    $('input[name="'+selectName+'"]').val($(this).text());
});