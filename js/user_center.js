var model=`<div class="edit_userinfo_box_contact_information_text">
<div class="edit_userinfo_box_contact_information_text_fun">
    <input placeholder="请输入联系方式">
</div>
<div class="edit_userinfo_box_contact_information_text_choose">
    <select>
        <option>
            <div class="edit_userinfo_box_contact_information_text_choose_box">
                <div class="edit_userinfo_box_contact_information_text_choose_ico">
                    <svg t="1712890771404" class="icon" viewBox="0 0 1025 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2340"
                        width="200" height="200">
                        <path
                            d="M483.84768 867.808C466.37568 885.792 441.73568 896 415.87968 896 390.05568 896 365.41568 885.792 347.94368 867.808L27.46368 547.552C-9.17632 508.864-9.17632 450.336 27.46368 411.648 44.26368 394.944 67.30368 385.088 91.68768 384.256 118.72768 383.008 144.93568 393.024 163.46368 411.648L415.87968 664 860.61568 219.552C878.31168 201.952 902.88768 192 928.58368 192 954.24768 192 978.82368 201.952 996.51968 219.552 1033.15968 258.208 1033.15968 316.704 996.51968 355.36L483.84768 867.808Z"
                            p-id="2341"></path>
                    </svg>
                </div>
                <div class="edit_userinfo_box_contact_information_text_choose_text">QQ</div>
            </div>
        </option>
        <option>
            <div class="edit_userinfo_box_contact_information_text_choose_box">
                <div class="edit_userinfo_box_contact_information_text_choose_ico"></div>
                <div class="edit_userinfo_box_contact_information_text_choose_text">微信</div>
            </div>
        </option>
    </select>
</div>
</div>`;

var vm=new Vue ({
    el:'.main_content',
    data:{
        edit_box_background_color_show:false,
        user_info_box_show:false,
        avatar_editbox_show:false,
        indexpage_style: {
            'border-top': "4px solid rgba(0, 150, 250, 1)",
            opacity: 1
        },
        collection_style:{
        },
        temp:{
            'border-top': "4px solid rgba(0, 150, 250, 1)",
            opacity: 1
        },
        action:{
            'background-color': 'rgba(200,200,200,0.5)',
            'border-radius': '15px',
            position: 'absolute',
            left: 109.5,
            width:'90px',
            height: '40px',
        },
        step_len:0,
        /*
        indexpage_use:true,
        collection_use:false,
        mainpage_width:document.querySelector('.switch_box_content_1_content_addpage_box_switch_box').offsetWidth,
        margin_width:10,
        padding_width:10,
        left:this.action.left,
        add_width:mainpage_width/(4)+2.5,*/
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
        },
        hidden_avatar_edit_box:function(){
            this.avatar_editbox_show=false;
            console.log("test");
        },
        add_contact()
        {
            var targetdiv=document.querySelectorAll('.edit_userinfo_box_contact_information');
            targetdiv.forEach(function(target){
                target.insertAdjacentHTML('beforeend',model);
            });
            
        },
        switch_box_btn:function(type){
            temp=this.temp;
            if(type=='indexpage'){
                this.indexpage_style=temp;
                this.collection_style=null;
            }
            else{
                this.collection_style=temp;
                this.indexpage_style=null;
            }
        },
        //切换动画
        switch_box_action: function(type) {
            var mainpage_width = document.querySelector('.switch_box_content_1_content_addpage_box_switch_box').offsetWidth;
            var add_width = mainpage_width / 4 + 2.5;
            var target_left = 0;

            switch (type) {
                case 0:
                    target_left = 2.5;
                    break;
                case 1:
                    target_left = add_width - 2.5;
                    break;
                case 2:
                    target_left = add_width * 2 - 2.5 * 2;
                    break;
                case 3:
                    target_left = add_width * 3 - 2.5 * 3;
                    break;
            }

            this.step_len = Math.abs(this.action.left - target_left) / 60;
            this.do_action(this.action.left, target_left);
            this.action.left = target_left;
        },
        do_action: function(now_left, target_left, steps = 0) {
            if (now_left == target_left || steps >= 60) {
                this.action.left = target_left;
                return;
            }

            var temp = now_left < target_left ? now_left + this.step_len : now_left - this.step_len;
            this.action.left = temp;
            setTimeout(() => this.do_action(temp, target_left, steps + 1), 0.1);
        },
        
    }
});




