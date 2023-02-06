<template>

  <div class="login-wrap">

    <div class="ms-title" style="font-size: 30px">
      相似度检测系统-登录<span style="font-size: 10px; margin-left: 0px">
        <u></u></span>
    </div>

    <div class="demo-input-suffix ms-login" style="width:300px">
      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" class="demo-ruleForm">
        <el-form-item prop="username">
          <el-input v-model="ruleForm.username" placeholder="请输入用户名"></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="ruleForm.password" type="password" placeholder="请输入密码"></el-input>
        </el-form-item>

        <el-form-item class="login-btn">
          <div style="width:145px" class="choose"> <el-select v-model="value" placeholder="请选择身份">
              <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select></div>
          <div style="width:30px" class="choose">

          </div>
          <div class="choose"> <el-button type="primary" @click="submit()" style="width:80px">登录</el-button></div>
          <el-form-item>
            <el-button type="text" @click="dialogFormVisible = true">忘记密码</el-button>

            <el-button type="text" @click="registerDialogFormVisible = true">注册</el-button>
          </el-form-item>
        </el-form-item>

      </el-form>
      <el-dialog title="修改密码" :visible.sync="dialogFormVisible">
        <el-form :model="form">
          <el-form-item label="手机号" :label-width="formLabelWidth">
            <el-input v-model="form.id" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="新密码" :label-width="formLabelWidth">
            <el-input v-model="form.newpwd" autocomplete="off"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogFormVisible = false">取 消</el-button>
          <el-button type="primary" @click="forget(); dialogFormVisible = false">确 定</el-button>
        </div>
      </el-dialog>

      <el-dialog title="注册" :visible.sync="registerDialogFormVisible">
        <el-form :model="registerForm">
          <el-form-item label="手机号" :label-width="formLabelWidth">
            <el-input v-model="registerForm.id" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="密码" :label-width="formLabelWidth">
            <el-input v-model="registerForm.password" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="昵称" :label-width="formLabelWidth">
            <el-input v-model="registerForm.username" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="身份" :label-width="formLabelWidth">
            <el-select v-model="registerForm.role" placeholder="请选择身份">
              <el-option label="教师" value="0"></el-option>
              <el-option label="学生" value="1"></el-option>
            </el-select>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="registerDialogFormVisible = false">取 消</el-button>
          <el-button type="primary" @click="register();registerDialogFormVisible = false">确 定</el-button>
        </div>
      </el-dialog>
    </div>
  </div>

</template>


<script>
const globalProperties = getCurrentInstance().appContext.config.globalProperties; // 获取全局挂载
export default {
  data:

    function () {
      return {
        registerDialogFormVisible: false,
        registerForm: {
          id: '',
          username: '',
          role: '',
          password: '',
        },
        dialogFormVisible: false,
        form: {
          id: '',
          newpwd: '',
        },
        formLabelWidth: '120px',
        options: [{
          value: '0',
          label: '教师'
        }, {
          value: '1',
          label: '学生'
        },],
        value: '',
        dialogVisible: false,
        ruleForm: {
          username: "",
          password: "",
          role: "",
        },
        rules: {
          username: [
            { required: true, message: "请输入用户名", trigger: "blur" },
          ],
          password: [{ required: true, message: "请输入密码", trigger: "blur" }],
        },
      };
    },

  created() {
    localStorage.setItem("username", "");
    localStorage.setItem("userid", "");
    localStorage.setItem("role", "");
    localStorage.setItem("pwd", "");
  },
  methods: {
    register(){  //注册
      if(this.registerForm.id === ""){
        this.$message({ type: "info", message: "用户名必须输入！" });
      }else if(this.registerForm.password=== ""){
        this.$message({ type: "info", message: "密码必须输入！" });
      }else if(this.registerForm.username=== ""){
        this.$message({ type: "info", message: "昵称必须输入！" });
      }else if (this.registerForm.role=== ""){
        this.$message({ type: "info", message: "请选择身份" });
      }
      else{
        this.$http
          .post(
            URL + "/login/register/",
            { userid: this.registerForm.id, password: this.registerForm.newpwd ,role:this.registerForm.role,username:this.registerForm.username},
            {
              headers: { "Content-Type": "application/x-www-form-urlencoded" },
              emulateJSON: true,
            }
          )
          .then((success) => {
            if (success.data == '注册成功') {
              this.$message({ type: "success", message: "注册成功" });

            } else if (success.data == '用户已存在') {

              this.$message({ type: "error", message: "用户已存在" });
            }
           
          });
      }
    },
    forget() {
      //  console.log(11111);

      //  this.$message({ type: "info", message:this.form.newpwd  });
      if (this.form.id === "") {
        this.$message({ type: "info", message: "用户名必须输入！" });
      } else if (this.form.newpwd === "") {
        this.$message({ type: "info", message: "密码必须输入！" });
      } else {
        this.$http
          .post(
            main.url + "/login/pwd_update/",
            { userid: this.form.id, password: this.form.newpwd },
            {
              headers: { "Content-Type": "application/x-www-form-urlencoded" },
              emulateJSON: true,
            }
          )
          .then((success) => {
            if (success.data == '修改成功') {
              this.$message({ type: "success", message: "修改成功" });

            } else if (success.data == '新旧密码相同') {

              this.$message({ type: "error", message: "新旧密码相同" });
            }
            else if (success.data == '用户名不存在！') {
              this.$message({ type: "error", message: "用户名不存在" });
            }
          });
      }

    },
    submit() {
      if (this.ruleForm.username === "") {
        this.$message({ type: "info", message: "用户名必须输入！" });
      } else if (this.ruleForm.password === "") {
        this.$message({ type: "info", message: "密码必须输入！" });
      } else {
        let crypto = require("crypto");
        const md5 = crypto.createHash("md5");
        md5.update(this.ruleForm.password);
        let md5password = md5.digest("hex");
        this.$http
          .post(
            main.url + "/login/",
            { userid: this.ruleForm.username, password: this.ruleForm.password, role: this.value },
            {
              headers: { "Content-Type": "application/x-www-form-urlencoded" },
              emulateJSON: true,
            }
          )
          .then((success) => {
            if (success.data != '密码错误') {
              this.$message({ type: "success", message: "登录成功" });
              // localStorage.setItem("userid", this.ruleForm.username);
              // localStorage.setItem("role", this.ruleForm.role);
              // localStorage.setItem("pwd", this.ruleForm.password);
              this.$router.push({ path: "/admin" });
              this.ruleForm.username = "";
            } else {

              this.$message({ type: "error", message: "用户名或密码错误" });
            }
            this.ruleForm.password = "";
            this.dialogVisible = true;
          });
      }
    },

    cancel() {
      this.$router.push({ path: "/" });
    },
  },
};
</script>

<style scoped>
.login-wrap {
  position: relative;
  background: url("/static/img/bg.jpg") no-repeat center;
  width: 100%;
  height: 100%;
}

.choose {
  display: inline-block;
}

.ms-title {
  position: absolute;
  top: 49%;
  width: 100%;
  margin-top: -230px;
  text-align: center;
  font-size: 14px;
  color: #fff;
  font-weight: bold;
}

.ms-login {
  position: absolute;
  left: 50%;
  top: 45%;
  width: 300px;
  height: 160px;
  margin: -150px 0 0 -190px;
  padding: 40px;
  border-radius: 20px;
  background: #fff;
}

.login-btn {
  text-align: center;
}

.demo-ruleForm {
  vertical-align: middle;
}

.login-btn button {
  width: 40%;
  height: 35px;
  left: 80px;
}
</style>
