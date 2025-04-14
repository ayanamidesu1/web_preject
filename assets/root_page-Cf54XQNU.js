import{_ as c,u as r,B as i,o as l,r as d,a as p,c as u,b as t,d as a,e as f}from"./index-CeFa-_Ge.js";const m={class:"root_page"},v={class:"header_box"},g={class:"content_box"},h={__name:"root_page",setup(w){const _=r(),s=new i;return l(async()=>{let e=await s.verify_login();if(e.status==200){let o=await s.get_self_info();console.log(`用户信息
`,o),_.$state.user=o.result.data}else console.log(`错误
`,e)}),(e,o)=>{const n=d("router-view");return p(),u("div",m,[t("div",v,[a(f)]),t("div",g,[a(n)])])}}},B=c(h,[["__scopeId","data-v-c84d296f"]]);export{B as default};
