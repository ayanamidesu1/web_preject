var socket = new WebSocket("ws://localhost:8888/websocket");

// 当连接建立时执行的函数
socket.onopen = function(event) {
    console.log("WebSocket 连接已建立");
    socket.send("Hello, server!");
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    // 将用户名和密码发送给服务器
    var message = {
        username: username,
        password: password
    };
    socket.send(JSON.stringify(message));
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