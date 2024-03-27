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
