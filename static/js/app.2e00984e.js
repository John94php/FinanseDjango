(function(){"use strict";var e={7831:function(e,t,n){var o=n(3751),r=n(641);function a(e,t){const n=(0,r.g2)("router-view");return(0,r.uX)(),(0,r.Wv)(n)}var i=n(6262);const u={},l=(0,i.A)(u,[["render",a]]);var s=l,c=n(5220);const d={class:"home"};function f(e,t,n,o,a,i){const u=(0,r.g2)("AuthLayout");return(0,r.uX)(),(0,r.CE)("div",d,[(0,r.bF)(u)])}function m(e,t,n,o,a,i){const u=(0,r.g2)("el-menu-item"),l=(0,r.g2)("el-sub-menu"),s=(0,r.g2)("el-button"),c=(0,r.g2)("el-menu");return(0,r.uX)(),(0,r.Wv)(c,{class:"el-menu-demo",mode:"horizontal"},{default:(0,r.k6)((()=>[(0,r.bF)(u,{index:"1"},{default:(0,r.k6)((()=>[(0,r.eW)("Processing Center")])),_:1}),(0,r.bF)(l,{index:"2"},{title:(0,r.k6)((()=>[(0,r.eW)("Workspace")])),default:(0,r.k6)((()=>[(0,r.bF)(u,{index:"2-1"},{default:(0,r.k6)((()=>[(0,r.eW)("item one")])),_:1}),(0,r.bF)(u,{index:"2-2"},{default:(0,r.k6)((()=>[(0,r.eW)("item two")])),_:1}),(0,r.bF)(u,{index:"2-3"},{default:(0,r.k6)((()=>[(0,r.eW)("item three")])),_:1}),(0,r.bF)(l,{index:"2-4"},{title:(0,r.k6)((()=>[(0,r.eW)("item four")])),default:(0,r.k6)((()=>[(0,r.bF)(u,{index:"2-4-1"},{default:(0,r.k6)((()=>[(0,r.eW)("item one")])),_:1}),(0,r.bF)(u,{index:"2-4-2"},{default:(0,r.k6)((()=>[(0,r.eW)("item two")])),_:1}),(0,r.bF)(u,{index:"2-4-3"},{default:(0,r.k6)((()=>[(0,r.eW)("item three")])),_:1})])),_:1})])),_:1}),(0,r.bF)(s,{type:"primary",onClick:i.handleLogout},{default:(0,r.k6)((()=>[(0,r.eW)("Wyloguj")])),_:1},8,["onClick"])])),_:1})}n(4114);var p=n(1250),h=n(163),b=n(1644),g={name:"AuthLayout",created(){this.checkAuthenticated()},methods:{checkAuthenticated(){const e=localStorage.getItem("token");if(!e)return h.nk.error("Zaloguj się, aby uzyskać dostęp do tej strony"),void this.$router.push("/");const t={Authorization:`Token ${e}`,"Content-Type":"application/json"};p.A.get("http://127.0.0.1:8000/api/userdata/",{headers:t}).then((e=>{console.log(e.data);const t=e.data.name,n=e.data.surname;(0,b.df)({title:`${t} ${n}`,message:(0,r.h)("i",{style:"color: blue"},"Witamy")})})).catch((e=>{console.error("Błąd podczas sprawdzania statusu logowania:",e)}))},handleLogout(){const e=localStorage.getItem("token"),t="http://127.0.0.1:8000/api/logout/",n={Authorization:`Token ${e}`,"Content-Type":"application/json"};p.A.post(t,null,{headers:n}).then((e=>{console.log(e.data.message),localStorage.removeItem("token"),this.$router.push("/")})).catch((e=>{console.error("Błąd podczas wylogowywania:",e)}))}}};const v=(0,i.A)(g,[["render",m]]);var k=v,y={name:"HomeView",components:{AuthLayout:k}};const w=(0,i.A)(y,[["render",f]]);var A=w;const F={id:"login"};function j(e,t,n,o,a,i){const u=(0,r.g2)("el-input"),l=(0,r.g2)("el-form-item"),s=(0,r.g2)("el-button"),c=(0,r.g2)("el-form");return(0,r.uX)(),(0,r.CE)("div",F,[(0,r.bF)(c,{model:a.form,"label-width":"auto",style:{"max-width":"700px"}},{default:(0,r.k6)((()=>[(0,r.bF)(l,{label:"Użytkownik"},{default:(0,r.k6)((()=>[(0,r.bF)(u,{modelValue:a.form.username,"onUpdate:modelValue":t[0]||(t[0]=e=>a.form.username=e),clearable:"",placeholder:"Wpisz nazwę użytkownika"},null,8,["modelValue"])])),_:1}),(0,r.bF)(l,{label:"Hasło"},{default:(0,r.k6)((()=>[(0,r.bF)(u,{modelValue:a.form.password,"onUpdate:modelValue":t[1]||(t[1]=e=>a.form.password=e),clearable:"",placeholder:"Wpisz hasło","show-password":"",type:"password"},null,8,["modelValue"])])),_:1}),(0,r.bF)(s,{type:"primary",onClick:i.handleLogin},{default:(0,r.k6)((()=>[(0,r.eW)("Zaloguj")])),_:1},8,["onClick"])])),_:1},8,["model"])])}var W={name:"LoginView",data(){return{form:{username:"",password:""}}},methods:{handleLogin(){const e={username:this.form.username,password:this.form.password};p.A.post("http://127.0.0.1:8000/api/login/",e).then((e=>{const t=e.data.token;localStorage.setItem("token",t),this.$router.push("/main")}))}}};const _=(0,i.A)(W,[["render",j]]);var x=_;const C=[{path:"/",name:"home",component:x},{path:"/about",name:"about",component:()=>n.e(594).then(n.bind(n,603))},{path:"/main",name:"main",component:A}],O=(0,c.aE)({history:(0,c.LA)("/"),routes:C});var z=O,L=n(6278),T=(0,L.y$)({state:{},getters:{},mutations:{},actions:{},modules:{}}),E=n(4952);n(4188);(0,o.Ef)(s).use(E.A).use(T).use(z).mount("#app"),document.title="Finanse - aplikacja do zarządzania budżetem domowym"}},t={};function n(o){var r=t[o];if(void 0!==r)return r.exports;var a=t[o]={exports:{}};return e[o].call(a.exports,a,a.exports,n),a.exports}n.m=e,function(){var e=[];n.O=function(t,o,r,a){if(!o){var i=1/0;for(c=0;c<e.length;c++){o=e[c][0],r=e[c][1],a=e[c][2];for(var u=!0,l=0;l<o.length;l++)(!1&a||i>=a)&&Object.keys(n.O).every((function(e){return n.O[e](o[l])}))?o.splice(l--,1):(u=!1,a<i&&(i=a));if(u){e.splice(c--,1);var s=r();void 0!==s&&(t=s)}}return t}a=a||0;for(var c=e.length;c>0&&e[c-1][2]>a;c--)e[c]=e[c-1];e[c]=[o,r,a]}}(),function(){n.d=function(e,t){for(var o in t)n.o(t,o)&&!n.o(e,o)&&Object.defineProperty(e,o,{enumerable:!0,get:t[o]})}}(),function(){n.f={},n.e=function(e){return Promise.all(Object.keys(n.f).reduce((function(t,o){return n.f[o](e,t),t}),[]))}}(),function(){n.u=function(e){return"js/about.79ce2d04.js"}}(),function(){n.miniCssF=function(e){}}(),function(){n.g=function(){if("object"===typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"===typeof window)return window}}()}(),function(){n.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)}}(),function(){var e={},t="frontend:";n.l=function(o,r,a,i){if(e[o])e[o].push(r);else{var u,l;if(void 0!==a)for(var s=document.getElementsByTagName("script"),c=0;c<s.length;c++){var d=s[c];if(d.getAttribute("src")==o||d.getAttribute("data-webpack")==t+a){u=d;break}}u||(l=!0,u=document.createElement("script"),u.charset="utf-8",u.timeout=120,n.nc&&u.setAttribute("nonce",n.nc),u.setAttribute("data-webpack",t+a),u.src=o),e[o]=[r];var f=function(t,n){u.onerror=u.onload=null,clearTimeout(m);var r=e[o];if(delete e[o],u.parentNode&&u.parentNode.removeChild(u),r&&r.forEach((function(e){return e(n)})),t)return t(n)},m=setTimeout(f.bind(null,void 0,{type:"timeout",target:u}),12e4);u.onerror=f.bind(null,u.onerror),u.onload=f.bind(null,u.onload),l&&document.head.appendChild(u)}}}(),function(){n.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})}}(),function(){n.p="/"}(),function(){var e={524:0};n.f.j=function(t,o){var r=n.o(e,t)?e[t]:void 0;if(0!==r)if(r)o.push(r[2]);else{var a=new Promise((function(n,o){r=e[t]=[n,o]}));o.push(r[2]=a);var i=n.p+n.u(t),u=new Error,l=function(o){if(n.o(e,t)&&(r=e[t],0!==r&&(e[t]=void 0),r)){var a=o&&("load"===o.type?"missing":o.type),i=o&&o.target&&o.target.src;u.message="Loading chunk "+t+" failed.\n("+a+": "+i+")",u.name="ChunkLoadError",u.type=a,u.request=i,r[1](u)}};n.l(i,l,"chunk-"+t,t)}},n.O.j=function(t){return 0===e[t]};var t=function(t,o){var r,a,i=o[0],u=o[1],l=o[2],s=0;if(i.some((function(t){return 0!==e[t]}))){for(r in u)n.o(u,r)&&(n.m[r]=u[r]);if(l)var c=l(n)}for(t&&t(o);s<i.length;s++)a=i[s],n.o(e,a)&&e[a]&&e[a][0](),e[a]=0;return n.O(c)},o=self["webpackChunkfrontend"]=self["webpackChunkfrontend"]||[];o.forEach(t.bind(null,0)),o.push=t.bind(null,o.push.bind(o))}();var o=n.O(void 0,[504],(function(){return n(7831)}));o=n.O(o)})();
//# sourceMappingURL=app.2e00984e.js.map