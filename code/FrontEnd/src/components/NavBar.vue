<template>
  <div class="out">
    <el-page-header @back="goBack">
      <template #content>
        
        <div class="flex items-center">
          <span class="text-large font-600 mr-3"> 相似度检测系统 </span>
          <!-- <span class="text-sm mr-2" style="color: var(--el-text-color-regular)">
            Sub title
          </span> -->
          <!-- <el-tag>Default</el-tag> -->
        </div>
      </template>
      <template #extra>
        <div class="tail"></div>
        <div class="msg">欢迎，{{ msg }}</div>
      </template>
    </el-page-header>
  </div>
</template>


<script >
export default {
  name: "header-navbar",
  data() {
    return {
      msg: localStorage.getItem("userid"),
    };
  },
  methods:{
    goBack(){
      this.$router.back()
    },
  },
};
</script>



<style>
.out {
  text-align: center;
  background-color: rgb(147, 191, 241);
  height: 40px;
}

.tail {
  height: 10px;
  width: 30px;
}

.msg {
  width: 150px;
}
</style>