<template>
  <div>
    <div>
      <div style="float: left; text-align: right; width: 50%; margin-left: 2%">
        <h2>我的班级</h2>
      </div>
      <div style="float: right; text-align: right; width: 38%">
        <el-button
          class="new_btn"
          type="primary"
          @click="dialogFormVisible = true"
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
          <el-button type="text" size="small" @click="deleteCourse(scope.row)"
            >删除</el-button
          ></template
        >
      </el-table-column>
    </el-table>
  </div>
  <el-dialog v-model="dialogFormVisible" title="新建课程">
    <el-form :model="form">
      <el-form-item label="课程名称" :label-width="formLabelWidth">
        <el-input v-model="form.coursename" autocomplete="off" />
      </el-form-item>
      <el-form-item label="班级名称" :label-width="formLabelWidth">
        <el-input v-model="form.classname" autocomplete="off" />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogFormVisible = false">Cancel</el-button>
        <el-button type="primary" @click="creat()"> Confirm </el-button>
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
      dialogFormVisible: false,
      formLabelWidth: "140px",
      form: {
        userid: "",
        classname: "",
        coursename: "",
      },

      tableHeader: {
        courseid: "课程号",
        coursename: "课程名称",
        classname: "班级名称",
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
          api.url + "/course/list/",
          {
            userid: localStorage.getItem("userid"),
          },
          {
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            emulateJSON: true,
          }
        )
        .then((success) => {
          var jsonObj = JSON.parse(JSON.stringify(success.data.data));
          for (var i = 0; i < jsonObj.length; i++) {
            // alert( jsonObj[i].coursename);
            var str = jsonObj[i].ctime;
            var str1 = str.slice(0, 9);
            var str2 = str.slice(11, 19);
            jsonObj[i].ctime = str1 + " " + str2;
          }
          this.tableData = jsonObj;
        });
    },
    check(row) {
      localStorage.setItem("classname", row.classname);
      localStorage.setItem("coursename", row.coursename);
      localStorage.setItem("courseid", row.courseid);
      this.$router.push("homework");
    },
    deleteCourse(row) {
      this.$confirm("此操作将永久删除, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          axios
            .post(
              api.url + "/course/delete/",
              {
                courseid: row.courseid,
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
    creat() {
      if (this.form.coursename === "") {
        this.$message({ type: "info", message: "课程名必须输入！" });
      } else if (this.form.classname === "") {
        this.$message({ type: "info", message: "班级名必须输入！" });
      } else {
        axios
          .post(
            this.api.url + "/course/creat/",
            {
              userid: localStorage.getItem("userid"),
              coursename: this.form.coursename,
              classname: this.form.classname,
            },
            {
              headers: { "Content-Type": "application/x-www-form-urlencoded" },
              emulateJSON: true,
            }
          )
          .then((success) => {
            if (success.data == "创建成功") {
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
