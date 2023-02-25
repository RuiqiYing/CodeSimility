<template>
  <div style="float: left; text-align: right; width: 49%; margin-left: 2%">
    <h2>相似度对比</h2>
  </div>
  <div class="flex_div">
    <div class="in_div">
      <h3>查看个人主页</h3>
      <div class="out" style="width: 200px; height: 30px">
        <el-input v-model="input1" placeholder="输入学号" clearable />
        <div style="height: 30px"></div>
      </div>
      <el-button class="button" type="primary" @click="click1()" plain
        >查看</el-button
      >
    </div>
    <div style="width: 30px"></div>
    <div class="in_div" style="width: 450px; height: 450px">
      <h3>对比</h3>
      <div class="out" style="width: 200px">
        <el-input v-model="input2" placeholder="输入学号" clearable />
        <div style="height: 30px"></div>
        <el-input v-model="input3" placeholder="输入学号" clearable />
        <div style="height: 30px"></div>
      </div>
      <el-button class="button" type="primary" @click="click2()" plain
        >查看</el-button
      >
    </div>
  </div>
</template>
  
  <script>
//   import axios from "axios";
//   import api from "@/api";
export default {
  data() {
    return {
      input1: "",
      input2: "",
      input3: "",
      input4: "",
    };
  },

  methods: {
    click1() {
      localStorage.setItem("input1", this.input1);
      this.$router.push("infor");
    },

    click2() {
      localStorage.setItem("input2", this.input2);
      localStorage.setItem("input3", this.input3);
      this.$router.push("comparepage");
    },
  },
};
</script>
  <style scoped>
.in_div {
  box-shadow: 0px -3px 0px 0px #e5e5e5, /*上边阴影 */ -1px 0px 0px 0px #e5e5e5,
    /*左边阴影  */ 1px 0px 0px 0px #e5e5e5,
    /*右边阴影 */ 0px 3px 0px 0px #e5e5e5; /*下边阴影 */
}

.flex_div {
  display: flex;
  height: 600px;
  width: 1100px;
  margin-top: 10%;
  margin-left: 5%;
  margin-right: 2%;
  justify-content: center;
  align-items: center;
}

.in_div {
  width: 450px;
  height: 450px;
  text-align: center;
  background-color: white;
  position: relative;
}

.out {
  position: absolute;
  background-color: white;
  left: 50%;
  top: 30%;
  transform: translate(-50%, -50%);
}

.button {
  position: absolute;
  text-align: center;
  right: 44%;
  bottom: 40%;
}
</style>