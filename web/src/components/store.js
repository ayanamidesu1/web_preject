import { createStore } from 'vuex';
import * as cookies from 'H:/web_project/model/cookies.js';

const MAX_STACK_DEPTH = 500; // 设置页面状态栈的最大深度

const store = createStore({
  state: {
    // 页面状态，控制不同页面的显示状态
    pageStatus: {
      upload_work: false,
      upload_work_type: '',
      index_page: true,
      indexPage: 0,
      search_page: false,
      chat_page: false,
      content_index_page: false,
      user_center_page: false,
      other_user_center_page:false,
      data_analysis_page:false,
      work_contribute_page:false,
      br_his_page:false, //浏览历史页面
    },
    // 内容页面状态，用于控制内容相关页面的显示状态
    content_page: {
      ill_page: false,
      comic_page: false,
      novel_page: false,
      img_content_page: false,
      item_path: '',
    },
    // 用户信息和认证相关状态
    token: '',
    userinfo: {},
    work_id: '',
    work_type: '',
    other_userid:'',
    // 页面状态栈，用于实现页面回退功能
    pageStack: [],
    // 定时器，用于页面状态管理
    pushTimer: null,
    cursor_msg:'喵~',
    //鼠标随动组件消息
  },
  mutations: {
    // 设置用户信息
    SET_USERINFO(state, userinfo) { state.userinfo = userinfo; },
    // 设置认证 token
    SET_TOKEN(state, token) { state.token = token; },
    // 更新页面状态
    SET_PAGESTATUS(state, pageStatus) { state.pageStatus = { ...state.pageStatus, ...pageStatus }; },
    // 设置上传作品的状态
    SET_UPLOAD_WORK(state, upload_work) { state.pageStatus.upload_work = upload_work; },
    // 设置上传作品类型
    SET_UPLOAD_WORK_TYPE(state, upload_work_type) { state.pageStatus.upload_work_type = upload_work_type; },
    // 设置首页状态
    SET_INDEX_PAGE(state, index_page) { state.pageStatus.index_page = index_page; },
    // 设置任意页面状态
    SET_KEY(state, { key, value }) { state.pageStatus[key] = value; },
    // 设置索引页
    SET_INDEXPAGE(state, value) { state.pageStatus.indexPage = value; },
    // 设置搜索页状态
    SET_SEARCH_PAGE(state, search_page) { state.pageStatus.search_page = search_page; },
    // 设置单一页面状态并控制所有页面状态的显示
    SET_SINGLE_PAGE_STATUS(state, { key, value }) {
      if (key === 'all') {
        for (const k in state.pageStatus) {
          if (Object.prototype.hasOwnProperty.call(state.pageStatus, k) && typeof state.pageStatus[k] === 'boolean') {
            state.pageStatus[k] = false;
          }
        }
        return;
      }
      for (const k in state.pageStatus) {
        if (Object.prototype.hasOwnProperty.call(state.pageStatus, k) && typeof state.pageStatus[k] === 'boolean') {
          state.pageStatus[k] = false;
        }
      }
      state.pageStatus[key] = value;
      const allFalse = Object.keys(state.pageStatus).every(k => typeof state.pageStatus[k] !== 'boolean' || state.pageStatus[k] === false);
      if (allFalse) {
        state.pageStatus.index_page = true;
      }
    },
    // 设置内容页面状态
    SET_CONTENT_PAGE(state, { key, value }) {
      for (const k in state.content_page) {
        if (Object.prototype.hasOwnProperty.call(state.content_page, k) && typeof state.content_page[k] === 'boolean') {
          state.content_page[k] = false;
        }
      }
      state.content_page[key] = value;
    },
    // 设置作品 ID
    SET_WORK_ID(state, work_id) { state.work_id = work_id; },
    // 将当前页面状态压入栈，以便后退时恢复
    PUSH_PAGE_STATE(state) {
      if (state.pageStack.length >= MAX_STACK_DEPTH) {
        state.pageStack.shift(); // 删除最早的记录
      }
      state.pageStack.push({
        pageStatus: JSON.parse(JSON.stringify(state.pageStatus)), // 深拷贝页面状态
        content_page: JSON.parse(JSON.stringify(state.content_page)), // 深拷贝内容页面状态
      });
    },
    // 恢复上一个页面状态
    POP_PAGE_STATE(state) {
      if (state.pageStack.length > 0) {
        const previousState = state.pageStack.pop();
        state.pageStatus = previousState.pageStatus;
        state.content_page = previousState.content_page;
      }
    },
    // 重置页面状态栈和定时器
    RESET_PAGE_STACK(state) {
      state.pageStack = [];
      state.pushTimer = null; // 清除定时器
    },
    // 设置内容页面的路径
    SET_ITEM_PATH(state, path) {
      state.content_page.item_path = path;
    },
    // 设置作品类型
    SET_WORK_TYPE(state, work_type) {
      state.work_type = work_type;
    },
    //设置其他用户ID
    SET_OTHER_USERID(state, userid) {
      state.other_userid = userid;
    },
    //设置浏览页面显示状态
    SET_BR_HIS_PAGE(state, br_his_page) {
      state.pageStatus.br_his_page = br_his_page;
    },
    //设置鼠标随动组件消息
    set_cursor_msg(state,msg){
      state.cursor_msg = msg;
    }
  },
  actions: {
    // 页面回退
    goBack({ commit }) {
      commit('POP_PAGE_STATE'); // 恢复上一个状态
    }
  },
  getters: {
    // 获取用户信息
    userinfo: state => state.userinfo,
    // 获取认证 token
    token: state => state.token,
    // 获取上传作品状态
    upload_work: state => state.pageStatus.upload_work,
    upload_work_type: state => state.pageStatus.upload_work_type,
    // 获取首页状态
    index_page: state => state.pageStatus.index_page,
    indexPage: state => state.pageStatus.indexPage,
    // 获取搜索页状态
    search_page: state => state.pageStatus.search_page,
    chat_page: state => state.pageStatus.chat_page,
    // 获取内容页面状态
    ill_page: state => state.content_page.ill_page,
    comic_page: state => state.content_page.comic_page,
    novel_page: state => state.content_page.novel_page,
    work_id: state => state.work_id,
    img_content_page: state => state.content_page.img_content_page,
    content_index_page: state => state.pageStatus.content_index_page,
    pageStack: state => state.pageStack,
    item_path: state => state.content_page.item_path,
    work_type: state => state.work_type,
    user_center_page: state => state.pageStatus.user_center_page,
    other_user_center_page:state=>state.pageStatus.other_user_center_page,
    other_userid:state=>state.other_userid,
    data_analysis_page:state=>state.pageStatus.data_analysis_page,
    work_contribute_page:state=>state.pageStatus.work_contribute_page,
    //暴露浏览历史页面状态
    br_his_page:state=>state.pageStatus.br_his_page,
    //暴露鼠标随动组件消息
    cursor_msg:state=>state.cursor_msg
  },
});

export default store;
