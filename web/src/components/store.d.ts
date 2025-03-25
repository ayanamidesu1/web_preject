// src/components/store.d.ts
import { Store } from 'vuex';

// 定义根状态类型
export interface RootState {
  pageStatus: {
    upload_work: boolean;
    upload_work_type: string;
    index_page: boolean;
    indexPage: number;
    search_page: boolean;
    chat_page: boolean;
    content_index_page: boolean;
    user_center_page: boolean;
    other_user_center_page: boolean;
  };
  content_page: {
    ill_page: boolean;
    comic_page: boolean;
    novel_page: boolean;
    img_content_page: boolean;
    item_path: string;
  };
  token: string;
  userinfo: Record<string, any>;
  work_id: string;
  work_type: string;
  other_userid: string;
  pageStack: Array<{
    pageStatus: any;
    content_page: any;
  }>;
  pushTimer: NodeJS.Timeout | null;
}

// 定义 mutation 类型
export type Mutation = {
  type: string;
  payload?: any;
};

declare module './store.js' {
  const store: Store<RootState>;
  export default store;
}
