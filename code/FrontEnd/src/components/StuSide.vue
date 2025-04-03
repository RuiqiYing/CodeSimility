<template>
    <el-menu
      router
      active-text-color="#ffd04b"
      background-color="#545c64"
      class="el-menu-vertical-demo"
      default-active="/stucourse"
      text-color="#fff"
      style="height:200px"
    >
      <el-menu-item index="/stucourse">
        <el-icon><icon-menu /></el-icon>
        <span>课程</span>
      </el-menu-item>
      <el-menu-item index="/stuinformation">
        <el-icon><document /></el-icon>
        <span>个人信息</span>
      </el-menu-item>
    </el-menu>
  </template>
    
    <!-- <script lang="ts" setup>
    import {
      Document,
      Menu as IconMenu,
      Location,
      Setting,
    } from '@element-plus/icons-vue'
    const handleOpen = (key: string, keyPath: string[]) => {
      console.log(key, keyPath)
    }
    const handleClose = (key: string, keyPath: string[]) => {
      console.log(key, keyPath)
    }
    </script> -->
    
    <!-- <style>
  .tac{
      width: 200px;
      height: 100%;
  }
  </style> -->