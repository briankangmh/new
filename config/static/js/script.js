$(function(){
    new WOW().init();
})

$(window).on('load',function (event) {
    $('.section-container').css('padding-top', $('header')[0].offsetHeight);
});

$(window).scroll(function (event) {
    $('.section-container').css('padding-top', $('header')[0].offsetHeight);
    if ($(window).scrollTop() > 100) {
        $('.header').addClass('active-navigation');
    }
    else {
        $('.header').removeClass('active-navigation')
    }
}).scroll();

$(window).resize(function (event) {
    $('.section-container').css('padding-top', $('header')[0].offsetHeight);
}).resize();
