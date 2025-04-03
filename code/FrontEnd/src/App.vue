<template>
  <!-- <HelloWorld></HelloWorld>
<router-link to="/home">首页</router-link>
<router-link to="/movie">电影</router-link>
<router-link to="/about">关于</router-link>  -->
<!-- 路由占位符 -->
<router-view></router-view>
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'

export default {
  name: 'App',
  // components: {
  //   // HelloWorld
  // }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  /* margin-top: 60px; */
  margin:0;
	padding:0;
	border:0
}
</style>
