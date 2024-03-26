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
//侧边栏显示切换
document.addEventListener('DOMContentLoaded', function() {
  var button = document.getElementById('head_mean');
  var dropdown = document.querySelector('.mean');
  var dropdownMean = document.querySelector('.dropdown_mean'); // 获取第二个下拉框元素
  var button1=document.getElementById('show_more');

  button.addEventListener('click', function(event) {
    event.stopPropagation();
    toggleDropdown();
  });

  document.addEventListener('click', closeDropdown);

  function toggleDropdown() {
    if (dropdown.style.display === 'block') {
      dropdown.style.display = 'none';
    } else {
      dropdown.style.display = 'block';
    }
  }

  function closeDropdown(event) {
    var target = event.target;
    if (target !== button && !dropdown.contains(target)) {
      dropdown.style.display = 'none';
      dropdownMean.style.display = 'none'; // 隐藏第二个下拉框元素
      button1.style.display = 'block';
    }
  }
});


//查看更多按钮展开
document.addEventListener('DOMContentLoaded', function() {
  var button=document.getElementById('show_more');
  var dropdown=document.querySelector('.dropdown_mean');
  button.addEventListener('click', function(event) {
    event.stopPropagation();
    toggleDropdown();
  });
  document.addEventListener('click', closeDropdown);
  function toggleDropdown() {
    if (dropdown.style.display === 'block') {
      button.style.display='none';
      dropdown.style.display = 'none';
        }
    else{
      dropdown.style.display = 'block';
      button.style.display='none';
    }
  }
});

//隐藏更多
document.addEventListener('DOMContentLoaded', function() {
  var button=document.getElementById('hide_title');
  var button1=document.getElementById('show_more');
  var dropdown=document.querySelector('.dropdown_mean');
  button.addEventListener('click', function(event) {
    event.stopPropagation();
    toggleDropdown();
  });
  document.addEventListener('click', closeDropdown);
  function toggleDropdown() {
    if (dropdown.style.display === 'block') {
      dropdown.style.display = 'none';
      button1.style.display='block';
    }
    else{
      dropdown.style.display = 'none';
      button1.style.display='block';
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

//page1
function page_1_fl(distance)
{
  const tabBar = document.querySelector('.follow_user_works');
    tabBar.scrollBy({ left: distance, behavior: 'smooth' });
}

function page_2_fl(distance)
{
  const tabBar = document.querySelector('.follow_user_works_2');
  tabBar.scrollBy({ left: distance, behavior: 'smooth' });
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
function scrollLeft_img2(distance) {
  const container = document.querySelector('.re_novel_work'); // 使用正确的选择器
  if (container) {
    container.scrollBy({ left: distance, behavior: 'smooth' });
  } else {
    console.log('未找到容器元素');
  }
}


//br自动换行
//根据离散值计算每个字的宽度
function getCharWidth(char) {
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');
  const fontSize = window.getComputedStyle(document.body).fontSize;
  const fontFamily = '微软雅黑';
  
  ctx.font = `${fontSize} ${fontFamily}`;
  const metrics = ctx.measureText(char);
  const averageWidth = metrics.width / char.length;
  
  let sumOfSquaredDifferences = 0;
  for (let i = 0; i < char.length; i++) {
    const charWidth = ctx.measureText(char[i]).width;
    sumOfSquaredDifferences += Math.pow((charWidth - averageWidth), 2);
  }
  
  const standardDeviation = Math.sqrt(sumOfSquaredDifferences);
  const finalWidth = averageWidth + standardDeviation;
  
  return finalWidth;
}
//获取字符
function getchar(id_value)
{
  var char=document.getElementById(id_value);
  return char;
}
//计算每行最大字数
function maxlingchars(char)
{
  var fiex_width=document.querySelector(".recommendation_novel");
  var fiex_width_num=fiex_width.offsetWidth;
  var char_width=getCharWidth(getchar(char).innerText);
  return Math.ceil(fiex_width_num/char_width-1);
}
//自动换行
function autowrap(id_value) {
  var char="edit_message_info";
  for(var j=1;true;j++){
    char="edit_message_info";
    char=char+j;
    console.log(char);
    var quit=document.getElementById(char);
    console.log(quit);
    getchar(char);
    if(quit==null)
    {
      break;
    }
  resetContent(char);
  var value = document.getElementById(char).innerText;
  var max_num = maxlingchars(char)-1;
  var count = 0;
  var result = '';

  for (var i = 0; i < value.length; i++) {
    result += value[i];
    count++;

    if (count === max_num) {
      result += '<br>';
      count = 0; // 重置计数器
    }
  }
  document.getElementById(char).innerHTML = result;
}
}

function resetContent(id_value) {
  var originalContent = document.getElementById(id_value).textContent;
  document.getElementById(id_value).innerHTML = originalContent;
}
//自动调用
setInterval(autowrap, 500);

function re_boolean(imgId) {
  var img_src = "file:///H:/web_preject/image/爱心.png";
  var img_src_1 = "file:///H:/web_preject/image/爱心1.png";
  var img_elm = document.getElementById(imgId);
  var src = decodeURI(img_elm.src);

  if (src == img_src) {
    img_elm.src = img_src_1;
    console.log(src+"0");
    console.log(img_src_1);
  } 
  else{
    img_elm.src = img_src;
    console.log(src+"1");
    console.log(img_src);
  }
}







