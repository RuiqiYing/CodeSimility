<template>
  <div>
    <h2>{{ username1 }}的{{ homeworkname }}提交情况</h2>

  </div>
  <div class="flex1_div">
    <div class="infor_div">
      <div class="inforsmall_div" style="height: 220px">
        <h2>详细信息</h2>
        <div style="width: 200px">
          <div>
            <div class="text_div">昵称: {{ name }}</div>
            <div class="text_div">注册时间: {{ ctime }}</div>
            <div class="text_div">个性签名:{{ infor }}</div>
            <div style="height: 20px"></div>
          </div>
        </div>
      </div>
      <div style="height: 30px"></div>
      <div class="inforsmall_div" style="height: 450px">
        <h2>完成的作业</h2>

        <div style="width: 150px; margin-left: 12%">
          <el-select
            style="height: 40px"
            v-model="value1"
            placeholder="选择作业"
          >
            <el-option
              v-for="item in options1"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
          <el-select
            style="height: 40px"
            v-model="value2"
            placeholder="选择算法"
          >
            <el-option
              v-for="item in options2"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
          <div style="height: 20px"></div>
          <el-button class="button" type="primary" @click="check()" plain
            >查看相似度</el-button
          >
          <div style="height: 20px"></div>
          <el-button class="button" type="primary" @click="checkanswer()" plain
            >查看答案</el-button
          >
          <div style="height: 20px"></div>
          <el-button
            class="button"
            type="primary"
            @click="dialogFormVisible = true"
            plain
            >对比答案</el-button
          >
        </div>
      </div>
    </div>
    <div class="information1111_div">
      <div id="myChart123" class="myChart123"></div>
      <div class="formTableDiv">
        <el-table
          :data="tableData11"
          style="width: 100%"
          stripe="true"
          border="true"
          :header-cell-style="{ 'text-align': 'center' }"
          :cell-style="{ textAlign: 'center' }"
        >
          <el-table-column
            :prop="index"
            :label="item"
            v-for="(item, index) in tableHeader"
            :key="index"
          >
          </el-table-column>
        </el-table>
      </div>
    </div>
  </div>
  <el-dialog
    v-model="dialogFormVisible"
    title="输入需要对比同学ID"
    draggable="true"
  >
    <el-form :model="form">
      <el-form-item label="同学ID" :label-width="formLabelWidth">
        <el-input v-model="form.userid" autocomplete="off" />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取消</el-button>
        <el-button type="primary" @click="compareanswer()"> 确定 </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script>
