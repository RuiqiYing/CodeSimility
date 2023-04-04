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
            <input
              type="file"
              id="avatar"
              name="avatar"
              accept="txt"
              multiple
              required
              @change="changeFile"
            />
          </el-form-item>
        </div>
      </div>

      <!-- 提交函数  -->

      <!-- <el-form-item style="text-align: center">
          <el-button type="primary" @click="submitForm('ruleForm', false)"
            >提交</el-button
          >
        </el-form-item> -->
    </el-form>
  </div>
</template>
  
  <script>
import axios from "axios";
import api from "@/api";
export default {
  data() {
    return {
      homeworkname: localStorage.getItem("homeworkname"),
      ruleForm: { resource: [] },
      question: [],
    };
  },
  created() {
    this.get();
  },
  methods: {
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
          console.log(success.data);
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
</style>
