document.querySelector('.artwork_look_more').addEventListener('click', function (event) {
    var text = event.target.innerText;
    console.log(text);
})

//显示更多作品滚动实现
// 第一个滚动容器
const leftBtn = document.querySelector('.artwork_leftbtn');
const rightBtn = document.querySelector('.artwork_rightbtn');
const otherWorkImage = document.querySelector('.other_work_image');

leftBtn.addEventListener('click', function () {
    scrollContainerArtwork(-100);
});

rightBtn.addEventListener('click', function () {
    scrollContainerArtwork(100);
});

function scrollContainerArtwork(scrollOffset) {
    otherWorkImage.scrollBy({ left: scrollOffset, behavior: 'smooth' });
}

// 第二个滚动容器
const leftBtnUser = document.querySelector('.artwork_thumbnail_leftbtn');
const rightBtnUser = document.querySelector('.artwork_thumbnail_rightbtn');

leftBtnUser.addEventListener('click', function () {
    scrollContainerUser(-200);
});

rightBtnUser.addEventListener('click', function () {
    scrollContainerUser(200);
});

function scrollContainerUser(scrollOffset) {
    var otherWorkImageUser = document.querySelector('.artwork_thumbnail_img');
    otherWorkImageUser.scrollBy({ left: scrollOffset, behavior: 'smooth' });
}
//评论的回复
var commentSectionTextareas = document.querySelectorAll('.comment_section .textarea');
var lineHeight = parseInt(window.getComputedStyle(commentSectionTextareas[0]).lineHeight);
var charHeight = 16;
var maxHeight = 300;

commentSectionTextareas.forEach(function (textarea) {
    textarea.addEventListener('input', function () {
        textarea.style.height = 'auto';
        var scrollHeight = textarea.scrollHeight;
        if (textarea.value.trim() === '') {
            textarea.style.height = '20px'; // 如果内容为空，将高度设置为 18px
        } else {
            textarea.style.height = Math.min(scrollHeight - charHeight, maxHeight) + 'px';
        }
    });
});


// 定义回复按钮点击事件绑定函数
function bindReplyButtonEvents(reply_button) {
    reply_button.addEventListener('click', function () {
        var reply_box = reply_button.closest('.comment_section_details').querySelector('.reply_message_box');
        if (reply_box) {
            if (reply_box.style.display === 'block') {
                reply_box.style.display = 'none';
                reply_button.innerHTML = '&nbsp;回复';
            } else {
                reply_box.style.display = 'block';
                reply_button.innerHTML = '&nbsp;收起';
            }
        }
    });
}

// 定义观察器的回调函数

//重新监听的实现
var observerCallback = function (mutationsList, observer) {
    mutationsList.forEach(function (mutation) {
        if (mutation.type === 'childList') {
            mutation.addedNodes.forEach(function (node) {
                if (node.nodeType === Node.ELEMENT_NODE) {
                    // 如果新增节点是.comment_section_details元素
                    if (node.classList.contains('comment_section_details')) {
                        // 获取新增节点内的回复按钮
                        var reply_button = node.querySelector('.comment_section_details_details_reply');
                        if (reply_button) {
                            // 绑定点击事件
                            bindReplyButtonEvents(reply_button);
                        }
                    }
                }
            });
        }
    });
};
// 创建一个观察器实例并传入回调函数
var observer = new MutationObserver(observerCallback);
var targetNode = document.querySelector('.comment_section');
var observerConfig = { childList: true, subtree: true };
observer.observe(targetNode, observerConfig);

//查看更多评论
document.addEventListener("DOMContentLoaded", function () {
    var showmore_btn = document.querySelectorAll('.comment_section_showmore');
    var more_page = document.querySelectorAll('.comment_section_hideen');
    showmore_btn.forEach(function (showmore_btn, index) {
        showmore_btn.addEventListener('click', function () {
            if (more_page[index].style.display === 'none') {
                more_page[index].style.display = 'block';
                showmore_btn.style.display = 'none';
            }
        });
    });
});

