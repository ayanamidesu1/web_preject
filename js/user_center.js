

var vm=new Vue ({
    el:'.main_content',
    data:{
        edit_box_background_color_show:false,
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
        }
    }
})

