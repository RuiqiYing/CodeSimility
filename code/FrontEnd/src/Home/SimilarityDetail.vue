<template>
  <h2>{{ homeworkname }}的相似度情况</h2>
  <div class="maindiv">
    <div class="viceDiv">
      <el-select
        v-model="value1"
        class="m-2"
        placeholder="选择题目"
        size="large"
      >
        <el-option
          v-for="item in options"
          :key="item"
          :label="item"
          :value="item"
        />
      </el-select>
    </div>
    <div class="viceDiv">
      <el-select
        v-model="value2"
        class="m-2"
        placeholder="选择算法"
        size="large"
      >
        <el-option
          v-for="item in options2"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
    </div>

    <div class="viceDiv">
      <el-button type="primary" style="width: 80px" @click="getdata()"
        >查看</el-button
      >
    </div>
  </div>
  <div class="detail">
    <el-select v-model="value3" placeholder="选择百分比" size="large">
      <el-option
        v-for="item in options3"
        :key="item.value"
        :label="item.label"
        :value="item.value"
      />
    </el-select>
    <el-button type="primary" style="height: 40px" @click="getinfor()"
      >查看同学</el-button
    >
  </div>

  <div class="flex_div">
    <div class="in_div" id="chartBar" style="width: 450px; height: 450px"></div>
    <div style="width: 30px"></div>
    <div id="chartPie" class="in_div" style="width: 450px; height: 450px"></div>
  </div>
  <el-dialog v-model="dialogTableVisible" title="详细信息" draggable>
    <el-table :data="gridData">
      <el-table-column
        :prop="index"
        :label="item"
        v-for="(item, index) in tableHeader"
        :key="index"
      >
      </el-table-column>
    
    </el-table>
  </el-dialog>
</template>
  
<script>
import axios from "axios";
import api from "@/api";
import * as eacharts from "echarts";

