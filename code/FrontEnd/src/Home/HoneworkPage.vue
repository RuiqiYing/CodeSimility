<template>
    <div>
      <div>
        <div style="float: left; text-align: right; width: 60%; margin-left: 2%">
          <h2>{{courseNameMsg}}的作业</h2>
        </div>
        <div style="float: right; text-align: right; width: 38%">
          <el-button class="new_btn" type="primary" @click="dialogFormVisible = true"
            >新增</el-button
          >
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
            <el-button type="text" size="small" @click="check(scope.row)"
              >查看</el-button
            >
            <el-button type="text" size="small" @click="checkSubmit(scope.row)"
              >同学</el-button
            >
            <el-button type="text" size="small" @click="deleteHomework(scope.row)"
              >删除</el-button
            ></template
          >
        </el-table-column>
      </el-table>
    </div>
    <el-dialog v-model="dialogFormVisible" title="发布作业">
    <el-form :model="form">
      <el-form-item label="作业名称" :label-width="formLabelWidth">
        <el-input v-model="form.homeworkname" autocomplete="off" />
      </el-form-item>
      <el-form-item label="题目编号" :label-width="formLabelWidth">
        <el-select v-model="form.questionnum" placeholder="请选择一套题目">
          <el-option label="习题1" value="1" />
          <el-option label="习题2" value="2" />
          <el-option label="习题3" value="3" />
          
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取消</el-button>
        <el-button type="primary" @click="creat()">
          确定
        </el-button>
      </span>
    </template>
  </el-dialog>
  </template>
  
  <script>
  import axios from "axios";
  import api from "@/api";
  export default {
    data() {
      return {
        courseNameMsg:localStorage.getItem("coursename")+"-"+localStorage.getItem("classname"),
        dialogFormVisible: false,
        formLabelWidth: "140px",
        form: {
          questionnum: "",
          homeworkname: "",
        },
  
  
        tableHeader: {
          homeworkid: "作业编号",
          questionnum:"题目编号",
          homeworkname: "作业名称",
          ctime: "添加时间",
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
            api.url + "/homework/list/",
            {
              courseid: localStorage.getItem("courseid"),
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
        
        this.$router.push('submitted')
        localStorage.setItem('homeworkname',row.homeworkname)
        localStorage.setItem('questionnum',row.questionnum)
        localStorage.setItem('homeworkid',row.homeworkid)
      },
      check(row) {
        this.$router.push('checkall')
        
        localStorage.setItem('homeworkname',row.homeworkname)
        localStorage.setItem('questionnum',row.questionnum)
        localStorage.setItem('homeworkid',row.homeworkid)
      },
      deleteHomework(row) {
        this.$confirm("此操作将永久删除, 是否继续?", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        })
          .then(() => {
            axios
              .post(
                api.url + "/homework/delete/",
                {
                  homeworkid:row.homeworkid
                },
                {
                  headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                  },
                  emulateJSON: true,
                }
              )
              .then((res) => {
                if (res.data === "删除成功") {
                  
                  location.reload();
                  this.$message.success("删除成功！");
                } else {
                  try {
                    this.$message.error(res.data);
                  } catch {
                    this.$message.error(res.data);
                  }
                }
              });
          })
          .catch(() => {
            this.$message({
              type: "info",
              message: "已取消删除",
            });
          });
      },
      creat(){
       if (this.form.homeworkname === "") {
           this.$message({ type: "info", message: "请输入作业名称" });
       } else if (this.form.questionnum === "") {
           this.$message({ type: "info", message: "请选择习题" });
       } else {
         axios
           .post(
               this.api.url + "/homework/creat/",
               { courseid:localStorage.getItem("courseid"), questionnum: this.form.questionnum,homeworkname:this.form.homeworkname },
               {
                   headers: { "Content-Type": "application/x-www-form-urlencoded" },
                   emulateJSON: true,
               }
           )
           .then((success) => {
               if (success.data == '创建成功') {
                   this.$message({ type: "success", message: "创建成功" });
                   this.dialogFormVisible = false;
                   location.reload();
               } 
           });
       }
     },
    },
  };
  </script>
  