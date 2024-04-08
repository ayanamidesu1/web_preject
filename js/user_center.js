//标题栏部分
$(document).ready(function() {
    var mainpage = $(".more_work");
    var dropdown = $(".more_work_dropdown");

    mainpage.click(function() {
        dropdown.slideToggle(200);
    });

    $(document).click(function(event) {
        if (!$(event.target).closest('.more_work').length && !$(event.target).closest('.more_work_dropdown').length) {
            dropdown.slideUp(200);
        }
    });
});


