document.querySelector('.artwork_look_more').addEventListener('click', function(event){
    var text=event.target.innerText;
    console.log(text);
})

//显示更多作品滚动实现
// 第一个滚动容器
const leftBtn = document.querySelector('.artwork_leftbtn');
const rightBtn = document.querySelector('.artwork_rightbtn');
const otherWorkImage = document.querySelector('.other_work_image');

leftBtn.addEventListener('click', function() {
    scrollContainerArtwork(-100);
});

rightBtn.addEventListener('click', function() {
    scrollContainerArtwork(100);
});

function scrollContainerArtwork(scrollOffset) {
    otherWorkImage.scrollBy({ left: scrollOffset, behavior: 'smooth' });
}

// 第二个滚动容器
const leftBtnUser = document.querySelector('.artwork_thumbnail_leftbtn');
const rightBtnUser = document.querySelector('.artwork_thumbnail_rightbtn');

leftBtnUser.addEventListener('click', function() {
    scrollContainerUser(-200);
});

rightBtnUser.addEventListener('click', function() {
    scrollContainerUser(200);
});

function scrollContainerUser(scrollOffset) {
    var otherWorkImageUser = document.querySelector('.artwork_thumbnail_img');
    otherWorkImageUser.scrollBy({ left: scrollOffset, behavior: 'smooth' });
}

var comment_section_input_box_textarea = document.querySelector('.textarea');
var lineHeight = parseInt(window.getComputedStyle(comment_section_input_box_textarea).lineHeight);
var charHeight = 16;
var maxHeight = 300;

comment_section_input_box_textarea.addEventListener('input', function() {
    comment_section_input_box_textarea.style.height = 'auto';
    var scrollHeight = comment_section_input_box_textarea.scrollHeight;
    comment_section_input_box_textarea.style.height = Math.min(scrollHeight - charHeight, maxHeight) + 'px';
});
//回复的查看和收起
document.addEventListener("DOMContentLoaded", function() {  
    var commentSection = document.querySelector(".comment_section");  
    commentSection.addEventListener("click", function(event) {  
        var target = event.target;  
        // 如果点击的是“查看回复”按钮  
        if (target.classList.contains("show_reply")) {  
            var showReplyButton = target;  
            var replyMessage = showReplyButton.nextElementSibling;  
            if (replyMessage) {  
                showReplyButton.style.display = "none";  
                replyMessage.style.display = "block";  
            }  
        }  
        // 如果点击的是“收起回复”按钮  
        else if (target.classList.contains("collapse_reply")) {  
            var collapseReplyButton = target;  
            var replyContainer = collapseReplyButton.closest('.reply_message');  
            if (replyContainer) {  
                var showReplyButton = replyContainer.previousElementSibling;  
                if (showReplyButton && showReplyButton.classList.contains("show_reply")) {  
                    replyContainer.style.display = "none";  
                    showReplyButton.style.display = "block";  
                }  
            }  
        }  
    });  
});
//收藏状态切换
document.addEventListener("DOMContentLoaded", function() {
    var collectionButtons = document.querySelectorAll(".related_artwork_collection");

    collectionButtons.forEach(function(button) {
        button.addEventListener("click", function(event) {
            var target = event.target;

            // 检查点击的是否为相关的按钮元素
            if (target.closest('.related_artwork_collection')) {
                // 切换按钮的显示状态
                var btn1 = this.querySelector('.collection_btn1');
                var btn2 = this.querySelector('.collection_btn2');

                if (btn2.style.display === "none") {
                    btn2.style.display = "block";
                } else {
                    btn2.style.display = "none";
                }
            }
        });
    });
});
document.addEventListener("DOMContentLoaded", function () {  
    var followingButtons = document.querySelectorAll(".following_btn");  
    followingButtons.forEach(function (button) {  
        button.addEventListener("click", function (event) {  
            var btn_text = this.innerText; // 直接使用this来获取按钮的文本  
            if (btn_text == '关注') {  
                this.innerText = '已关注';  
                this.style.backgroundColor = 'rgba(172,172,172,0.8)'; 
            } else if (btn_text == '已关注') {  
                this.innerText = '关注';  
                this.style.backgroundColor = 'rgba(0, 173, 254, 0.8)'; 
            }  
        });  
    });  
});

document.addEventListener("DOMContentLoaded", function() {
    var following_btn=document.querySelectorAll('.artwork_following');
    following_btn.forEach(function(btn){
        btn.addEventListener('click',function(){
            var btn_text=this.innerText;
            if(btn_text=='关注'){
                this.innerText='已关注';
                this.style.backgroundColor='rgba(172,172,172,0.8)';
            }
            else if(btn_text=='已关注'){
                this.innerText='关注';
                this.style.backgroundColor='rgba(0, 173, 254, 0.8)';
            }
        });
    });
}
);

