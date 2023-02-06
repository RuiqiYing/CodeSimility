<template>
  <header-navbar></header-navbar
  ><el-container>
    <el-container><side-bar></side-bar></el-container>
    <el-container
      ><el-main>
        <!-- 路由占位符 -->
        <router-view></router-view> </el-main
    ></el-container>
  </el-container>
</template>
<script >
import HeaderNavbar from "@/components/NavBar.vue";
import SideBar from "@/components/SideBar.vue";
export default {
  components: {
    HeaderNavbar,
    SideBar,
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