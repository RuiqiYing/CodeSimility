<template>
  <h2>{{ username1 }}的{{ homeworkname }}提交情况</h2>
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
        </div>
      </div>
    </div>
    <div class="information1111_div">
      <div id="myChart123" class="myChart123"></div>
       <div class="formTableDiv"><el-table
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
    </el-table></div> 
    </div>
    
  </div>
</template>
  
  <script>
import axios from "axios";
import api from "@/api";
import * as echarts from "echarts";
export default {
  data() {
    return {
      username1: localStorage.getItem("goaluserid"),
      questionid: "",
      homeworkname:localStorage.getItem("homeworkname"),
      value1: localStorage.getItem("homeworkid"),
      value2: "",
      question: "",
      name: "",
      ctime: "",
      chartData: [],
      tableData11:[],
      infor: "",
      algorithm: "",
      answer1: "",
      answer2: "",
      useriddata:[],
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
    get() {
      axios
        .post(
          api.url + "/information/getusername/",
          {
            userid: localStorage.getItem("input1"),
          },
          {
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            emulateJSON: true,
          }
        )
        .then((success) => {
          this.name1 = success.data;
        });

      axios
        .post(
          api.url + "/information/gethomeworkname/",
          {
            userid: localStorage.getItem("input1"),
          },
          {
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            emulateJSON: true,
          }
        )
        .then((success) => {
          var i;
          for (i = 0; i < success.data.data.length; i++) {
            this.options1.push({
              value: success.data.homeworkid[i],
              label: success.data.data[i],
            });
          }
        });

      axios
        .post(
          api.url + "/information/getallinfor/",
          {
            userid: localStorage.getItem("input1"),
          },
          {
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            emulateJSON: true,
          }
        )
        .then((success) => {
          this.name = success.data.username;
          this.ctime = success.data.ctime.slice(0, 9);
          this.infor = success.data.information;
        });
    },
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
      // myChart1.on("click", function (params) {
      //   //用于做每个点的监听，只用点击点才能够获取想要的监听效果；
      //   let data = {
      //     x: params.name,
      //     y: params.data,
      //   };
      //   console.log(data);
      //   alert(JSON.stringify(data));
      // });

      window.addEventListener("resize", () => {
        myChart1.resize();
      });
    },
    check() {
      axios
        .post(
          api.url + "/getsimilarity/getstuhomeworksim/",
          {
            userid: localStorage.getItem("input1"),
            homeworkid: this.value1,
            calculation: this.value2,
          },
          {
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            emulateJSON: true,
          }
        )
        .then((success) => {
          this.tableData11=[]
          //console.log(success.data);
          this.xAxis.data = success.data.id;
          this.chartData = success.data.similarity;
          this.useriddata=success.data.useriddata;
          this.drawChart();
          for(var i=0;i<success.data.id.length;i++){
            var json={}
            json.questionid=success.data.id[i]
            json.similarity=success.data.similarity[i]
            json.userid=success.data.useriddata[i]
            this.tableData11.push(json)
          }
          
        });
    },
  },
};
</script>
  
  <style >
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
.myChart123{
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

.formTableDiv{
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