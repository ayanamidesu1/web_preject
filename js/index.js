document.addEventListener('DOMContentLoaded', function() {
  var button = document.getElementById('submission');
  var dropdown = document.getElementById('dropdown_1');

  button.addEventListener('click', function(event) {
    event.stopPropagation(); // 防止点击按钮时冒泡关闭下拉菜单
    toggleDropdown();
  });

  function toggleDropdown() {
    var computedStyle = window.getComputedStyle(dropdown);
    if (computedStyle.display === 'block') {
      dropdown.style.display = 'none';
      // 移除文档的点击事件监听器
      document.removeEventListener('click', closeDropdown);
    } else {
      dropdown.style.display = 'block';
      // 在文档中添加点击事件监听器，以便在用户点击除下拉列表以外的地方时关闭下拉列表
      document.addEventListener('click', closeDropdown);
    }
  }

  function closeDropdown(event) {
    var targetElement = event.target;
    // 检查用户是否点击了下拉列表之外的其他元素
    if (!dropdown.contains(targetElement) && targetElement !== button) {
      dropdown.style.display = 'none';
      // 移除文档的点击事件监听器
      document.removeEventListener('click', closeDropdown);
    }
  }
});
//用户下拉列表
document.addEventListener('DOMContentLoaded', function() {
  var button = document.getElementById('user_avatar_1');
  var dropdown = document.querySelector('.user_dropdown');

  button.addEventListener('click', function(event) {
    event.stopPropagation(); 
    toggleUserDropdown();
  });
  document.addEventListener('click', closeUserDropdown);
  function toggleUserDropdown() {
    if (dropdown.style.display === 'block') {
      dropdown.style.display = 'none';
    } else {
      dropdown.style.display = 'block';
    }
  }
  function closeUserDropdown(event) {
    var target = event.target;
    if (target !== button && !dropdown.contains(target)) {
      dropdown.style.display = 'none';
    }
  }
});
//切换页面
function chosepage(button) {
  var tag = button.getAttribute("tag-value");

  // 遍历所有按钮，重置样式
  document.querySelectorAll('.select_category_subitem button').forEach(function(btn) {
    btn.style.borderTop = '';
  });

  // 设置选定的按钮样式
  button.style.borderTop = '5px solid rgba(53,160,237,1.00)';

  // 设置页面显示与隐藏
  document.getElementById("page_1").style.display = tag === "插画" ? "block" : "none";
  document.getElementById("page_2").style.display = tag === "漫画" ? "block" : "none";
  document.getElementById("page_3").style.display = tag === "小说" ? "block" : "none";
}





function scrollTabs(distance) {//标签滚动
    const tabBar = document.querySelector('.tab-bar');
    tabBar.scrollBy({ left: distance, behavior: 'smooth' });
  }

function scrollTabs1(distance) {//推荐栏滚动
  const container = document.getElementById('follow_page_3');
  if(container) {
      container.scrollBy({ left: distance, behavior: 'smooth' });
  } else {
      console.error('Container element not found');
  }
}



