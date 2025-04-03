<template>
  <div>
    <div>
      <div style="float: left; text-align: right; width: 50%; margin-left: 2%">
        <h2>我的课程</h2>
      </div>
      <div style="float: right; text-align: right; width: 38%">
        <el-button
          class="new_btn"
          type="primary"
          @click="dialogFormVisible = true"
          >加入</el-button
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
        </template>
      </el-table-column>
    </el-table>
  </div>
  <el-dialog v-model="dialogFormVisible" title="加入课程">
    <el-form :model="form">
      <el-form-item label="课程ID" :label-width="formLabelWidth">
        <el-input v-model="form.courseid" autocomplete="off" />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取消</el-button>
        <el-button type="primary" @click="joinCourse()"> 提交 </el-button>
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
        courseid: "",
      },

      tableHeader: {
        courseid: "课程号",
        coursename: "课程名称",
        classname: "班级名称",
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
          api.url + "/stuCourse/viewStuCourse/",
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
          console.log(jsonObj);
          this.tableData = jsonObj;
        });
    },
    check(row) {
      localStorage.setItem("classname", row.classname);
      localStorage.setItem("coursename", row.coursename);
      localStorage.setItem("courseid", row.courseid);
      this.$router.push("stuhomework");
    },
    // deleteCourse(row) {
    //   this.$confirm("此操作将永久删除, 是否继续?", "提示", {
    //     confirmButtonText: "确定",
    //     cancelButtonText: "取消",
    //     type: "warning",
    //   })
    //     .then(() => {
    //       axios
    //         .post(
    //           api.url + "/course/delete/",
    //           {
    //             courseid: row.courseid,
    //           },
    //           {
    //             headers: {
    //               "Content-Type": "application/x-www-form-urlencoded",
    //             },
    //             emulateJSON: true,
    //           }
    //         )
    //         .then((res) => {
    //           if (res.data === "删除成功") {
    //             location.reload();
    //             this.$message.success("删除成功！");
    //           } else {
    //             try {
    //               this.$message.error(res.data);
    //             } catch {
    //               this.$message.error(res.data);
    //             }
    //           }
    //         });
    //     })
    //     .catch(() => {
    //       this.$message({
    //         type: "info",
    //         message: "已取消删除",
    //       });
    //     });
    // },
    joinCourse() {
      if (this.form.coursename === "") {
        this.$message({ type: "info", message: "课程ID必须输入！" });
      } else {
        axios
          .post(
            this.api.url + "/stuCourse/join/",
            {
              userid: localStorage.getItem("userid"),
              courseid: this.form.courseid,
            },
            {
              headers: { "Content-Type": "application/x-www-form-urlencoded" },
              emulateJSON: true,
            }
          )
          .then((success) => {
            if (success.data == "加入成功") {
              this.$message({ type: "success", message: "加入成功" });
              this.dialogFormVisible = false;
              location.reload();
            } else if (success.data == "课程不存在，检查课程ID") {
              this.$message({
                type: "error",
                message: "课程不存在，检查课程ID",
              });
            } else if (success.data == "你已加入该课程") {
              this.$message({ type: "error", message: "你已加入该课程" });
            }
          });
      }
    },
  },
};
</script>
