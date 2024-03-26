document.querySelector('.artwork_look_more').addEventListener('click', function(event){
    var text=event.target.innerText;
    console.log(text);
})

//显示更多作品滚动实现
const leftBtn = document.querySelector('.artwork_leftbtn');
    const rightBtn = document.querySelector('.artwork_rightbtn');
    const otherWorkImage = document.querySelector('.other_work_image');

    leftBtn.addEventListener('click', function() {
        scrollContainer(-100);
    });

    rightBtn.addEventListener('click', function() {
        scrollContainer(100);
    });

    function scrollContainer(scrollOffset) {
        otherWorkImage.scrollBy({ left: scrollOffset, behavior: 'smooth' });
    }