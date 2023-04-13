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
export default {
  data() {
    return {
      formData: new FormData(),
      homeworkname: localStorage.getItem("homeworkname"),
      ruleForm: { resource: [] },
      question: [],
    };
  },
  created() {
    this.get();
  },
  methods: {
    submitAll(){
    var json={}
    json.userid=localStorage.getItem("userid")
    json.homeworkid=localStorage.getItem("homeworkid")
    json.questionnum=localStorage.getItem("questionnum")
    console.log(this.ruleForm.resource.length)
    var jsondata=[]

    for(var i=0;i<this.ruleForm.resource.length;i++){
      var temp={};
      if(temp.questiontype!="4"){
      temp.questionid=this.question[i].questionid
      temp.questiontype=this.question[i].questiontype
      temp.question=this.question[i].question
      temp.answer=this.ruleForm.resource[i]
      jsondata.push(temp)
      }
    }
    json.data=jsondata
     console.log( json)
      axios
        .post( api.url +"/homework/submit/", json, {
          headers: {
            "Content-Type": "application/json",
          },
        })
        .then((success) => {
          this.$message({ type: "success", message: success.data });
          this.$router.push("stuhomework");
        });
     },
    getFile(event) {
      this.videoFile = event.currentTarget.files[0];
    },
    post(questionid,questiontype) {
      let params = new FormData();
      params.append("questionid", questionid);
      params.append("userid", localStorage.getItem("userid"));
      params.append("file", this.videoFile);
      params.append("questionnum", localStorage.getItem("questionnum"));
      params.append("homeworkid", localStorage.getItem("homeworkid"));
      params.append("questiontype", questiontype);
      axios
        .post( api.url +"/homework/submitcode/", params, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((success) => {
          this.$message({ type: "success", message: success.data });
        });
    },

    // toUploadFile() {
    //   let btn = document.getElementById("unloadFile");
    //   btn.click();
    //   this.dialogVisible = false;
    //   this.uploadPercent = 0;
    //   this.onSubmit()
    // },

    // onSubmit() {

    //   this.formData.append("questionnum", localStorage.getItem("questionnum"));
    //   this.formData.append("userid", localStorage.getItem("userid"));
    //   this.formData.append("homeworkid", localStorage.getItem("homeworkid"));
    //   console.log(this.formData)
    //   // axios
    //   //   .post("/homework/submitcode/", this.formData)
    //   //   .then((success) => {
    //   //     this.$notify({
    //   //       title: "成功",
    //   //       message: success,
    //   //       type: "success",
    //   //     });
    //   //     this.$router.push({ path: "/filemanage/data" });
    //   //   })

    // },
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
          //console.log(success.data);
          this.question = success.data.data;
        });
    },
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
          //console.log(success.data);
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
