<template>
  <div class="home-container">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card class="welcome-card">
          <template #header>
            <div class="card-header">
              <h2>欢迎使用接口自动化平台</h2>
            </div>
          </template>
          <div class="card-content">
            <p>一个轻量、高效、可扩展的接口自动化测试平台</p>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="quick-actions">
      <el-col :span="6">
        <el-card class="action-card" @click="navigateTo('/cases')">
          <el-icon class="action-icon"><Document /></el-icon>
          <h3>用例管理</h3>
          <p>创建和管理接口测试用例</p>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="action-card" @click="navigateTo('/environments')">
          <el-icon class="action-icon"><Setting /></el-icon>
          <h3>环境配置</h3>
          <p>配置和管理测试环境</p>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="action-card" @click="navigateTo('/executions')">
          <el-icon class="action-icon"><VideoPlay /></el-icon>
          <h3>执行管理</h3>
          <p>执行测试用例并查看结果</p>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="action-card" @click="navigateTo('/reports')">
          <el-icon class="action-icon"><DataLine /></el-icon>
          <h3>测试报告</h3>
          <p>查看历史测试报告</p>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="statistics">
      <el-col :span="8">
        <el-card class="stat-card">
          <template #header>
            <div class="stat-header">
              <span>用例统计</span>
            </div>
          </template>
          <div class="stat-content">
            <div class="stat-item">
              <span class="stat-label">总用例数</span>
              <span class="stat-value">0</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">今日新增</span>
              <span class="stat-value">0</span>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card">
          <template #header>
            <div class="stat-header">
              <span>执行统计</span>
            </div>
          </template>
          <div class="stat-content">
            <div class="stat-item">
              <span class="stat-label">总执行次数</span>
              <span class="stat-value">0</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">今日执行</span>
              <span class="stat-value">0</span>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card">
          <template #header>
            <div class="stat-header">
              <span>成功率</span>
            </div>
          </template>
          <div class="stat-content">
            <div class="stat-item">
              <span class="stat-label">总成功率</span>
              <span class="stat-value">0%</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">今日成功率</span>
              <span class="stat-value">0%</span>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import {
  Document,
  Setting,
  VideoPlay,
  DataLine
} from '@element-plus/icons-vue'

const router = useRouter()

const navigateTo = (path: string) => {
  router.push(path)
}
</script>

<style scoped>
.home-container {
  padding: 20px;
}

.welcome-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-content {
  text-align: center;
  padding: 20px 0;
}

.quick-actions {
  margin-bottom: 20px;
}

.action-card {
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
}

.action-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 2px 12px 0 rgba(0,0,0,.1);
}

.action-icon {
  font-size: 48px;
  color: #409EFF;
  margin-bottom: 10px;
}

.action-card h3 {
  margin: 10px 0;
  color: #303133;
}

.action-card p {
  color: #909399;
  font-size: 14px;
}

.statistics {
  margin-bottom: 20px;
}

.stat-card {
  height: 100%;
}

.stat-header {
  font-weight: bold;
}

.stat-content {
  padding: 10px 0;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.stat-label {
  color: #606266;
}

.stat-value {
  font-size: 20px;
  font-weight: bold;
  color: #409EFF;
}
</style> 