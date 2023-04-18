<template>
  <div>
    <div style="float: left; text-align: right; width: 60%; margin-left: 2%">
      <h2>{{ homeworkname }}总体概览</h2>
    </div>
    <div style="float: right; text-align: right; width: 38%">
      <el-button class="new_btn" type="primary" @click="download()"
        >下载</el-button
      >
    </div>
  </div>
  <div class="flex_div_all">
    <div class="left_div">
      <div class="smallbox">
        <div class="zhanwei"></div>
        <div class="zhanwei"></div>
        整体相似度最高：
        {{ highid }}
        <div class="zhanwei"></div>
        <el-text class="mx-1" style="color: red; font-size: x-large">{{
          highsim
        }}</el-text>
        <div class="zhanwei"></div>
        <div class="zhanwei"></div>
        整体相似度最低：
        {{ lowid }}
        <div class="zhanwei"></div>
        <el-text class="mx-1" style="color: green; font-size: x-large">{{
          lowsim
        }}</el-text>
      </div>
      <div class="smallbox" >
        相似度最高的题目
        <div class="zhanwei"></div>
        <el-form
          :model="ruleForm"
          :rules="rules"
          ref="ruleForm"
          label-width="0px"
          class="demo-ruleForm"
        >
          <div
            class="VSTD_box_item"
            v-for="(item, index) in sortlist"
            :key="item.questionid"
          >
            <div>
              <el-form-item label="" prop="resource">
                <div class="zhanwei"></div>
                <div class="div-small1">{{ index + 1 }} : {{ item[0] }}</div>
                <div class="zhanwei"></div>
                <div class="div-small1">人数:{{ item[1].length }}</div>
              </el-form-item>
            </div>
          </div>
        </el-form>
        
      </div>
    </div>
    <div>
      各题较相似的同学数量展示
      <div id="myChartall" class="myChartall"></div>
      <div>
        <div style="width: 62%; margin: auto">
          <div style="float: left; width: 100%; text-align: center">
            <el-button type="primary" @click="checksubmit()"
              >详细信息</el-button
            >
          </div>
          <!-- <div style="float: left; width: 49%; text-align: center">
            <el-button type="primary" @click="viewlistfunc()"
              >查看名单</el-button
            >
          </div> -->
        </div>
      </div>
    </div>
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
      <el-table-column fixed="right" label="操作" width="200px">
        <template #default="scope">
          <el-button type="text" size="small" @click="check(scope.row)"
            >查看</el-button
          ></template
        >
      </el-table-column>
    </el-table>
  </el-dialog>
</template>
    
    <script>
