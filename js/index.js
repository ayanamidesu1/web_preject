function scrollTabs(distance) {
    const tabBar = document.querySelector('.tab-bar');
    tabBar.scrollBy({ left: distance, behavior: 'smooth' });
  }
  function scrollTabs1(distance) {
    const tabBar = document.querySelector('.follow_user_works');
    tabBar.scrollBy({ left: distance, behavior: 'smooth' });
  }

function scrollLeft() {  
    const container = document.querySelector('.follow_user_works');  
    container.scrollLeft -= 200;
}
function scrollRight() {  
    const container = document.querySelector('.follow_user_works');  
    container.scrollLeft += 200; 
}