//查看更多的显示逻辑
document.addEventListener("DOMContentLoaded", function () {
    // 定义一个函数，用于检查并隐藏查看更多按钮
    function checkAndHideShowReplyButtons() {
        var main_pages = document.querySelectorAll('.comment_section');
        main_pages.forEach(function (main_page) {
            var subpages = main_page.querySelectorAll('.comment_section_details');
            subpages.forEach(function (subpage) {
                var show_reply_btn = subpage.querySelector('.show_reply');
                var reply_boxes = subpage.querySelectorAll('.reply_message');
                if (reply_boxes.length === 0 && show_reply_btn) {
                    show_reply_btn.style.display = 'none';
                }
            });
        });
    }
    checkAndHideShowReplyButtons();
    var observer = new MutationObserver(function (mutationsList, observer) {
        checkAndHideShowReplyButtons();
    });
    observer.observe(document.documentElement, { childList: true, subtree: true });
});



//回复的查看和收起
/*document.addEventListener("DOMContentLoaded", function() {  
    var commentSections = document.querySelectorAll(".comment_section");  
    commentSections.forEach(function(commentSection) {
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
                    var showReplyButton = replyContainer.querySelector('.show_reply');  
                    if (showReplyButton) {  
                        replyContainer.style.display = "none";  
                        showReplyButton.style.display = "block";  
                    }  
                }  
            }  
        });
    });
});*/
document.addEventListener("DOMContentLoaded", function () {
    var master = document.querySelectorAll('.comment_section');
    master.forEach(function (master) {
        var mainpage = document.querySelectorAll('.comment_section_details');
        mainpage.forEach(function (mainpage, index) {
            var subpage = mainpage.querySelector('.reply_message');
            var showmore = mainpage.querySelector('.show_reply');
            var closepage = mainpage.querySelector('.collapse_reply');
            showmore.addEventListener('click', function () {
                if (subpage.style.display == 'none') {
                    subpage.style.display = 'block';
                    showmore.style.display = 'none';
                    closepage.style.display = 'block';
                }
            });
            closepage.addEventListener('click', function () {
                subpage.style.display = 'none';
                showmore.style.display = 'block';
                closepage.style.display = 'none';
            });
        });
    });
});