import axios from "axios";
import api from "@/api";
import * as echarts from "echarts";
export default {
  data() {
    return {
      form: {
        userid: "",
        name: "",
        region: "",
        date1: "",
        date2: "",
        delivery: false,
        type: [],
        resource: "",
        desc: "",
      },
      dialogFormVisible: false,
      username1: localStorage.getItem("goaluserid"),
      questionid: "",
      homeworkname: localStorage.getItem("homeworkname"),
      value1: localStorage.getItem("homeworkid"),
      value2: "",
      question: "",
      name: "",
      ctime: "",
      chartData: [],
      tableData11: [],
      infor: "",
      algorithm: "",
      answer1: "",
      answer2: "",
      useriddata: [],
      dialogVisible: false,
      options1: [],
      tableHeader: {
        questionid: "问题id",
        similarity: "相似度",
        userid: "最相似同学id",
      },
      xAxis: {
        data: [],
      },
      options2: [
        {
          value: "1",
          label: "算法一：均衡",
        },
        {
          value: "2",
          label: "算法二：长文本及代码有优势",
        },
        {
          value: "3",
          label: "算法三：仅给出是否相似，适合概览",
        },
      ],
    };
  },
  created() {
    this.get();
  },
  mounted() {},
  methods: {
    // 下载文件
    download() {
      axios
        .post(
          "http://127.0.0.1:8000/getsimilarity/getfile/",
          {},
          {
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            emulateJSON: true,
            responseType: "blob",
          }
        )
        .then((res) => {
          let blob = new Blob([res.data], {
            type: "application/msword", // 这里需要根据不同的文件格式写不同的参数
          });

          let eLink = document.createElement("a");
          eLink.download = "111.xlsx"; // 给文件名和指定格式，浏览器下载时看到的
          eLink.style.display = "none";
          eLink.href = URL.createObjectURL(blob);
          document.body.appendChild(eLink);
          eLink.click();
          URL.revokeObjectURL(eLink.href);
          document.body.removeChild(eLink);
        })
        .catch((err) => {
          console.log(err);
        });
    },

    // 比较答案
    compareanswer() {
      this.dialogFormVisible = false;
      localStorage.setItem("compareid", this.form.userid);
      this.$router.push("compareanswer");
    },

    // 获取数据
    get() {
      const limit = pLimit(2); // 限制并发请求数量为 2

      // 请求 1: 获取用户名
      const request1 = limit(() =>
        axios.post(
          api.url + "/information/getusername/",
          {
            userid: localStorage.getItem("input1"),
          },
          {
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            emulateJSON: true,
          }
        )
      );

      // 请求 2: 获取作业名称
      const request2 = limit(() =>
        axios.post(
          api.url + "/information/gethomeworkname/",
          {
            userid: localStorage.getItem("input1"),
          },
          {
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            emulateJSON: true,
          }
        )
      );

      // 请求 3: 获取用户信息
      const request3 = limit(() =>
        axios.post(
          api.url + "/information/getallinfor/",
          {
            userid: localStorage.getItem("input1"),
          },
          {
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            emulateJSON: true,
          }
        )
      );

      // 并行执行这些请求
      Promise.all([request1, request2, request3])
        .then(([nameResponse, homeworkResponse, userInfoResponse]) => {
          this.name1 = nameResponse.data;
          const homeworkData = homeworkResponse.data;
          this.options1 = homeworkData.data.map((homework, index) => ({
            value: homeworkData.homeworkid[index],
            label: homework,
          }));
          this.name = userInfoResponse.data.username;
          this.ctime = userInfoResponse.data.ctime.slice(0, 9);
          this.infor = userInfoResponse.data.information;
        })
        .catch((error) => {
          console.error("Error occurred:", error);
        });
    },

    // 绘制图表
    drawChart() {
      let myChart1 = echarts.init(document.getElementById("myChart123"));
      myChart1.setOption({
        xAxis: this.xAxis,
        yAxis: {},
        tooltip: {},
        series: [
          {
            name: "相似度",
            type: "line",
            data: this.chartData,
          },
        ],
      });

      window.addEventListener("resize", () => {
        myChart1.resize();
      });
    },

    // 查看答案
    checkanswer() {
      this.$router.push("viewanswer");
    },

    // 获取作业相似度
    check() {
      const limit = pLimit(2); // 限制并发请求数量为 2

      // 请求 1: 获取作业相似度
      const request1 = limit(() =>
        axios.post(
          api.url + "/getsimilarity/getstuhomeworksim/",
          {
            userid: localStorage.getItem("goaluserid"),
            homeworkid: this.value1,
            calculation: this.value2,
          },
          {
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            emulateJSON: true,
          }
        )
      );

      // 并行执行请求
      request1
        .then((success) => {
          this.tableData11 = [];
          this.xAxis.data = success.data.id;
          this.chartData = success.data.similarity;
          this.useriddata = success.data.useriddata;
          this.drawChart();
          for (let i = 0; i < success.data.id.length; i++) {
            this.tableData11.push({
              questionid: success.data.id[i],
              similarity: success.data.similarity[i],
              userid: success.data.useriddata[i],
            });
          }
        })
        .catch((error) => {
          console.error("Error occurred:", error);
        });
    },
  },
};
</script>

<style>
.button {
  width: 90px;
}
.flex1_div {
  width: 90%;
  height: 700px;
  display: flex;
  margin-left: 5%;
  margin-top: 3%;
  /* justify-content: center;
  align-items: center; */
  box-shadow: 0px -2px 0px 0px #e5e5e5, /*上边阴影 */ -2px 0px 0px 0px #e5e5e5,
    /*左边阴影  */ 2px 0px 0px 0px #e5e5e5,
    /*右边阴影 */ 0px 2px 0px 0px #e5e5e5; /*下边阴影 */
}
.myChart123 {
  height: 350px;
  width: 1000px;
}

.infor_div {
  width: 200px;
  box-shadow: 0px -2px 0px 0px #e5e5e5, /*上边阴影 */ -2px 0px 0px 0px #e5e5e5,
    /*左边阴影  */ 2px 0px 0px 0px #e5e5e5,
    /*右边阴影 */ 0px 2px 0px 0px #e5e5e5; /*下边阴影 */
}
.information1111_div {
  width: fit-content;
  /* margin-left: 20px; */
}

.formTableDiv {
  width: 1000px;
  height: 350px;
  overflow: auto;
}
.inforsmall_div {
  margin-top: -10%;
  width: 200px;
  position: relative;
  background-color: #f3f3f3;
  box-shadow: 0px -2px 0px 0px #e5e5e5, /*上边阴影 */ -2px 0px 0px 0px #e5e5e5,
    /*左边阴影  */ 2px 0px 0px 0px #e5e5e5,
    /*右边阴影 */ 0px 2px 0px 0px #e5e5e5; /*下边阴影 */
}
.text_div {
  text-align: left;
  margin-left: 22px;
  height: 30px;
}
</style>
