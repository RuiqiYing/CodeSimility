<template>
    <header-navbar></header-navbar
    ><el-container>
      <el-container><stu-side-bar></stu-side-bar></el-container>
      <el-container
        ><el-main>
          <!-- 路由占位符 -->
          <router-view></router-view> </el-main
      ></el-container>
    </el-container>
  </template>
  <script >
  import HeaderNavbar from "@/components/NavBar.vue";
  import StuSideBar from "@/components/StuSide.vue";
  export default {
    components: {
      HeaderNavbar,
      StuSideBar,
    },
  
  };
  </script>
  
  
    <style>
  .out {
    text-align: center;
    background-color: rgb(147, 191, 241);
    height: 40px;
  }
  </style>