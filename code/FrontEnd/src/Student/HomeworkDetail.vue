<template>
  <h1>{{ homeworkname }}</h1>
  <div class="homeworkout">
    <el-form
      :model="ruleForm"
      :rules="rules"
      ref="ruleForm"
      label-width="100px"
      class="demo-ruleForm"
    >
      <!-- 循环后端给你的所有题 -->
      <div
        class="VSTD_box_item"
        v-for="(item, index) in question"
        :key="item.questionid"
      >
        <!-- 1 单选 -->
        <!-- 2 判断 -->
        <!-- 3 多选 -->
        <!-- 4 简答 -->

        <div class="VSTD_box_item_title">
          <!-- 题目的信息 -->
          <p class="pbiaoqian">
            第{{ index + 1 }}题：{{ item.question }}
            <span v-if="item.questiontype == 1">（选择）</span>
            <span v-if="item.questiontype == 2">（填空）</span>
            <span v-if="item.questiontype == 3">（简答）</span>
            <span v-if="item.questiontype == 4">（代码）</span>
          </p>
        </div>

        <!-- 如果questionType 等于1 那么他是单选题 -->
        <!-- 题目绑定的值是 ruleForm.resource[index]  -->

        <div v-if="item.questiontype == 1" class="VSTD_box_item_select">
          <el-form-item label="" prop="resource">
            <el-radio-group v-model="ruleForm.resource[index]">
              <el-radio label="A">{{ item.optionA }}</el-radio>
              <el-radio label="B">{{ item.optionB }}</el-radio>
              <el-radio label="C">{{ item.optionC }}</el-radio>
              <el-radio label="D">{{ item.optionD }}</el-radio>
            </el-radio-group>
          </el-form-item>
        </div>
        <div v-if="item.questiontype == 2" class="VSTD_box_item_select">
          <el-form-item label="" prop="resource">
            <el-input
              type="textarea"
              style="width: 80%"
              v-model="ruleForm.resource[index]"
            ></el-input>
          </el-form-item>
        </div>
        <div v-if="item.questiontype == 3" class="VSTD_box_item_select">
          <el-form-item label="" prop="resource">
            <el-input
              type="textarea"
              style="width: 80%"
              v-model="ruleForm.resource[index]"
            ></el-input>
          </el-form-item>
        </div>
        <div v-if="item.questiontype == 4" class="VSTD_box_item_select">
          <el-form-item label="" prop="resource">
            <!-- <el-input
             
              v-model="ruleForm.resource[index]"
            ></el-input> -->
            <input type="file" @change="getFile($event)" />

            <el-button type="primary" @click="post(item.questionid,item.questiontype)">确 定</el-button>
          </el-form-item>
        </div>
      </div>

      <!-- 提交函数  -->

      <el-form-item >
        
          </el-form-item>
    </el-form>
    <div class="center"><el-button class="ebuton" type="primary" @click="submitAll()"
            >提交</el-button
          >
        </div>
  </div>

</template>
<script>
import axios from "axios";
import api from "@/api";
import pLimit from 'p-limit';
export default {
  data() {
    return {
      formData: new FormData(),
      homeworkname: localStorage.getItem("homeworkname"),
      ruleForm: { resource: [] },
      question: [],
      videoFile: null, // 用于存储上传的视频文件
    };
  },
  created() {
    this.get();
  },
  methods: {
    submitAll() {
      const limit = pLimit(3); // 限制并发数量为 3

      const json = {
        userid: localStorage.getItem("userid"),
        homeworkid: localStorage.getItem("homeworkid"),
        questionnum: localStorage.getItem("questionnum"),
        data: [],
      };

      const promises = [];

      // 循环处理每一个题目
      for (let i = 0; i < this.ruleForm.resource.length; i++) {
        const questionItem = this.question[i];
        const answer = this.ruleForm.resource[i];

        // 如果是非视频类题目（questiontype != "4"）
        if (questionItem.questiontype !== "4") {
          const temp = {
            questionid: questionItem.questionid,
            questiontype: questionItem.questiontype,
            question: questionItem.question,
            answer: answer,
          };
          json.data.push(temp);
        } else {
          // 对视频类题目使用并发控制上传
          const uploadPromise = limit(() => this.post(questionItem.questionid, questionItem.questiontype));
          promises.push(uploadPromise);
        }
      }

      // 提交非视频类题目
      axios
        .post(api.url + "/homework/submit/", json, {
          headers: {
            "Content-Type": "application/json",
          },
        })
        .then((success) => {
          this.$message({ type: "success", message: "主观题提交成功：" + success.data });

          // 并行提交视频题目并等待全部完成
          return Promise.all(promises);
        })
        .then(() => {
          this.$message({ type: "success", message: "所有视频题目提交成功" });
          this.$router.push("stuhomework");
        })
        .catch((err) => {
          this.$message.error("提交过程中发生错误：" + err);
        });
    },

    // 获取文件
    getFile(event) {
      this.videoFile = event.currentTarget.files[0];
    },

    // 上传视频文件
    post(questionid, questiontype) {
      const params = new FormData();
      params.append("questionid", questionid);
      params.append("userid", localStorage.getItem("userid"));
      params.append("file", this.videoFile); // 你可以改为视频文件数组，处理多个文件
      params.append("questionnum", localStorage.getItem("questionnum"));
      params.append("homeworkid", localStorage.getItem("homeworkid"));
      params.append("questiontype", questiontype);

      return axios.post(api.url + "/homework/submitcode/", params, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }).then((success) => {
        this.$message({ type: "success", message: success.data });
      });
    },

    // 获取题目列表
    changeFile() {
      axios
        .post(
          api.url + "/homework/submitcode/",
          {
            questionnum: localStorage.getItem("questionnum"),
          },
          {
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            emulateJSON: true,
          }
        )
        .then((success) => {
          this.question = success.data.data;
        });
    },

    // 获取题目
    get() {
      axios
        .post(
          api.url + "/stuCourse/getquestionlist/",
          {
            questionnum: localStorage.getItem("questionnum"),
          },
          {
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            emulateJSON: true,
          }
        )
        .then((success) => {
          this.question = success.data.data;
        });
    },
  },
};
</script>
  
  <style >
.homeworkout {
  background: #f6f6f6;
  width: 90%;
  position: absolute;
  top: 10%;
  left: 0;
  right: 0;
  margin: auto;
}

.pbiaoqian {
  padding: 0px 0px 0px 80px;
  width: fit-content;
  font-weight: 700;
  text-align: left;
}
.ebutton{
  display: block;
  margin: 0 auto;
}
.center{
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
