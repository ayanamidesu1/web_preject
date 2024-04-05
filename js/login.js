var socket = new WebSocket("ws://localhost:8888/websocket");

// 当连接建立时执行的函数
socket.onopen = function(event) {
    console.log("WebSocket 连接已建立");
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    // 将用户名和密码发送给服务器
    
};

// 当接收到消息时执行的函数
socket.onmessage = function(event) {
    console.log("收到消息：" + event.data);
};

// 当连接关闭时执行的函数
socket.onclose = function(event) {
    console.log("WebSocket 连接已关闭");
};

document.addEventListener('DOMContentLoaded',function(event){
    var login = document.getElementById("login");
    login.addEventListener('click',function(event){
        var username = document.getElementById("username").value;
        var password = document.getElementById("password").value;
        var message = {
            username: username,
            password: password
        };
        socket.send(JSON.stringify(message));
    });
});

socket.onmessage = function(event) {
    var data=JSON.parse(event.data);
    if(data.status=="success"){
        window.location.href = "http://127.0.0.1:8888";
        alert("登录成功");
    }else{
        alert("用户名或密码错误");
        return 0;
    }
};

document.addEventListener("DOMContentLoaded", function() {
    var login_btn = document.getElementById("login");
    var password = document.getElementById("password");
    var username = document.getElementById("username");
    
    // 添加输入框的输入事件监听器
    username.addEventListener("input", checkInputValues);
    password.addEventListener("input", checkInputValues);
    
    // 页面加载时立即检查一次输入框的值
    checkInputValues();
});

// 检查输入框的值并更新登录按钮的背景颜色
function checkInputValues() {
    var login_btn = document.getElementById("login");
    var password = document.getElementById("password");
    var username = document.getElementById("username");
    
    if (password.value.trim() !== "" && username.value.trim() !== ""&& password.value.length>=6&&username.value.length>=2) {
        login_btn.style.backgroundColor = "rgba(0, 150, 253, 1)";
        login_btn.style.pointerEvents = "auto";
    } else {
        login_btn.style.pointerEvents = "none";
        login_btn.style.backgroundColor = "rgba(0, 150, 250, 0.5)";
    }
}