export default {
  data() {
    return {
      dialogTableVisible: false,
      tableHeader: {
        userid: "学号",
        similarity: "相似度",
      },
      formLabelWidth: "140px",
      yData: [0, 0, 0, 0, 0], // 数据
      update: true,
      value1: "",
      options: [1, 2, 3],
      value2: "",
      value3: "",
      gridData: [],
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
      options3: [
        {
          value: "1",
          label: "0%-20%",
        },
        {
          value: "2",
          label: "20%-40%",
        },
        {
          value: "3",
          label: "40%-60%",
        },
        {
          value: "4",
          label: "60%-80%",
        },
        {
          value: "5",
          label: "80%-100%",
        },
      ],

      homeworkname: localStorage.getItem("homeworkname"),
      chartPie: null,
      chartBar: null,
      echartsCtx: null,
      chartsWrapperStyle: {},
      debounceTimeout: null, // 用于存储防抖定时器
    };
  },
  created() {
    this.getsum();
    this.chartsWrapperStyle = {
      width: this.width + "px",
      height: this.height + "px",
    };
  },
  mounted() {
    this.drawPieChart([
      { value: 0, name: "0%-20%" },
      { value: 0, name: "20%-40%" },
      { value: 0, name: "40%-60%" },
      { value: 0, name: "60%-80%" },
      { value: 0, name: "80%-100%" },
    ]);
    this.initEcharts();
  },

  methods: {
    // 防抖函数
    debounce(func, wait) {
      return (...args) => {
        if (this.debounceTimeout) {
          clearTimeout(this.debounceTimeout); // 清除上一次的定时器
        }
        this.debounceTimeout = setTimeout(() => {
          func(...args); // 延迟执行函数
        }, wait);
      };
    },

    getinfor() {
      this.dialogTableVisible = true;
      axios
        .post(
          api.url + "/getsimilarity/getsimdetail/",
          {
            homeworkid: localStorage.getItem("homeworkid"),
            questionid: this.value1,
            calculation: this.value2,
            range:this.value3,
          },
          {
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            emulateJSON: true,
          }
        )
        .then((success) => {
          this.gridData = []
          for (var i = 0; i < success.data.data.length; i++) {
            var temp = { similarity: success.data.data[i], userid: success.data.stuinfor[i] }
            this.gridData.push(temp)
          }
        });
    },

    debouncedGetinfor() {
      this.debounce(this.getinfor, 1000)();
    },
    getdata() {
      axios
        .post(
          api.url + "/getsimilarity/gethomework/",
          {
            homeworkid: localStorage.getItem("homeworkid"),
            questionid: this.value1,
            calculation: this.value2,
          },
          {
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            emulateJSON: true,
          }
        )
        .then((success) => {
          console.log(success.data.data);
          var data = [
            { value: 0, name: "0%-20%" },
            { value: 0, name: "20%-40%" },
            { value: 0, name: "40%-60%" },
            { value: 0, name: "60%-80%" },
            { value: 0, name: "80%-100%" },
          ];
          var res = [0, 0, 0, 0, 0];
          var list = [];
          list = success.data.data;
          for (var i = 0; i < list.length; i++) {
            if (list[i] < 0.2) {
              res[0]++;
              data[0].value++;
            } else if (list[i] >= 0.2 && list[i] < 0.4) {
              res[1]++;
              data[1].value++;
            } else if (list[i] >= 0.4 && list[i] < 0.6) {
              res[2]++;
              data[2].value++;
            } else if (list[i] >= 0.6 && list[i] < 0.8) {
              res[3]++;
              data[3].value++;
            } else {
              res[4]++;
              data[4].value++;
            }
          }

          console.log(res);
          this.yData = res;
          this.drawPieChart(data);
          this.initEcharts();
        });
    },

    getsum() {
      axios
        .post(
          api.url + "/getsimilarity/getsum/",
          {
            questionnum: localStorage.getItem("questionnum"),
          },
          {
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            emulateJSON: true,
          }
        )
        .then((success) => {
          var jsonObj = JSON.parse(JSON.stringify(success.data.data));
          this.options = jsonObj;
        });
    },

    initEcharts() {
      // 基本柱状图
      const myChart = eacharts.init(document.getElementById("chartBar"));
      myChart.setOption({
        title: {
          text: "各区间人数",
          x: "center",
        },
        xAxis: {
          data: ["0%-20%", "20%-40%", "40%-60%", "60%-80%", "80%-100%"],
        },
        yAxis: {},
        series: [
          {
            type: "bar", //形状为柱状图
            data: this.yData,
          },
        ],
        tooltip: {},
        itemStyle: {
          emphasis: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: "rgba(0, 0, 0, 0.5)",
          },
        },
      });
      // 随着屏幕大小调节图表
      window.addEventListener("resize", () => {
        myChart.resize();
      });
    },

    // pie
    drawPieChart(data) {
      this.chartPie = eacharts.init(document.getElementById("chartPie"));
      this.chartPie.setOption({
        title: {
          text: "各区间比例",
          x: "center",
        },
        tooltip: {
          trigger: "item",
          formatter: "{a} <br/>{b} : {c} ({d}%)",
        },
        legend: {
          orient: "vertical",
          left: "left",
          data: ["0%-20%", "20%-40%", "40%-60%", "60%-80%", "80%-100%"],
        },
        series: [
          {
            name: "详细信息",
            type: "pie",
            radius: "55%",
            center: ["50%", "60%"],
            data: data,
            itemStyle: {
              emphasis: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: "rgba(0, 0, 0, 0.5)",
              },
            },
          },
        ],
      });
    },
    drawCharts() {
      this.drawPieChart();
    },
  },

  watch: {
    loading(n) {
      if (!n) {
        this.render();
        this.hideLoading();
      } else {
        this.showLoading();
      }
    },
    option: {
      handler(n) {
        this.render(n);
      },
      deep: true,
    },
  },
};
</script>


<style scoped>
.in_div {
  box-shadow: 0px -1px 0px 0px #e5e5e5, /*上边阴影 */ -0.2px 0px 0px 0px #e5e5e5,
    /*左边阴影  */ 0.2px 0px 0px 0px #e5e5e5,
    /*右边阴影 */ 0px 1px 0px 0px #e5e5e5; /*下边阴影 */
}

.flex_div {
  display: flex;
  height: 600px;
  justify-content: center;
  align-items: center;
}
.maindiv {
  display: flex;
  width: auto;
  height: 80px;
  margin-left: 25%;
}

.viceDiv {
  float: left;
  margin-top: 2%;
  margin-left: 3%;
  width: 20%;
}

.detail {
  float: left;
  margin-top: 2%;
  margin-left: 5%;
  width: 30%;
  height: 40px;
  display: flex;
}
</style>