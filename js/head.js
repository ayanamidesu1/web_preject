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

$(document).ready(function(){
    var show_btn = $(".show_more_dropdown_content_more_content_btn");
    var mainpage = $(".show_more_dropdown_content_more_content");
    var ico=$("#dropdown_show_more_btn");
    var text=$(".show_more_dropdown_content_more_content_btn");
    var hidden_btn=$(".show_more_dropdown_content_more_content_hidden");
    
    show_btn.click(function(event){
        event.stopPropagation(); // 阻止事件冒泡
        mainpage.slideToggle(200);
        show_btn.css("display","none");
        ico.css("display","none");
    });
    ico.click(function(event){
        event.stopPropagation();
        mainpage.slideToggle(200);
        show_btn.css("display","none");
        ico.css("display","none");
    });

    $(document).click(function(event){
        if (!$(event.target).closest('.show_more_dropdown_content_more_content').length ||$(event.target).closest(".show_more_dropdown_content_more_content_hidden").length) {
            mainpage.slideUp(200);
            show_btn.css("display","flex");
            ico.css("display","flex");
        }
    });
});




$(document).ready(function() {
    var mainpage = $(".show_more_dropdown");
    var show_btn = $("#show_more_btn");
    var animationDuration = 300; // 动画持续时间，单位毫秒
    var isAnimating = false;

    function animate(startMargin, endMargin, callback) {
        mainpage.animate({marginLeft: endMargin + '%'}, {
            duration: animationDuration,
            progress: function() {
                isAnimating = true;
            },
            complete: function() {
                isAnimating = false;
                if (callback) {
                    callback();
                }
            }
        });
    }

    show_btn.click(function() {
        if (mainpage.css('display') === 'none' || parseInt(mainpage.css('marginLeft'), 10) === -100) {
            // 展开动画
            mainpage.css('display', 'block');
            animate(-100, 0);
        } else if (!isAnimating) {
            // 收起动画
            animate(0, -100, function() {
                mainpage.css('display', 'none');
            });
        }
    });

    $(document).click(function(event) {
        var target = $(event.target);
        // 检查点击的目标元素是否是按钮或下拉框的子元素
        if (!target.is(show_btn) && !target.closest('.show_more_dropdown').length) {
            if (!isAnimating) {
                animate(0, -100, function() {
                    mainpage.css('display', 'none');
                });
            }
        }
    });
});


$(document).ready(function() {
    var switch_btn = $(".avatar_btn");
    var mainpage = $(".avatar_subpage");
    var animationDuration = 300; // 动画持续时间，单位毫秒
    var isAnimating = false;

    function animate(startMargin, endMargin, callback) {
        mainpage.stop().animate({marginTop: endMargin}, {
            duration: animationDuration,
            progress: function() {
                isAnimating = true;
            },
            complete: function() {
                isAnimating = false;
                if (callback) {
                    callback();
                }
            }
        });
    }

    switch_btn.click(function() {
        if (mainpage.css("display") === "none" || parseInt(mainpage.css("marginTop"), 10) <= -mainpage.outerHeight()) {
            // 展开动画
            mainpage.css("display", "block").css("marginTop", -mainpage.outerHeight());
            animate(-mainpage.outerHeight(), 0);
        } else if (!isAnimating) {
            // 收起动画
            animate(0, -mainpage.outerHeight(), function() {
                mainpage.css("display", "none");
            });
        }
    });

    $(document).click(function(event) {
        if (!$(event.target).closest('.avatar_btn, .avatar_subpage').length && !isAnimating) {
            animate(0, -mainpage.outerHeight(), function() {
                mainpage.css("display", "none");
            });
        }
    });
});

//跳转部分
document.addEventListener("DOMContentLoaded",function(){
    var head_icon=document.querySelector(".head_icon");
    head_icon.addEventListener("click",function(){
        window.location.href="http://127.0.0.1:8888";
    });
});