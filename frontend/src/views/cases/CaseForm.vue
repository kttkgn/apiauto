<template>
  <div class="case-form">
    <el-form
      ref="formRef"
      :model="formData"
      :rules="rules"
      label-width="100px"
      class="form-container"
    >
      <!-- 基本信息区 -->
      <el-card class="form-card">
        <template #header>
          <div class="card-header">
            <span>基本信息</span>
          </div>
        </template>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="用例名称" prop="name">
              <el-input v-model="formData.name" placeholder="请输入用例名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="所属模块" prop="module">
              <el-select v-model="formData.module" placeholder="请选择所属模块" style="width: 100%">
                <el-option label="用户模块" value="用户模块" />
                <el-option label="订单模块" value="订单模块" />
                <el-option label="商品模块" value="商品模块" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="请求方法" prop="method">
              <el-select v-model="formData.method" placeholder="请选择请求方法" style="width: 100%">
                <el-option label="GET" value="GET" />
                <el-option label="POST" value="POST" />
                <el-option label="PUT" value="PUT" />
                <el-option label="DELETE" value="DELETE" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="请求路径" prop="path">
              <el-input v-model="formData.path" placeholder="请输入请求路径" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-card>

      <!-- 请求配置区 -->
      <el-card class="form-card">
        <template #header>
          <div class="card-header">
            <span>请求配置</span>
          </div>
        </template>
        <el-tabs v-model="activeTab">
          <el-tab-pane label="Headers" name="headers">
            <div class="key-value-table">
              <div v-for="(item, index) in formData.headers" :key="index" class="key-value-row">
                <el-input v-model="item.key" placeholder="Key" class="key-input" />
                <el-input v-model="item.value" placeholder="Value" class="value-input" />
                <el-button type="danger" link @click="removeHeader(index)">
                  <el-icon><Delete /></el-icon>
                </el-button>
              </div>
              <el-button type="primary" link @click="addHeader">
                <el-icon><Plus /></el-icon>添加Header
              </el-button>
            </div>
          </el-tab-pane>
          <el-tab-pane label="Params" name="params">
            <div class="key-value-table">
              <div v-for="(item, index) in formData.params" :key="index" class="key-value-row">
                <el-input v-model="item.key" placeholder="Key" class="key-input" />
                <el-input v-model="item.value" placeholder="Value" class="value-input" />
                <el-button type="danger" link @click="removeParam(index)">
                  <el-icon><Delete /></el-icon>
                </el-button>
              </div>
              <el-button type="primary" link @click="addParam">
                <el-icon><Plus /></el-icon>添加Param
              </el-button>
            </div>
          </el-tab-pane>
          <el-tab-pane label="Body" name="body">
            <el-form-item label="Body类型" prop="bodyType">
              <el-radio-group v-model="formData.bodyType">
                <el-radio label="json">JSON</el-radio>
                <el-radio label="form">Form</el-radio>
              </el-radio-group>
            </el-form-item>
            <div v-if="formData.bodyType === 'json'">
              <el-input
                v-model="formData.body"
                type="textarea"
                :rows="10"
                placeholder="请输入JSON格式的请求体"
              />
            </div>
            <div v-else class="key-value-table">
              <div v-for="(item, index) in formData.formData" :key="index" class="key-value-row">
                <el-input v-model="item.key" placeholder="Key" class="key-input" />
                <el-input v-model="item.value" placeholder="Value" class="value-input" />
                <el-button type="danger" link @click="removeFormData(index)">
                  <el-icon><Delete /></el-icon>
                </el-button>
              </div>
              <el-button type="primary" link @click="addFormData">
                <el-icon><Plus /></el-icon>添加Form数据
              </el-button>
            </div>
          </el-tab-pane>
        </el-tabs>
      </el-card>

      <!-- 断言配置区 -->
      <el-card class="form-card">
        <template #header>
          <div class="card-header">
            <span>断言配置</span>
          </div>
        </template>
        <el-form-item label="状态码断言">
          <el-input v-model="formData.assertions.statusCode" placeholder="请输入预期状态码" />
        </el-form-item>
        <div class="assertion-list">
          <div v-for="(item, index) in formData.assertions.body" :key="index" class="assertion-item">
            <el-input v-model="item.jsonpath" placeholder="JSONPath" class="jsonpath-input" />
            <el-select v-model="item.operator" placeholder="操作符" class="operator-select">
              <el-option label="等于" value="equals" />
              <el-option label="包含" value="contains" />
              <el-option label="大于" value="greater" />
              <el-option label="小于" value="less" />
            </el-select>
            <el-input v-model="item.expected" placeholder="预期值" class="expected-input" />
            <el-button type="danger" link @click="removeAssertion(index)">
              <el-icon><Delete /></el-icon>
            </el-button>
          </div>
          <el-button type="primary" link @click="addAssertion">
            <el-icon><Plus /></el-icon>添加断言
          </el-button>
        </div>
      </el-card>

      <!-- 底部操作栏 -->
      <div class="form-footer">
        <el-button @click="handleCancel">取消</el-button>
        <el-button type="primary" @click="handleSave">保存</el-button>
        <el-button type="success" @click="handleExecute">执行测试</el-button>
      </div>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Plus, Delete } from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'