//互动按钮的状态切换
document.addEventListener("DOMContentLoaded", function() {
   var like_btn=document.querySelectorAll('.user_art_work_interaction_like');
   like_btn.forEach(function(btn){
      btn.addEventListener('click',function(){
        var like_img_divs = this.querySelectorAll('.user_art_work_interaction_like_img');
        var like_text_div = this.querySelector('.user_art_work_interaction_like_text');
        // 切换图片的显示状态
        like_img_divs.forEach(function(img_div) {
            if (img_div.style.display === 'block') {
                img_div.style.display = 'none';
            } else {
                img_div.style.display = 'block';
            }
        });
        // 根据第一张图片是否显示来决定是否要设置文字样式
        if (like_img_divs[0].style.display === 'block') {
            like_text_div.style = '';
        } else {
            like_text_div.style.color = 'rgba(12, 138, 241, 1)';
        }
      });
   });
});

document.addEventListener("DOMContentLoaded", function() {
    var collection_btns = document.querySelectorAll('.user_art_work_interaction_collection');
    
    collection_btns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            var second_img_div = this.querySelector('.user_art_work_interaction_collection_img:nth-child(2)');

            // 切换第二张图片的显示状态
            if (second_img_div.style.display === 'block' || second_img_div.style.display === '') {
                second_img_div.style.display = 'none';
            } else {
                second_img_div.style.display = 'block';
            }
        });
    });
});
// 复制链接按钮点击事件
document.addEventListener("DOMContentLoaded", function() {  
    var copylink_btn = document.querySelector('.user_art_work_interaction_collection_img_copylink');  
    copylink_btn.addEventListener('click', function() {  
        var page_link = window.location.href;  
          
        // 使用 Clipboard API 复制文本到剪贴板  
        navigator.clipboard.writeText(page_link)  
            .then(function() {  
                alert('链接已复制'); 
            })  
            .catch(function(error) {  
                console.error('复制链接时出错:', error);  
                alert('复制链接失败，请手动复制。'); 
            });  
    });  
});

//分享按钮下拉列表
document.addEventListener("DOMContentLoaded", function() {
    var share_btn = document.querySelector('.user_art_work_interaction_share_img');
    var share_dropdown = document.querySelector('.user_art_work_interaction_collection_img_dropdown');

    share_btn.addEventListener('click', function(event) {
        event.stopPropagation(); 
        toggleDropdown();
    });

    // 点击其他位置时隐藏下拉列表
    document.addEventListener('click', function(event) {
        var target = event.target;
        if (!target.closest('.user_art_work_interaction_share')) {
            share_dropdown.style.display = 'none';
        }
    });
    // 切换下拉列表的显示状态
    function toggleDropdown() {
        if (share_dropdown.style.display === 'block') {
            share_dropdown.style.display = 'none';
        } else {
            share_dropdown.style.display = 'block';
        }
    }
});
document.addEventListener("DOMContentLoaded", function() {  
    var copylink_btn = document.getElementById('user_art_work_interaction_collection_img_copylink');  
    copylink_btn.addEventListener('click', function() {  
        var page_link = window.location.href;  
          
        // 使用 Clipboard API 复制文本到剪贴板  
        navigator.clipboard.writeText(page_link)  
            .then(function() {  
                alert('链接已复制'); 
            })  
            .catch(function(error) {  
                console.error('复制链接时出错:', error);  
                alert('复制链接失败，请手动复制。'); 
            });  
    });  
});

document.addEventListener("DOMContentLoaded", function() {
    var share_btn = document.getElementById('user_art_work_interaction_share_img');
    var share_dropdown = document.getElementById('user_art_work_interaction_collection_img_dropdown');

    share_btn.addEventListener('click', function(event) {
        event.stopPropagation(); 
        toggleDropdown();
    });

    // 点击其他位置时隐藏下拉列表
    document.addEventListener('click', function(event) {
        var target = event.target;
        if (!target.closest('.user_art_work_interaction_share')) {
            share_dropdown.style.display = 'none';
        }
    });
    // 切换下拉列表的显示状态
    function toggleDropdown() {
        if (share_dropdown.style.display === 'block') {
            share_dropdown.style.display = 'none';
        } else {
            share_dropdown.style.display = 'block';
        }
    }
});



