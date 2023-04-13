<template>
    <div>
      <div>
        <div style="float: left; text-align: right; width: 60%; margin-left: 2%">
          <h2>{{courseNameMsg}}的作业提交情况</h2>
        </div>
        <div style="float: right; text-align: right; width: 38%">
         
        </div>
      </div>
      <el-table
        :data="tableData"
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
        <el-table-column fixed="right" label="操作" width="200px">
          <template #default="scope">
            <el-button type="text" size="small" @click="checkSubmit(scope.row)"
              >查看</el-button
            >
            </template
          >
        </el-table-column>
      </el-table>
    </div>
    
  </template>
  
  <script>
  import axios from "axios";
  import api from "@/api";
  export default {
    data() {
      return {
        courseNameMsg:localStorage.getItem("homeworkname"),
        dialogFormVisible: false,
        formLabelWidth: "140px",
        form: {
          questionnum: "",
          homeworkname: "",
        },
  
  
        tableHeader: {
          homeworkid: "作业编号",
          questionnum:"题目编号",
          userid: "学号",
          ctime: "提交时间",
        },
        tableData: [],
      };
    },
    created() {
      this.get();
    },
    methods: {
      get() {
        axios
          .post(
            api.url + "/homework/getsubmitlist/",
            {
                homeworkid: localStorage.getItem("homeworkid"),
            },
            {
              headers: { "Content-Type": "application/x-www-form-urlencoded" },
              emulateJSON: true,
            }
          )
          .then((success) => {
            var jsonObj = JSON.parse(JSON.stringify(success.data.data));
            for (var i = 0; i < jsonObj.length; i++) {
              var str = jsonObj[i].ctime;
              var str1 = str.slice(0, 9);
              var str2 = str.slice(11, 19);
              jsonObj[i].ctime = str1 + " " + str2;
            }
            this.tableData = jsonObj;
          });
      },
      checkSubmit(row){
        this.$router.push('submitview')
        localStorage.setItem('goaluserid',row.userid)
        localStorage.setItem('questionnum',row.questionnum)
        localStorage.setItem('homeworkid',row.homeworkid)
      },
      
     
    },
  };
  </script>
  