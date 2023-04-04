<template>
  <div style="margin-right: 100px; width: 19%">
    <h2>个人信息</h2>
  </div>

  <div class="flex_div">
    <div class="in_div" style="width: 600px; height: 450px">
      <div class="out" style="width: 300px">
        <el-form
          label-width="100px"
          :model="formLabelAlign"
          style="max-width: 450px"
        >
          <el-form-item label="学号">
            <el-input v-model="formLabelAlign.userid" disabled="true" />
          </el-form-item>
          <el-form-item label="姓名">
            <el-input v-model="formLabelAlign.username" />
          </el-form-item>
          <el-form-item label="个人简介">
            <el-input v-model="formLabelAlign.information" />
          </el-form-item>
          <el-form-item label="注册时间">
            <el-input v-model="formLabelAlign.ctime" disabled="true" />
          </el-form-item>
        </el-form>
      </div>
      <el-button class="button" type="primary" @click="click()" plain
        >修改</el-button
      >
    </div>
  </div>
</template>
    
    <script>
import axios from "axios";
import api from "@/api";
export default {
  data() {
    return {
      formLabelAlign: {
        userid: "",
        username: "",
        information: "",
        ctime: "",
      },
      input1: "",
    };
  },
  created() {
    this.get();
  },
  methods: {
    get() {
      axios
        .post(
          api.url + "/information/getallinfor/",
          {
            userid: localStorage.getItem("userid"),
          },
          {
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            emulateJSON: true,
          }
        )
        .then((success) => {
          console.log(success.data);
          this.formLabelAlign.username = success.data.username;

          this.formLabelAlign.information = success.data.information;
          var time =
            success.data.ctime.substring(0, 10) +
            " " +
            success.data.ctime.substring(11, 19);
          this.formLabelAlign.ctime = time;
          this.formLabelAlign.userid = localStorage.getItem("userid");
        });
    },
    click() {
      axios
        .post(
          api.url + "/information/changeinformation/",
          {
            userid: localStorage.getItem("userid"),
            information: this.formLabelAlign.information,
            username: this.formLabelAlign.username,
          },
          {
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            emulateJSON: true,
          }
        )
        .then((success) => {
          this.$message({ type: "info", message: success.data });
        });
    },
  },
};
</script>
    <style scoped>
.in_div {
  box-shadow: 0px -0.5px 0px 0px #e5e5e5,
    /*上边阴影 */ -1.5px 0px 0px 0px #e5e5e5,
    /*左边阴影  */ 1.5px 0px 0px 0px #e5e5e5,
    /*右边阴影 */ 0px 3px 0px 0px #e5e5e5; /*下边阴影 */
}

.flex_div {
  display: flex;
  height: 600px;
  width: 1100px;
  margin: auto;
  position: absolute;
  top: 0;
  left: 140px;
  right: 0;
  bottom: 0;
}

.in_div {
  width: 450px;
  height: 450px;
  text-align: center;
  background-color: white;
  margin: auto;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.out {
  position: absolute;
  background-color: white;
  left: 45%;
  top: 30%;
  transform: translate(-50%, -50%);
}

.button {
  position: absolute;
  text-align: center;
  right: 44%;
  bottom: 20%;
}
</style>