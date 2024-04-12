

var vm=new Vue ({
    el:'.main_content',
    data:{
        edit_box_background_color_show:false,
        user_info_box_show:false,
    },
    computed:{
        
    },
    methods:{
        edit_btn:function()
        {
            console.log('test');
            this.edit_box_background_color_show=true;
        },
        hidden_btn:function()
        {
            this.edit_box_background_color_show=false;
        },
        delete_btn:function()
        {
            if(window.confirm('是否删除该图片？')){
                console.log("删除确认");
            }
            else{
                console.log("删除取消");
            }
        },
        done_upload:function(){
            console.log("上传完成");
        },
        upload_img:function(){
            console.log("选择完成");
        },
        close_user_info_box:function(){
            this.user_info_box_show=false;
        },
        open_user_info_box:function(){
            this.user_info_box_show=true;
        }
    }
})