//查看更多按钮的显示切换以及功能实现
document.addEventListener("DOMContentLoaded", function() {
    var hiddenElement = document.querySelector('.user_art_work_hidden');
    var moreButton = document.querySelector('.artwork_look_more');

    // 检查图片元素的数量并设置按钮的显示状态
    function checkImageCount() {
        var imageCount = hiddenElement.querySelectorAll('img').length;
        if (imageCount === 0) {
            moreButton.style.display = 'none';
        } else {
            moreButton.style.display = '';
        }
    }

    // 页面加载时检查图片元素的数量
    checkImageCount();

    // 当有图片元素被添加或移除时重新检查图片数量
    var observer = new MutationObserver(checkImageCount);
    observer.observe(hiddenElement, { childList: true });

});
document.addEventListener("DOMContentLoaded", function() {
    var showMoreTexts = document.querySelectorAll('.artwork_look_more');
    var hiddenElements = document.querySelectorAll('.user_art_work_hidden');
    var interactive_btn1 = document.querySelector('.user_art_work_interaction');
    var interactive_btn2 = document.getElementById('user_art_work_interaction');
    // 点击show_more_artwork_text元素时隐藏artwork_look_more元素
    showMoreTexts.forEach(function(showMoreText) {
        showMoreText.addEventListener('click', function() {
            var artworkLookMore = document.querySelector('.artwork_look_more');
            if (artworkLookMore) {
                artworkLookMore.style.display = 'none';
            }
            // 清除所有user_art_work_hidden元素的display属性
            hiddenElements.forEach(function(hiddenElement) {
                hiddenElement.removeAttribute('style');
            });
            // 隐藏第一个交互按钮，显示第二个交互按钮
            if (interactive_btn1) {
                interactive_btn1.style.display = 'none';
            }
            if (interactive_btn2) {
                interactive_btn2.style.display = '';
            }
        });
    });
});
document.addEventListener("DOMContentLoaded", function(){
    var dropdown_btn = document.querySelector('.float_interactive_share');
    var dropdown_content = document.querySelector('.float_interactive_share_box'); // 添加一个点以指定类选择器
    dropdown_btn.addEventListener('click', function(){
        if(dropdown_content.style.display == 'none') {
            dropdown_content.style.display = 'block';
        } else {
            dropdown_content.style.display = 'none';
        }
    });
});
document.addEventListener("DOMContentLoaded", function() {  
    var copylink_btn = document.querySelector('.float_interactive_share_box_copylink');  
    copylink_btn.addEventListener('click', function() {  
        var page_link = window.location.href;  
          
        // 使用 Clipboard API 复制文本到剪贴板  
        navigator.clipboard.writeText(page_link)  
            .then(function() {  
                alert('链接已复制'); 
            })  
            .catch(function(error) {  
                console.error('复制链接时出错:', error);  
                alert('复制链接失败，请手动复制。'); 
            });  
    });  
});
//滚动显示操作
 // 检查条件并执行特定操作
 document.addEventListener("DOMContentLoaded", function(){
    var userArtWorkHidden = document.querySelector('.user_art_work_hidden');
    // 创建 MutationObserver 实例
    var observer = new MutationObserver(function(mutationsList, observer) {
        // 检查每个变化
        for(var mutation of mutationsList) {
            if (mutation.type === 'attributes' && mutation.attributeName === 'style') {
                // 获取元素样式
                var computedStyle = window.getComputedStyle(userArtWorkHidden);
                var displayStyle = computedStyle.getPropertyValue('display');
                var imgElements = userArtWorkHidden.querySelectorAll('img');
                if (imgElements.length >= 1 && displayStyle !== 'none') {
                    console.log('条件满足，执行操作');
                    // 执行操作
                    var floatInteractive = document.querySelector('.float_interactive');
                    var lastScrollTop = 0;
                    var isAnimatingUp = false;
                    function handleScroll() {
                        var currentScrollTop = window.scrollY;
                        if (currentScrollTop > lastScrollTop) {
                            // Scroll down
                            isAnimatingUp = false;
                            floatInteractive.style.display = 'none';
                        } else {
                            // Scroll up
                            isAnimatingUp = true;
                            floatInteractive.style.display = 'flex';
                            floatInteractive.style.animation = 'slideUp 0.5s forwards';
                        }
                        lastScrollTop = currentScrollTop;
                    }
                    window.addEventListener('scroll', handleScroll);
                }
            }
        }
    });
    // 配置 MutationObserver 监视属性变化
    observer.observe(userArtWorkHidden, { attributes: true });
});

//浮动栏的显示切换
document.addEventListener("DOMContentLoaded",function(){
    var float_tab=document.querySelector('.float_interactive_like');
    float_tab.addEventListener('click',function(){
        var svg1=document.querySelector('.float_interactive_like_svg_1');
        var svg2=document.querySelector('.float_interactive_like_svg_2');
        var float_interactive_like_text=document.querySelector('.float_interactive_like_text');
       if(svg1.style.display=='none')
       {
           svg1.style.display='block';
           svg2.style.display='none';
           float_interactive_like_text.style.color= '';
        } 
        else{
            svg1.style.display='none';
            svg2.style.display='block';
            float_interactive_like_text.style.color= 'rgba(12, 138, 241,1)';
        }
    });
});
document.addEventListener("DOMContentLoaded", function(){
    var float_tab = document.querySelector('.float_interactive_collection');
    float_tab.addEventListener('click', function(){
        var svg1 = document.querySelector('.float_interactive_collection_svg_1');
        var svg2 = document.querySelector('.float_interactive_collection_svg_2');

        if (svg1.style.display === 'none') {
            svg1.style.display = 'block';
            svg2.style.display = 'none';
        } else {
            svg1.style.display = 'none';
            svg2.style.display = 'block';
        }
    });
});

















