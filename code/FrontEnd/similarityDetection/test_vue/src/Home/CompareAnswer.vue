<template>
  <h1>{{ homeworkname }}</h1>
  <div style="display: flex">
    <div class="leftans">
        <h2>{{ username }}</h2>
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
              <span
                >相似度：({{ simidata[index][0] }},{{
                  simidata[index][1]
                }},{{ simidata[index][2] }})</span
              >
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
            <el-form-item label="答案" prop="resource">
              <el-input
                type="textarea"
                style="width: 80%"
                v-model="answerdata[index].answer"
              ></el-input>
            </el-form-item>
          </div>
          <div v-if="item.questiontype == 2" class="VSTD_box_item_select">
            <el-form-item label="答案" prop="resource">
              <el-input
                type="textarea"
                style="width: 80%"
                v-model="answerdata[index].answer"
              ></el-input>
            </el-form-item>
          </div>
          <div v-if="item.questiontype == 3" class="VSTD_box_item_select">
            <el-form-item label="答案" prop="resource">
              <el-input
                type="textarea"
                style="width: 80%"
                v-model="answerdata[index].answer"
              ></el-input>
            </el-form-item>
          </div>
          <div v-if="item.questiontype == 4" class="VSTD_box_item_select">
            <el-form-item label="答案" prop="resource">
              <el-input
                type="textarea"
                style="width: 80%"
                v-model="answerdata[index].answer"
              ></el-input>
            </el-form-item>
          </div>
        </div>

      </el-form>
    </div>
    <div  class="rightans">
        <h2>{{ compareid }}</h2>
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
              <span
                >相似度：({{ simidata[index][0] }},{{
                  simidata[index][1]
                }},{{ simidata[index][2] }})</span
              >
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
            <el-form-item label="答案" prop="resource">
              <el-input
                type="textarea"
                style="width: 80%"
                v-model="answerdata1[index].answer"
              ></el-input>
            </el-form-item>
          </div>
          <div v-if="item.questiontype == 2" class="VSTD_box_item_select">
            <el-form-item label="答案" prop="resource">
              <el-input
                type="textarea"
                style="width: 80%"
                v-model="answerdata1[index].answer"
              ></el-input>
            </el-form-item>
          </div>
          <div v-if="item.questiontype == 3" class="VSTD_box_item_select">
            <el-form-item label="答案" prop="resource">
              <el-input
                type="textarea"
                style="width: 80%"
                v-model="answerdata1[index].answer"
              ></el-input>
            </el-form-item>
          </div>
          <div v-if="item.questiontype == 4" class="VSTD_box_item_select">
            <el-form-item label="答案" prop="resource">
              <el-input
                type="textarea"
                style="width: 80%"
                v-model="answerdata1[index].answer"
              ></el-input>
            </el-form-item>
          </div>
        </div>

        <!-- 提交函数  -->

        <el-form-item> </el-form-item>
      </el-form>
    </div>
  </div>
</template>
      
      <script>
import axios from "axios";
import api from "@/api";
export default {
  data() {
    return {
      formData: new FormData(),
      username: localStorage.getItem("goaluserid"),
      homeworkname: localStorage.getItem("homeworkname"),
      ruleForm: { resource: [] },
      question: [],
      answerdata: [],
      answerdata1: [],
      simidata:[],
      compareid: localStorage.getItem("compareid"),
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
            id1:localStorage.getItem("goaluserid"),
            id2:localStorage.getItem("compareid"),
            homeworkid: localStorage.getItem("homeworkid"),
          },
          {
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            emulateJSON: true,
          }
        )
        .then((success) => {
          //console.log(success.data);
          this.simidata=success.data.simidata;
          this.question = success.data.data;
        });
      axios
        .post(
          api.url + "/homework/checkAnswer/",
          {
            userid: localStorage.getItem("goaluserid"),
            homeworkid: localStorage.getItem("homeworkid"),
          },
          {
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            emulateJSON: true,
          }
        )
        .then((success) => {
          this.answerdata = success.data.data;
        });
        axios
        .post(
          api.url + "/homework/checkAnswer/",
          {
            userid: localStorage.getItem("compareid"),
            homeworkid: localStorage.getItem("homeworkid"),
          },
          {
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            emulateJSON: true,
          }
        )
        .then((success) => {
          this.answerdata1 = success.data.data;
        });
        
      
    
    },
  },
};
</script>
      
      <style >
.homeworkout {
  background: #f6f6f6;
}
.leftans {

  width: 900px;
  box-shadow: 0px -0.5px 0px 0px #e5e5e5,
    /*上边阴影 */ -1.5px 0px 0px 0px #e5e5e5,
    /*左边阴影  */ 1.5px 0px 0px 0px #e5e5e5,
    /*右边阴影 */ 0px 3px 0px 0px #e5e5e5; /*下边阴影 */
}

.rightans{
  width: 900px;
  box-shadow: 0px -0.5px 0px 0px #e5e5e5,
    /*上边阴影 */ -1.5px 0px 0px 0px #e5e5e5,
    /*左边阴影  */ 1.5px 0px 0px 0px #e5e5e5,
    /*右边阴影 */ 0px 3px 0px 0px #e5e5e5; /*下边阴影 */
}

.pbiaoqian {
  padding: 0px 0px 0px 80px;
  width: fit-content;
  font-weight: 700;
  text-align: left;
}
.ebutton {
  display: block;
  margin: 0 auto;
}
.center {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
    