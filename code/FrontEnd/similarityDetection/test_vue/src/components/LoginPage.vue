<template>
  <div class="login-wrap">
    <div class="ms-title" style="font-size: 30px">
      相似度检测系统-登录<span style="font-size: 10px; margin-left: 0px">
        <u></u
      ></span>
    </div>

    <div class="demo-input-suffix ms-login" style="width: 300px">
      <el-form
        :model="ruleForm"
        :rules="rules"
        ref="ruleForm"
        class="demo-ruleForm"
      >
        <el-form-item prop="username">
          <el-input
            v-model="ruleForm.username"
            placeholder="请输入用户名"
          ></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            v-model="ruleForm.password"
            type="password"
            placeholder="请输入密码"
          ></el-input>
        </el-form-item>

        <el-form-item class="login-btn">
          <div style="width: 145px" class="choose">
            <el-select v-model="value" placeholder="请选择身份">
              <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              >
              </el-option>
            </el-select>
          </div>
          <div style="width: 30px" class="choose"></div>
          <div class="choose">
            <el-button type="primary" style="width: 80px" @click="submit()"
              >登录</el-button
            >
          </div>
        </el-form-item>
        <div>
          <el-button type="text" @click="dialogFormVisible = true"
            >忘记密码</el-button
          >

          <el-button type="text"   @click="registerDialogFormVisible = true " 
            >注册</el-button
          >
        </div>
      </el-form>

      <el-dialog v-model="dialogFormVisible" title="忘记密码">
        <el-form :model="form">
          <el-form-item label="输入用户名" :label-width="formLabelWidth">
            <el-input v-model="form.id" autocomplete="off" />
          </el-form-item>
          <el-form-item label="输入新密码" :label-width="formLabelWidth">
            <el-input
              v-model="form.newpwd"
              type="password"
              autocomplete="off"
            />
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="dialogFormVisible = false">取消</el-button>
            <el-button
              type="primary"
              @click="
                forget();
                dialogFormVisible = false;
              "
            >
              提交
            </el-button>
          </span>
        </template>
      </el-dialog>

      <el-dialog v-model="registerDialogFormVisible" title="注册">
        <el-form :model="registerForm">
          <el-form-item label="手机号" :label-width="formLabelWidth">
            <el-input v-model="registerForm.id" autocomplete="off" />
          </el-form-item>
          <el-form-item label="密码" :label-width="formLabelWidth">
            <el-input
              v-model="registerForm.password"
              type="password"
              autocomplete="off"
            />
          </el-form-item>
          <el-form-item label="昵称" :label-width="formLabelWidth">
            <el-input v-model="registerForm.username" autocomplete="off" />
          </el-form-item>
          <el-form-item label="身份" :label-width="formLabelWidth">
            <el-select v-model="registerForm.role" placeholder="选择身份">
              <el-option label="教师" value="0" />
              <el-option label="学生" value="1" />
            </el-select>
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="registerDialogFormVisible = false"
              >取消</el-button
            >
            <el-button
              type="primary"
              @click="register();registerDialogFormVisible = false"
            >
              提交
            </el-button>
          </span>
        </template>
      </el-dialog>
    </div>
    
  </div> 
</template>


<script >
import axios from "axios";
import api from "@/api";
export default {
  name: "LoginPage",
  props: {
    msg: String,
  },

  data: function () {
    return {
      options: [
        {
          value: "0",
          label: "教师",
        },
        {
          value: "1",
          label: "学生",
        },
      ],
      value: "",
      form: {
        id: "",
        newpwd: "",
      },

      registerDialogFormVisible: false,
      dialogFormVisible: false,
      formLabelWidth: "140px",

      ruleForm: {
        username: "",
        password: "",
        role: "",
      },

      registerForm: {
        id: "",
        username: "",
        role: "",
        password: "",
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
    register() {
      //注册
      if (this.registerForm.id === "") {
        this.$message({ type: "info", message: "用户名必须输入！" });
      } else if (this.registerForm.password === "") {
        this.$message({ type: "info", message: "密码必须输入！" });
      } else if (this.registerForm.username === "") {
        this.$message({ type: "info", message: "昵称必须输入！" });
      } else if (this.registerForm.role === "") {
        this.$message({ type: "info", message: "请选择身份" });
      } else {
        axios
          .post(
            api.url + "/login/register/",
            {
              userid: this.registerForm.id,
              password: this.registerForm.password,
              role: this.registerForm.role,
              username: this.registerForm.username,
            },
            {
              headers: { "Content-Type": "application/x-www-form-urlencoded" },
              emulateJSON: true,
            }
          )
          .then((success) => {
            if (success.data == "注册成功") {
              this.$message({ type: "success", message: "注册成功" });
            } else if (success.data == "用户已存在") {
              this.$message({ type: "error", message: "用户已存在" });
            }
          });
      }
    },
    forget() {
     
      if (this.form.id === "") {
          this.$message({ type: "info", message: "用户名必须输入！" });
      } else if (this.form.newpwd === "") {
          this.$message({ type: "info", message: "密码必须输入！" });
      } else {

        axios
          .post(
              this.api.url + "/login/pwd_update/",
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
    jump(){
      this.$router.push('movie')
    },
    submit() {
      if (this.ruleForm.username === "") {
        this.$message({ type: "info", message: "用户名必须输入！" });
      } else if (this.ruleForm.password === "") {
        this.$message({ type: "info", message: "密码必须输入！" });
      } else {
        axios
          .post(
            api.url + "/login/",
            {
              userid: this.ruleForm.username,
              password: this.ruleForm.password,
              role: this.value,
            },
            {
              headers: { "Content-Type": "application/x-www-form-urlencoded" },
              emulateJSON: true,
            }
          )
          .then((response) => {
            if (response.data == "登录成功") {
                localStorage.setItem("userid",this.ruleForm.username);
                localStorage.setItem("pwd",this.ruleForm.password);
                localStorage.setItem("role",this.ruleForm.role);
               
              this.$message({ type: "info", message: response.data });
              this.$router.push('home')
            } else if (response.data != "登录成功") {
              this.$message({ type: "info", message: response.data });
            }
          })
          .catch((response) => {
            alert(response.data);
          });
      }
    },

    // cancel() {
    //     this.$router.push({ path: "/" });
    // },
  },
};
</script>

<style scoped>
.login-wrap {
  background-image: url("../assets/img/bg.png");
  width: 100%;
  height: 100%;

  overflow: auto;
  background-repeat: no-repeat;
  position: fixed;
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
