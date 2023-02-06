<template>
    <div>
     <el-row class="tac">
     <el-col :span="4">   
      <el-menu
       default-active="1"
        class="el-menu-vertical-demo"
        @open="handleOpen"
        @close="handleClose"
        background-color="#545c64"
        text-color="#fff"
        active-text-color="#ffd04b"
        router
        >
        <el-submenu index="1">
          <template slot="title">
            <i class="el-icon-s-platform"></i>
            <span>班级管理</span>
          </template>
          <el-menu-item-group>
            <el-menu-item index="/index/menu1" >我的班级</el-menu-item>
            <el-menu-item index="/index/menu2">新建班级</el-menu-item>
          </el-menu-item-group>
        </el-submenu>
         <el-submenu index="2">
          <template slot="title">
            <i class="el-icon-s-tools"></i>
            <span>相似度查看</span>
          </template>
          <el-menu-item-group>
            <el-menu-item index="1-1">权限管理</el-menu-item>
            <el-menu-item index="1-2">角色管理</el-menu-item>
          </el-menu-item-group>
        </el-submenu>
        <el-submenu index="3">
          <template slot="title">
            <i class="el-icon-user-solid"></i>
            <span>我的信息</span>
          </template>
          <el-menu-item-group>        
            <el-menu-item index="1-1">人员数量</el-menu-item>
            <el-menu-item index="1-2">人员位置</el-menu-item>
          </el-menu-item-group>
        </el-submenu>      
       
      </el-menu>
    </el-col>
  </el-row>
    </div>
  </template>
  <script>
    export default {
      methods: {
        handleOpen(key, keyPath) {
          console.log(key, keyPath);
        },
        handleClose(key, keyPath) {
          console.log(key, keyPath);
        }
      }
    }
  </script>