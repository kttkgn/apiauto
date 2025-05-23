<template>
  <el-container class="layout-container">
    <el-aside width="200px">
      <el-menu
        router
        :default-active="$route.path"
        class="el-menu-vertical"
      >
        <el-menu-item index="/">
          <el-icon><HomeFilled /></el-icon>
          <span>首页</span>
        </el-menu-item>
        <el-menu-item index="/environments">
          <el-icon><Setting /></el-icon>
          <span>环境配置</span>
        </el-menu-item>
        <el-menu-item index="/modules">
          <el-icon><Files /></el-icon>
          <span>模块管理</span>
        </el-menu-item>
        <el-menu-item index="/cases">
          <el-icon><Document /></el-icon>
          <span>用例管理</span>
        </el-menu-item>
        <el-menu-item index="/executions">
          <el-icon><VideoPlay /></el-icon>
          <span>执行管理</span>
        </el-menu-item>
        <el-menu-item index="/reports">
          <el-icon><DataLine /></el-icon>
          <span>测试报告</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container class="main-container">
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import {
  HomeFilled,
  Document,
  Setting,
  VideoPlay,
  DataLine,
  Files
} from '@element-plus/icons-vue'
</script>

<style scoped>
.layout-container {
  height: 100vh;
  margin: 0;
  padding: 0;
  width: 100vw;
  overflow: hidden;
}

.el-aside {
  background-color: #304156;
  color: #fff;
  margin: 0;
  padding: 0;
  height: 100vh;
}

.el-menu {
  border-right: none;
  margin: 0;
  padding: 0;
}

.el-menu-vertical {
  height: 100%;
  background-color: #304156;
}

.el-menu-item {
  color: #bfcbd9;
}

.el-menu-item:hover {
  color: #fff;
}

.el-menu-item.is-active {
  color: #409eff;
}

.main-container {
  flex: 1;
  height: 100vh;
  overflow: hidden;
}

.el-main {
  background-color: #f0f2f5;
  padding: 20px;
  margin: 0;
  height: 100vh;
  overflow-y: auto;
  box-sizing: border-box;
}

:deep(.el-container) {
  margin: 0;
  padding: 0;
}

:deep(.el-main) {
  margin: 0;
  padding: 20px;
}
</style> 