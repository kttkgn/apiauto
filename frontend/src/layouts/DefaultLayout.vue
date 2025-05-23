<template>
  <el-container class="layout-container">
    <el-aside width="200px">
      <el-menu
        :router="true"
        :default-active="route.path"
        class="el-menu-vertical"
      >
        <el-menu-item index="/">
          <el-icon><HomeFilled /></el-icon>
          <span>首页</span>
        </el-menu-item>
        <el-menu-item index="/cases">
          <el-icon><Document /></el-icon>
          <span>用例管理</span>
        </el-menu-item>
        <el-menu-item index="/environments">
          <el-icon><Setting /></el-icon>
          <span>环境配置</span>
        </el-menu-item>
        <el-menu-item index="/executions">
          <el-icon><VideoPlay /></el-icon>
          <span>执行管理</span>
        </el-menu-item>
        <el-menu-item index="/reports">
          <el-icon><DataLine /></el-icon>
          <span>测试报告</span>
        </el-menu-item>
        <el-menu-item index="/variables">
          <el-icon><List /></el-icon>
          <span>参数管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header>
        <div class="header-left">
          <h2>接口自动化平台</h2>
        </div>
        <div class="header-right">
          <!-- Remove user info and dropdown -->
        </div>
      </el-header>
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import {
  HomeFilled,
  Document,
  Setting,
  VideoPlay,
  DataLine,
  List
} from '@element-plus/icons-vue'

const route = useRoute()
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

.el-aside {
  background-color: #304156;
  color: #fff;
}

.el-menu {
  border-right: none;
}

.el-header {
  background-color: #fff;
  border-bottom: 1px solid #dcdfe6;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.header-left {
  /* Keep header-left to align logo/title */
}

.header-right {
  /* Remove user info and dropdown */
  display: none;
}

.user-info {
  /* Remove user info and dropdown */
  display: none;
}

.user-info span {
  /* Remove user info and dropdown */
  display: none;
}

.el-main {
  background-color: #f0f2f5;
  padding: 20px;
}
</style> 