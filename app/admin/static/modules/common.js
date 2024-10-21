/**
 * common demo
 */

layui.define(function (exports) {
  var $ = layui.$,
    layer = layui.layer,
    laytpl = layui.laytpl,
    setter = layui.setter,
    view = layui.view,
    admin = layui.admin;

  //公共业务的逻辑处理可以写在此处，切换任何页面都会执行
  //……

  // 检查token的函数 现在改成session了暂时不需要
  // function checkToken() {
  //   var token = layui.data(setter.tableName).access_token
  //   if (!token && location.pathname !== "/admin/login") {
  //     //判断是不是登录页面，如果不是则跳转
  //     location.href = "/admin/login";
  //   }
  // }

  // checkToken();

  //退出
  admin.events.logout = function () {
    //执行退出接口
    // admin.req({
    //   url: layui.setter.paths.base + "json/user/logout.js",
    //   type: "get",
    //   data: {},
    //   done: function (res) {
    //     //这里要说明一下：done 是只有 response 的 code 正常才会执行。而 succese 则是只要 http 为 200 就会执行

    //     //清空本地记录的 token，并跳转到登入页
    //     admin.exit(function () {
    //       location.href = "user/login.html";
    //     });
    //   },
    // });
    // 清除access_token
    localStorage.removeItem("access_token");
    location.href = "/admin/login";
  };

  //对外暴露的接口
  exports("common", {});
});
