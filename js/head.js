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
    var show_btn=$(".show_more_dropdown_content_more_content_btn");
    var mainpage=$(".show_more_dropdown_content_more_content");
    var hidden_btn=(".show_more_dropdown_content_more_content_hidden");
    show_btn.click(function(){
        mainpage.slideToggle(200);
    });
    $(document).click(function(event){
        if(!$(event.target).closest('.show_more_dropdown_content_more_content').length)
        {
            mainpage.slideUp(200);
        }
    });
});


document.addEventListener("DOMContentLoaded", function() {  
    var mainpage = document.querySelector(".show_more_dropdown");  
    var show_btn = document.getElementById("show_more_btn");  
    var animationDuration = 300; // 动画持续时间，单位毫秒  
    var isAnimating = false;  
  
    function animate(startMargin, endMargin, callback) {  
        var start = null;  
        var initialMarginLeft = startMargin;  
  
        function step(timestamp) {  
            if (!start) start = timestamp;  
            var progress = timestamp - start;  
            var percentage = Math.min(progress / animationDuration, 1);  
            var newMarginLeft = initialMarginLeft + (endMargin - initialMarginLeft) * percentage;  
            mainpage.style.marginLeft = newMarginLeft + '%';  
  
            if (percentage < 1) {  
                window.requestAnimationFrame(step);  
            } else {  
                if (callback) {  
                    callback();  
                }  
            }  
        }  
  
        window.requestAnimationFrame(step);  
    }  
  
    show_btn.addEventListener("click", function() {  
        if (mainpage.style.display === "none" || parseInt(mainpage.style.marginLeft, 10) === -100) {  
            // 展开动画  
            mainpage.style.display = "block";  
            animate(-100, 0, function() {  
                isAnimating = false;  
            });  
            isAnimating = true;  
        } else if (!isAnimating) {  
            // 收起动画  
            animate(0, -100, function() {  
                mainpage.style.display = "none";  
                isAnimating = false;  
            });  
            isAnimating = true;  
        }  
    });  
  
    document.addEventListener('click', function(event) {  
        var target = event.target;  
  
        while (target != null) {  
            if (target === show_btn || target.classList.contains("show_more_dropdown")) {  
                return;  
            }  
            target = target.parentElement;  
        }  
  
        if (!isAnimating) {  
            // 如果点击了页面其他部分，则执行收起动画  
            animate(0, -100, function() {  
                mainpage.style.display = "none";  
            });  
            isAnimating = true;  
        }  
    });  
});

document.addEventListener("DOMContentLoaded", function() {  
    var switch_btn = document.querySelector(".avatar_btn");  
    var mainpage = document.querySelector(".avatar_subpage");  
    var animationDuration = 300; // 动画持续时间，单位毫秒  
    var isAnimating = false;  
  
    function animate(startMargin, endMargin, callback) {  
        var start = null;  
        var initialMarginTop = startMargin;  
  
        function step(timestamp) {  
            if (!start) start = timestamp;  
            var progress = timestamp - start;  
            var percentage = Math.min(progress / animationDuration, 1);  
            var newMarginTop = initialMarginTop + (endMargin - initialMarginTop) * percentage;  
            mainpage.style.marginTop = newMarginTop + 'px'; // 修改为px单位，假设您想要以像素为单位进行动画  
  
            if (percentage < 1) {  
                window.requestAnimationFrame(step);  
            } else {  
                if (callback) {  
                    callback();  
                }  
            }  
        }  
  
        window.requestAnimationFrame(step);  
    }  
  
    switch_btn.addEventListener("click", function() {  
        if (mainpage.style.display === "none" || parseInt(mainpage.style.marginTop, 10) <= -mainpage.offsetHeight) {  
            // 展开动画  
            mainpage.style.display = "block";  
            mainpage.style.marginTop = -mainpage.offsetHeight + 'px'; // 初始设置为完全隐藏在屏幕下方  
            animate(-mainpage.offsetHeight, 0, function() {  
                isAnimating = false;  
            });  
            isAnimating = true;  
        } else if (!isAnimating) {  
            // 收起动画  
            animate(0, -mainpage.offsetHeight, function() {  
                mainpage.style.display = "none";  
                isAnimating = false;  
            });  
            isAnimating = true;  
        }  
    });  
  
    document.addEventListener('click', function(event) {  
        var target = event.target;  
  
        while (target != null) {  
            if (target === switch_btn || target.classList.contains("avatar_subpage")) {  
                return;  
            }  
            target = target.parentElement;  
        }  
        if (!isAnimating) {   
            animate(0, -mainpage.offsetHeight, function() {  
                mainpage.style.display = "none";  
            });  
            isAnimating = true;  
        }  
    });  
});