import axios from "axios";
import api from "@/api";
import * as echarts from "echarts";
export default {
  data() {
    return {
      dialogTableVisible: false,
      jsondataall: [],
      input1: "",
      input2: "",
      input3: "",
      input4: "",
      homeworkname: localStorage.getItem("homeworkname"),
      highsim: 0,
      highid: "",
      lowsim: 0,
      lowid: "",
      data: [],
      sortlist: [],
      fri: [],
      sec: [],
      thr: [],
      frilen: 0,
      seclen: 0,
      thrlen: 0,
      xAxisall: {
        data: [],
      },
      tableHeader: {
        userid: "学号",
      },
      chartDataall: [],
      gridData: [],
    };
  },
  created() {
    this.get();
  },
  methods: {
    download() {
      axios
        .post(
          "http://127.0.0.1:8000/getsimilarity/getfile/",
          {
            homeworkid: localStorage.getItem("homeworkid"),
            homeworkname: localStorage.getItem("homeworkname"),
          },
          {
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            emulateJSON: true,
            responseType: "blob",
          }
        )
        .then((res) => {
          let blob = new Blob([res.data], {
            type: "application/msword", //这里需要根据不同的文件格式写不同的参数
          });

          let eLink = document.createElement("a");
          eLink.download = localStorage.getItem("homeworkname") + ".xlsx"; //给文件名和指定格式,浏览器下载时看到的
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
    get() {
      axios
        .post(
          api.url + "/homework/getHomeworkSimilarity/",
          {
            homeworkid: localStorage.getItem("homeworkid"),
            questionnum: localStorage.getItem("questionnum"),
          },
          {
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            emulateJSON: true,
          }
        )
        .then((success) => {
          this.highid = success.data.highid;
          this.highsim = success.data.highsim;
          this.lowid = success.data.lowid;
          this.lowsim = success.data.lowsim;
          this.xAxisall.data = success.data.namelist;
          this.chartDataall = success.data.lenlist;
          this.sortlist = success.data.sortlist;
          this.fri = this.sortlist[0][0];
          this.sec = this.sortlist[1][0];
          this.thr = this.sortlist[2][0];
          this.frilen = this.sortlist[0][1].length;
          this.seclen = this.sortlist[1][1].length;
          this.thrlen = this.sortlist[2][1].length;
          this.jsondataall = success.data.jsondata;
          this.drawChart();
        });
    },
    check(row) {
      this.$router.push("submitview");
      localStorage.setItem("goaluserid", row.userid);
    },
    drawChart() {
      let myChartall = echarts.init(document.getElementById("myChartall"));
      myChartall.setOption({
        xAxis: this.xAxisall,
        yAxis: { type: "value" },
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "shadow",
          },
          formatter: "{a0} <br/>题号：{b} <br />人数： {c0}",
        },
        series: [
          {
            name: "详细信息",
            type: "line",
            data: this.chartDataall,
          },
        ],
      });
      myChartall.on("click", (params) => {
        //用于做每个点的监听，只用点击点才能够获取想要的监听效果；
        // let data = {
        //   x: params.name,
        //   y: params.data,
        // };
        //alert(JSON.stringify(data));
        this.showdialog(params.name);
      });

      window.addEventListener("resize", () => {
        myChartall.resize();
      });
    },
    checksubmit() {
      this.$router.push("detail");
    },
    showdialog(name) {
      this.dialogTableVisible = true;
      this.gridData = this.jsondataall[name];
      console.log(this.gridData);
    },
  },
};
</script>
    <style scoped>
.flex_div_all {
  display: flex;
  height: 600px;
  width: 1050px;
  margin-top: 5%;
  margin-right: 2%;
  justify-content: center;
  align-items: center;
  box-shadow: 0px -0.5px 0px 0px #e5e5e5,
    /*上边阴影 */ -1.5px 0px 0px 0px #e5e5e5,
    /*左边阴影  */ 1.5px 0px 0px 0px #e5e5e5,
    /*右边阴影 */ 0px 3px 0px 0px #e5e5e5; /*下边阴影 */
}

.zhanwei {
  height: 10px;
  width: 20px;
}
.div-small1 {
  
}

.myChartall {
  width: 900px;
  height: 500px;
}
.div-small {
  width: 150px;
  height: 70px;
  margin-left: 2px;
  float: left;
  box-shadow: 0px -0.5px 0px 0px #e5e5e5, /*上边阴影 */ 0px 0px 0px 0px #e5e5e5,
    /*左边阴影  */ 0px 0px 0px 0px #e5e5e5,
    /*右边阴影 */ 0px 0.5px 0px 0px #e5e5e5; /*下边阴影 */
}
.smallbox {
  height: 300px;
  width: 150px;
  overflow:auto;
  box-shadow: 0px -0.5px 0px 0px #e5e5e5,
    /*上边阴影 */ -1.5px 0px 0px 0px #e5e5e5,
    /*左边阴影  */ 1.5px 0px 0px 0px #e5e5e5,
    /*右边阴影 */ 0px 3px 0px 0px #e5e5e5; /*下边阴影 */
}
.smallbox::-webkit-scrollbar {
        width: 0px;
    }
</style>