const route = useRoute()
const router = useRouter()
const formRef = ref<FormInstance>()
const activeTab = ref('headers')

// 表单数据
const formData = reactive({
  name: '',
  module: '',
  method: '',
  path: '',
  headers: [] as { key: string; value: string }[],
  params: [] as { key: string; value: string }[],
  bodyType: 'json',
  body: '',
  formData: [] as { key: string; value: string }[],
  assertions: {
    statusCode: '',
    body: [] as { jsonpath: string; operator: string; expected: string }[]
  }
})

// 表单验证规则
const rules: FormRules = {
  name: [{ required: true, message: '请输入用例名称', trigger: 'blur' }],
  module: [{ required: true, message: '请选择所属模块', trigger: 'change' }],
  method: [{ required: true, message: '请选择请求方法', trigger: 'change' }],
  path: [{ required: true, message: '请输入请求路径', trigger: 'blur' }]
}

// 添加Header
const addHeader = () => {
  formData.headers.push({ key: '', value: '' })
}

// 移除Header
const removeHeader = (index: number) => {
  formData.headers.splice(index, 1)
}

// 添加Param
const addParam = () => {
  formData.params.push({ key: '', value: '' })
}

// 移除Param
const removeParam = (index: number) => {
  formData.params.splice(index, 1)
}

// 添加Form数据
const addFormData = () => {
  formData.formData.push({ key: '', value: '' })
}

// 移除Form数据
const removeFormData = (index: number) => {
  formData.formData.splice(index, 1)
}

// 添加断言
const addAssertion = () => {
  formData.assertions.body.push({ jsonpath: '', operator: '', expected: '' })
}

// 移除断言
const removeAssertion = (index: number) => {
  formData.assertions.body.splice(index, 1)
}

// 取消
const handleCancel = () => {
  router.back()
}

// 保存
const handleSave = async () => {
  if (!formRef.value) return
  await formRef.value.validate((valid) => {
    if (valid) {
      // TODO: 调用保存API
      ElMessage.success('保存成功')
      router.back()
    }
  })
}

// 执行测试
const handleExecute = async () => {
  if (!formRef.value) return
  await formRef.value.validate((valid) => {
    if (valid) {
      // TODO: 调用执行API
      ElMessage.success('开始执行测试')
    }
  })
}

// 获取用例详情
const fetchCaseDetail = (id: string) => {
  // TODO: 调用获取详情API
  // 模拟数据
  Object.assign(formData, {
    name: '测试用例',
    module: '用户模块',
    method: 'POST',
    path: '/api/v1/users',
    headers: [
      { key: 'Content-Type', value: 'application/json' }
    ],
    params: [
      { key: 'page', value: '1' }
    ],
    body: JSON.stringify({ name: 'test' }, null, 2),
    assertions: {
      statusCode: '200',
      body: [
        { jsonpath: '$.code', operator: 'equals', expected: '0' }
      ]
    }
  })
}

// 初始化
onMounted(() => {
  const id = route.params.id
  if (id) {
    fetchCaseDetail(id as string)
  }
})
</script>

<style scoped>
.case-form {
  height: 100%;
  overflow-y: auto;
  padding: 20px;
}

.form-container {
  max-width: 1200px;
  margin: 0 auto;
}

.form-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.key-value-table {
  margin-bottom: 16px;
}

.key-value-row {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
  align-items: center;
}

.key-input {
  width: 200px;
}

.value-input {
  flex: 1;
}

.assertion-list {
  margin-top: 16px;
}

.assertion-item {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
  align-items: center;
}

.jsonpath-input {
  width: 300px;
}

.operator-select {
  width: 120px;
}

.expected-input {
  flex: 1;
}

.form-footer {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  gap: 16px;
}
</style> 