var data={msg1:"test1",msg2:"test2",msg3:"test3"};
var vm=new Vue({
    el:".test",
    data:data
})
document.write(vm.msg1===data.msg1);
document.write("<br>");
vm.msg2="测试二";
document.write(vm.msg2);
document.write("<br>");
data.msg3="测试三"
document.write(vm.msg3);