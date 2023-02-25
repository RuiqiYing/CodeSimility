<template>
  <h2>{{ username1 }}与{{ username2 }}的对比情况</h2>
  <div class="flex_div">
    <div class="infor_div">
      <div class="small_div" style="height: 220px">
        <h2>选择题目</h2>
        <div style="width: 150px; margin-left: 12%">
          <el-input
            style="height: 40px"
            v-model="questionid"
            placeholder="请输入题目ID"
          ></el-input>
          <div style="height: 10px"></div>
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
        </div>
        <el-button class="button" type="primary" @click="check()" plain
          >查看</el-button
        >
      </div>
      <div style="height: 30px"></div>
      <div class="small_div" style="height: 450px">
        <h2>详细信息</h2>
        <div>
          <div class="text_div">姓名1: {{ name1 }}</div>
          <div class="text_div">姓名2: {{ name2 }}</div>
          <div class="text_div">相似度:{{ similarity }}</div>
          <div style="height: 20px"></div>
          <el-button
            class="button"
            type="primary"
            @click="checkquestion()"
            plain
            >查看题目</el-button
          >
        </div>
      </div>
    </div>
    <div class="diff_div">
      <code-diff
        :old-string="answer1"
        :new-string="answer2"
        file-name="test.txt"
        output-format="side-by-side"
      />
    </div>
  </div>
  <el-dialog
    v-model="dialogVisible"
    title="题目"
    width="30%"
    :before-close="handleClose"
  >
    <span>{{ question }}</span>
    <template #footer>
      <span class="dialog-footer">
        <el-button type="primary" @click="dialogVisible = false">
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
      username1: localStorage.getItem("input2"),
      username2: localStorage.getItem("input3"),
      questionid: "",
      value2: "",
      question: "",
      name1: "",
      name2: "",
      similarity: "",
      algorithm: "",
      answer1: "",
      answer2: "",
      dialogVisible: false,
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
  methods: {
    get() {
      axios
        .post(
          api.url + "/information/getusername/",
          {
            userid: localStorage.getItem("input2"),
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
          api.url + "/information/getusername/",
          {
            userid: localStorage.getItem("input3"),
          },
          {
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            emulateJSON: true,
          }
        )
        .then((success) => {
          this.name2 = success.data;
        });
    },
    check() {
      axios
        .post(
          api.url + "/getsimilarity/compare/",
          {
            userid1: localStorage.getItem("input2"),
            userid2: localStorage.getItem("input3"),
            questionid: this.questionid,
            algorithm: this.value2,
          },
          {
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            emulateJSON: true,
          }
        )
        .then((success) => {
          // console.log(success.data)
          this.answer1 = success.data.answer1;
          this.answer2 = success.data.answer2;
          this.similarity = success.data.similarity;
          this.question = success.data.question;
        });
    },
    checkquestion() {
      this.dialogVisible = true;
    },
  },
};
</script>
  
  <style >
.flex_div {
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

.infor_div {
  width: 200px;
}
.diff_div {
  width: 100%;
  overflow:auto;
  /* margin-left: 20px; */
  box-shadow: 0px -1px 0px 0px #e5e5e5, /*上边阴影 */ -1px 0px 0px 0px #e5e5e5,
    /*左边阴影  */ 0.2px 0px 0px 0px #e5e5e5,
    /*右边阴影 */ 0px 1px 0px 0px #e5e5e5; /*下边阴影 */
}

.small_div {
  margin-top: -10%;
  width: 200px;
  position: relative;
  background-color: #f3f3f3;
  box-shadow: 0px -0.5px 0px 0px #e5e5e5, /*上边阴影 */ -1px 0px 0px 0px #e5e5e5,
    /*左边阴影  */ 0.2px 0px 0px 0px #e5e5e5,
    /*右边阴影 */ 0px 1px 0px 0px #e5e5e5; /*下边阴影 */
}
.text_div {
  text-align: left;
  margin-left: 22px;
  height: 30px;
}
</style>