//收藏状态切换
document.addEventListener("DOMContentLoaded", function () {
    var collectionButtons = document.querySelectorAll(".related_artwork_collection");

    collectionButtons.forEach(function (button) {
        button.addEventListener("click", function (event) {
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

document.addEventListener("DOMContentLoaded", function () {
    var following_btn = document.querySelectorAll('.artwork_following');
    following_btn.forEach(function (btn) {
        btn.addEventListener('click', function () {
            var btn_text = this.innerText;
            if (btn_text == '关注') {
                this.innerText = '已关注';
                this.style.backgroundColor = 'rgba(172,172,172,0.8)';
            }
            else if (btn_text == '已关注') {
                this.innerText = '关注';
                this.style.backgroundColor = 'rgba(0, 173, 254, 0.8)';
            }
        });
    });
}
);

//互动按钮的状态切换
document.addEventListener("DOMContentLoaded", function () {
    var like_btn = document.querySelectorAll('.user_art_work_interaction_like');
    like_btn.forEach(function (btn) {
        btn.addEventListener('click', function () {
            var like_img_divs = this.querySelectorAll('.user_art_work_interaction_like_img');
            var like_text_div = this.querySelector('.user_art_work_interaction_like_text');
            // 切换图片的显示状态
            like_img_divs.forEach(function (img_div) {
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

document.addEventListener("DOMContentLoaded", function () {
    var collection_btns = document.querySelectorAll('.user_art_work_interaction_collection');

    collection_btns.forEach(function (btn) {
        btn.addEventListener('click', function () {
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
document.addEventListener("DOMContentLoaded", function () {
    var copylink_btn = document.querySelector('.user_art_work_interaction_collection_img_copylink');
    copylink_btn.addEventListener('click', function () {
        var page_link = window.location.href;

        // 使用 Clipboard API 复制文本到剪贴板  
        navigator.clipboard.writeText(page_link)
            .then(function () {
                alert('链接已复制');
            })
            .catch(function (error) {
                console.error('复制链接时出错:', error);
                alert('复制链接失败，请手动复制。');
            });
    });
});

//分享按钮下拉列表
document.addEventListener("DOMContentLoaded", function () {
    var share_btn = document.querySelector('.user_art_work_interaction_share_img');
    var share_dropdown = document.querySelector('.user_art_work_interaction_collection_img_dropdown');

    share_btn.addEventListener('click', function (event) {
        event.stopPropagation();
        toggleDropdown();
    });

    // 点击其他位置时隐藏下拉列表
    document.addEventListener('click', function (event) {
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
document.addEventListener("DOMContentLoaded", function () {
    var copylink_btn = document.getElementById('user_art_work_interaction_collection_img_copylink');
    copylink_btn.addEventListener('click', function () {
        var page_link = window.location.href;

        // 使用 Clipboard API 复制文本到剪贴板  
        navigator.clipboard.writeText(page_link)
            .then(function () {
                alert('链接已复制');
            })
            .catch(function (error) {
                console.error('复制链接时出错:', error);
                alert('复制链接失败，请手动复制。');
            });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    var share_btn = document.getElementById('user_art_work_interaction_share_img');
    var share_dropdown = document.getElementById('user_art_work_interaction_collection_img_dropdown');

    share_btn.addEventListener('click', function (event) {
        event.stopPropagation();
        toggleDropdown();
    });

    // 点击其他位置时隐藏下拉列表
    document.addEventListener('click', function (event) {
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
document.addEventListener("DOMContentLoaded", function () {
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
document.addEventListener("DOMContentLoaded", function () {
    var showMoreTexts = document.querySelectorAll('.artwork_look_more');
    var hiddenElements = document.querySelectorAll('.user_art_work_hidden');
    var interactive_btn1 = document.querySelector('.user_art_work_interaction');
    var interactive_btn2 = document.getElementById('user_art_work_interaction');
    // 点击show_more_artwork_text元素时隐藏artwork_look_more元素
    showMoreTexts.forEach(function (showMoreText) {
        showMoreText.addEventListener('click', function () {
            var artworkLookMore = document.querySelector('.artwork_look_more');
            if (artworkLookMore) {
                artworkLookMore.style.display = 'none';
            }
            // 清除所有user_art_work_hidden元素的display属性
            hiddenElements.forEach(function (hiddenElement) {
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
document.addEventListener("DOMContentLoaded", function () {
    var dropdown_btn = document.querySelector('.float_interactive_share');
    var dropdown_content = document.querySelector('.float_interactive_share_box');
    dropdown_btn.addEventListener('click', function (event) {
        event.stopPropagation(); // 阻止事件冒泡，避免下拉内容被隐藏
        if (dropdown_content.style.display == 'none') {
            dropdown_content.style.display = 'block';
        } else {
            dropdown_content.style.display = 'none';
        }
    });
    // 点击页面其他地方时隐藏下拉内容
    document.addEventListener('click', function (event) {
        var target = event.target;
        if (target !== dropdown_btn && target !== dropdown_content) {
            dropdown_content.style.display = 'none';
        }
    });
    // 点击下拉内容区域内的子元素时阻止事件冒泡
    dropdown_content.addEventListener('click', function (event) {
        event.stopPropagation();
    });
});

document.addEventListener("DOMContentLoaded", function () {
    var copylink_btn = document.querySelector('.float_interactive_share_box_copylink');
    copylink_btn.addEventListener('click', function () {
        var page_link = window.location.href;

        // 使用 Clipboard API 复制文本到剪贴板  
        navigator.clipboard.writeText(page_link)
            .then(function () {
                alert('链接已复制');
            })
            .catch(function (error) {
                console.error('复制链接时出错:', error);
                alert('复制链接失败，请手动复制。');
            });
    });
});
//滚动显示操作
// 检查条件并执行特定操作
document.addEventListener("DOMContentLoaded", function () {
    var userArtWorkHidden = document.querySelector('.user_art_work_hidden');
    // 创建 MutationObserver 实例
    var observer = new MutationObserver(function (mutationsList, observer) {
        // 检查每个变化
        for (var mutation of mutationsList) {
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
document.addEventListener("DOMContentLoaded", function () {
    var float_tab = document.querySelector('.float_interactive_like');
    float_tab.addEventListener('click', function () {
        var svg1 = document.querySelector('.float_interactive_like_svg_1');
        var svg2 = document.querySelector('.float_interactive_like_svg_2');
        var float_interactive_like_text = document.querySelector('.float_interactive_like_text');
        if (svg1.style.display == 'none') {
            svg1.style.display = 'block';
            svg2.style.display = 'none';
            float_interactive_like_text.style.color = '';
        }
        else {
            svg1.style.display = 'none';
            svg2.style.display = 'block';
            float_interactive_like_text.style.color = 'rgba(12, 138, 241,1)';
        }
    });
});
document.addEventListener("DOMContentLoaded", function () {
    var float_tab = document.querySelector('.float_interactive_collection');
    float_tab.addEventListener('click', function () {
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

//消息的发送逻辑

function getdate() {
    var datetime = new Date();
    var year = datetime.getFullYear(); // 获取年份  
    var month = datetime.getMonth() + 1; // 获取月份（注意，月份是从0开始的，所以需要+1）  
    var day = datetime.getDate(); // 获取日  
    var hours = datetime.getHours(); // 获取小时  
    var minutes = datetime.getMinutes(); // 获取分钟  
    var seconds = datetime.getSeconds(); // 获取秒  
    // 为了保证格式统一，当值小于10时在前面补0  
    month = month < 10 ? '0' + month : month;
    day = day < 10 ? '0' + day : day;
    hours = hours < 10 ? '0' + hours : hours;
    minutes = minutes < 10 ? '0' + minutes : minutes;
    seconds = seconds < 10 ? '0' + seconds : seconds;
    // 拼接字符串得到最终的日期时间格式  
    var formattedDateTime = year + '年' + month + '月' + day + '日' + hours + ':' + minutes + ':' + seconds;
    return formattedDateTime;
}

document.addEventListener("DOMContentLoaded", function () {
    var send_btn = document.getElementById('first_sendbtn');
    send_btn.addEventListener('click', function () {
        var input_box = document.getElementById('first_input_box');
        var textarea = input_box.querySelector('textarea');
        var input_text = textarea.value;
        if (input_text === '') {
            console.log('输入不能为空');
            alert('输入不能为空');
            return;
        }
        console.log(input_text + '132');
        var datetime = getdate();
        var ready_addtext = `<div class="comment_section_details">
            <div class="comment_section_details_user">
                <div class="comment_section_details_user_avatar"><img src="image/101092272_p0.jpg"></div>
                <div class="comment_section_details_user_name">
                    <div style="align-self: self-start;">username</div>
                    <div class="comment_section_details_details">${input_text}</div>
                    <div class="comment_section_details_details_time">${datetime}<div
                            class="comment_section_details_details_reply">&nbsp;回复</div>
                    </div>
                    <div class="reply_message_box" style="display:none;">
                        <div class="comment_section_input">
                            <div class="send_user_avatar"><img src="image/101092272_p0.jpg"></div>
                            <div class="comment_section_input_box"><textarea class="textarea" placeholder="发表评论"></textarea>
                            </div>
                            <div class="comment_section_input_sendbtn" id="second_sendbtn"><b>发送</b></div>
                        </div>
                    </div>
                    <div class="show_reply">查看回复</div>
                </div>
            </div>
        </div>`;
        var main_pages = document.querySelectorAll('.comment_section');
        main_pages.forEach(function (page) {
            var first_comment = page.querySelector('.comment_section_details');
            var newElement = document.createElement('div');
            newElement.innerHTML = ready_addtext;
            page.insertBefore(newElement.firstChild, first_comment);
            textarea.value = '';
        });
    });
});

//回复框的展开和收起

//重新为回复添加监听
function relistening() {
    var main = document.querySelectorAll('.comment_section');
    main.forEach(function (main, mian_index) {
        var main_subpage = main.querySelectorAll();
    });
}

//多重循环的视线击事件监听
/*
document.addEventListener("DOMContentLoaded", function () {
    var main_pages = document.querySelectorAll('.comment_section');
    main_pages.forEach(function (main_page) {
        var subpages = main_page.querySelectorAll('.comment_section_details');
        var reply_box = main_page.querySelectorAll('.comment_section_details_details_time'); // 次级发送框
        subpages.forEach(function (subpage) {
            var sub_subpages = subpage.querySelectorAll('.comment_section_details_user');
            sub_subpages.forEach(function (sub_subpage) {
                var reply_message_boxes = sub_subpage.querySelectorAll('.reply_message_box');
                var reply_message_btns = sub_subpage.querySelectorAll('.comment_section_details_details_reply');
                reply_message_btns.forEach(function (reply_btn, index) {
                    reply_btn.addEventListener('click', function () {
                        console.log(reply_btn);
                        var sub_reply_sendbox = reply_message_boxes[index];
                        if (sub_reply_sendbox.style.display === 'none' || sub_reply_sendbox.style.display === '') {
                            sub_reply_sendbox.style.display = 'block';
                            reply_btn.innerHTML = '收起';
                        } else {
                            sub_reply_sendbox.style.display = 'none';
                            reply_btn.innerHTML = '回复';
                        }
                    });
                });
            });
        });
    });
});*/
//已经弃用
/*
document.addEventListener("DOMContentLoaded", function () {
    document.addEventListener('click', function (event) {
        var target = event.target;
        if (target.classList.contains('comment_section_details_details_reply')) {
            var reply_message_box = target.closest('.comment_section_details_user').querySelector('.reply_message_box');
            if (reply_message_box) {
                toggleReplyBox(reply_message_box, target);
            }
        }
    });
    function toggleReplyBox(reply_box, reply_btn) {
        var computedStyle = window.getComputedStyle(reply_box);
        if (computedStyle.display === 'none') {
            reply_box.style.display = 'block';
            reply_btn.innerHTML = '收起';
        } else {
            reply_box.style.display = 'none';
            reply_btn.innerHTML = '回复';
        }
    }
});*/

//次级回复功能的元素增加功能
function subpage_reply() {
    var main_pages = document.querySelectorAll('.comment_section');
    main_pages.forEach(function (main_page) {
        var subpages = main_page.querySelectorAll('.comment_section_details');
        subpages.forEach(function (subpage) {
            var sub_subpages = subpage.querySelectorAll('.comment_section_details_user');
            sub_subpages.forEach(function (sub_subpage) {
                var reply_message_boxes = sub_subpage.querySelectorAll('.reply_message_box');
                reply_message_boxes.forEach(function (reply_message_box) {
                    var send_btn = reply_message_box.querySelector('.comment_section_input_sendbtn');
                    var reply_message_textarea = reply_message_box.querySelector('.comment_section_input_box textarea');
                    send_btn.addEventListener('click', function () {
                        var date = getdate();
                        var reply_message_text = reply_message_textarea.value.trim();
                        if (reply_message_text) {
                            var modle = `<div class="subreply_box">
                                <div class="reply_user_avatar"><img src="image/101779890_p0.jpg"></div>
                                <div class="reply_user_username">
                                    <div class="reply_user_username_details">username</div>
                                    <div class="reply_message_details">${reply_message_text}</div>
                                    <div class="reply_message_details_time">${date}
                                        <div class="reply_message_reply">&nbsp;回复</div>
                                    </div>
                                </div>
                            </div>`;
                            var reply_message = sub_subpage.querySelector('.reply_message_box');
                            var first_subreply_box = reply_message.querySelector('.subreply_box:first-child');
                            if (first_subreply_box) {
                                first_subreply_box.insertAdjacentHTML('beforebegin', modle);
                            } else {
                                reply_message.innerHTML = modle + reply_message.innerHTML;
                            }
                            // 清空文本框
                            reply_message_textarea.value = '';
                        }
                    });
                });
            });
        });
    });
}

// 监控树的变化，为新增的回复按钮添加功能
function subpage_reply_observer(mutationsList, observer) {
    mutationsList.forEach(function (mutation) {
        if (mutation.type === 'childList') {
            mutation.addedNodes.forEach(function (node) {
                if (node.nodeType === Node.ELEMENT_NODE) {
                    var comment_section_input_sendbtn = node.querySelector('.comment_section_input_sendbtn');
                    if (comment_section_input_sendbtn) {
                        comment_section_input_sendbtn.addEventListener('click', subpage_reply);
                    }
                }
            });
        }
    });
}
// 创建一个观察者实例，监控指定节点的子节点变化
var sub_reply_btn_observer = new MutationObserver(subpage_reply_observer);
var sub_reply_btn_targetNode = document.querySelector('.comment_section');
var sub_reply_btn_observerConfig = { childList: true, subtree: true };
sub_reply_btn_observer.observe(sub_reply_btn_targetNode, sub_reply_btn_observerConfig);
//已经弃用
/*
function sub_of_sub_replymsg_sendbtn() {
    var model = `<div class="temp_reply_message">  
        <div class="temp_reply_message_avatar"><img src="image/101092272_p0.jpg"></div>  
        <div class="temp_reply_message_inputbox"><textarea placeholder="输入评论"></textarea></div>  
        <div class="temp_reply_message_sendbtn">发送</div>  
        </div>`;

    document.addEventListener('DOMContentLoaded', function () {
        var main = document.querySelectorAll('.comment_section');
        main.forEach(function (mainElem) {
            var sub_main = mainElem.querySelectorAll('.comment_section_details');
            sub_main.forEach(function (sub_mainElem) {
                var sub_page = sub_mainElem.querySelectorAll('.comment_section_details_user');
                sub_page.forEach(function (sub_pageElem) {
                    var sub_subpage = sub_pageElem.querySelectorAll('.comment_section_details_user_name');
                    sub_subpage.forEach(function (sub_subpageElem) {
                        var reply_message = sub_subpageElem.querySelectorAll('.reply_message');
                        reply_message.forEach(function (reply_messageElem) {
                            var subreply_box = reply_messageElem.querySelectorAll('.subreply_box');
                            subreply_box.forEach(function (subreply_boxElem) {
                                var reply_user_username = subreply_boxElem.querySelectorAll('.reply_user_username');
                                // 为每个.reply_user_username后面的回复按钮添加事件监听器  
                                reply_user_username.forEach(function (reply_user_usernameElem, index) {
                                    var reply_message_send_btn = subreply_boxElem.querySelector('.reply_message_reply');
                                    reply_message_send_btn.addEventListener('click', function () {
                                        var buttonText = reply_message_send_btn.textContent.trim();
                                        console.log('test');
                                        if (buttonText === '回复') {
                                            // 如果按钮文字为回复，则添加模板
                                            var tempdiv = document.createElement('div');
                                            tempdiv.innerHTML = model;
                                            var newReplyBox = tempdiv.firstElementChild;
                                            subreply_boxElem.insertBefore(newReplyBox, reply_user_usernameElem.nextElementSibling);
                                            reply_message_send_btn.textContent = '收起';
                                        } else if (buttonText === '收起') {
                                            // 如果按钮文字为收起，则删除已添加的所有模板
                                            var tempReplyMessages = subreply_boxElem.querySelectorAll('.temp_reply_message');
                                            tempReplyMessages.forEach(function (tempReplyMessage) {
                                                tempReplyMessage.remove();
                                            });
                                            reply_message_send_btn.textContent = '回复';
                                        }
                                    });
                                });
                            });
                        });
                    });
                });
            });
        });
    });
}
sub_of_sub_replymsg_sendbtn();*/

document.addEventListener("DOMContentLoaded", function(){
    var listenpage = document.querySelector('.comment_section');
    var model = `<div class="temp_reply_message">  
        <div class="temp_reply_message_avatar"><img src="image/101092272_p0.jpg"></div>  
        <div class="temp_reply_message_inputbox"><textarea placeholder="输入评论"></textarea></div>  
        <div class="temp_reply_message_sendbtn">发送</div>  
    </div>`;
    listenpage.addEventListener('click', function(event){
        var target = event.target;
        if(target.classList.contains('reply_message_reply')) {
            var parentUser = target.closest('.reply_user_username');
            if(parentUser) {
                var replyBox = parentUser.nextElementSibling;
                if(replyBox && replyBox.classList.contains('temp_reply_message')) {
                    replyBox.remove();
                    target.textContent = '回复';
                } else {
                    var subReplyBox = document.createElement('div');
                    subReplyBox.classList.add('temp_reply_message');
                    subReplyBox.innerHTML = model;
                    parentUser.insertAdjacentElement('afterend', subReplyBox);
                    target.textContent = '收起';
                }
            }
        }
    });
    // 创建 MutationObserver 实例
    var observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            // 检查是否有子节点添加
            if (mutation.addedNodes.length > 0) {
                // 在添加的节点中找到 textarea
                mutation.addedNodes.forEach(function(node) {
                    var textarea = node.querySelector('textarea');
                    if (textarea) {
                        // 绑定 input 事件
                        textarea.addEventListener('input', function () {
                            textarea.style.height = 'auto';
                            var scrollHeight = textarea.scrollHeight;
                            if (textarea.value.trim() === '') {
                                textarea.style.height = '22px'; // 如果内容为空，将高度设置为 22px
                            } else {
                                textarea.style.height = Math.min(scrollHeight - charHeight, maxHeight) + 'px';
                            }
                        });
                    }
                });
            }
        });
    });
    // 监听 .comment_section 的子节点变化
    observer.observe(listenpage, { childList: true, subtree: true });
});

document.addEventListener('DOMContentLoaded', function(){
    var model = `<div class="reply_message_box"><div class="temp_reply_message_box" >
        <div class="comment_section_input">
            <div class="send_user_avatar"><img src="image/101092272_p0.jpg"></div>
            <div class="comment_section_input_box"><textarea class="textarea" placeholder="发表评论"></textarea></div>
            <div class="comment_section_input_sendbtn" id="second_sendbtn"><b>发送</b></div>
        </div>
        </div>
    </div>`;
    var main = document.querySelector('.comment_section');
    main.addEventListener('click', function(event){
        var target = event.target;
        if(target.classList.contains('comment_section_details_details_reply'))
        {
            var parentUser = target.closest('.comment_section_details_details_time');
            console.log(parentUser,target.textContent);
            if (parentUser) {
                var replybtn = parentUser.nextElementSibling;
                if (target.textContent.trim() == '回复') {
                    // 添加模板，作为兄弟元素插入
                    parentUser.insertAdjacentHTML('afterend', model);
                    target.textContent = '收起';
                    console.log(parentUser);
                } else if (target.textContent.trim() == '收起') {
                    // 删除所有模板
                    var replyMessageBoxes = document.querySelectorAll('.temp_reply_message_box');
                    replyMessageBoxes.forEach(function(box) {
                        box.remove();
                    });
                    target.textContent = '回复';
                    console.log(parentUser);
                }
            }
        }
    });
});

document.addEventListener('DOMContentLoaded', function(){
    var main = document.querySelector('.comment_section');
    
    // 创建 MutationObserver 实例，传入回调函数
    var observer = new MutationObserver(function(mutationsList, observer) {
        // 遍历每个变化
        mutationsList.forEach(function(mutation) {
            // 检查是否有节点被添加
            if (mutation.type === 'childList') {
                // 遍历每个添加的节点
                mutation.addedNodes.forEach(function(addedNode) {
                    // 如果添加的节点是临时回复框
                    if (addedNode.classList && addedNode.classList.contains('temp_reply_message')) {
                        // 为发送按钮添加功能
                        var sendBtn = addedNode.querySelector('.temp_reply_message_sendbtn');
                        sendBtn.addEventListener('click', function() {
                            // 处理发送按钮点击事件
                            temp_handleSendButtonClick(addedNode);
                        });
                    }
                });
            }
        });
    });

    // 监听树的变化
    observer.observe(main, { childList: true, subtree: true });
});

// 处理发送按钮点击事件的函数
function temp_handleSendButtonClick(replyBox) {
    var inputText = replyBox.querySelector('textarea').value;
    var datetime = getdate();
    
    // 创建评论模板
    var model = `<div class="subreply_box">
    <div class="reply_user_avatar"><img src="image/101779890_p0.jpg"></div>
    <div class="reply_user_username">
        <div class="reply_user_username_details">username</div>
        <div class="reply_message_details">${inputText}</div>
        <div class="reply_message_details_time">${datetime}
            <div class="reply_message_reply">&nbsp;回复</div>
        </div>
    </div>
</div>`;
    
    // 获取要插入的位置
    var parentUser = replyBox.previousElementSibling;
    // 插入评论模板
    parentUser.insertAdjacentHTML('afterend', model);

    // 清空回复框中的内容
    replyBox.querySelector('textarea').value = '';
    
    // 删除所有的临时输入框
    var replyMessageBoxes = document.querySelectorAll('.temp_reply_message');
    replyMessageBoxes.forEach(function(box) {
        box.remove();
    });
}



















