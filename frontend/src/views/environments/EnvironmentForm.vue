<template>
  <div class="environment-form">
    <el-form
      ref="formRef"
      :model="formData"
      :rules="rules"
      label-width="100px"
      class="form-container"
    >
      <!-- 基本信息 -->
      <el-card class="form-card">
        <template #header>
          <div class="card-header">
            <span>基本信息</span>
          </div>
        </template>
        <el-form-item label="环境名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入环境名称" />
        </el-form-item>
        <el-form-item label="基础URL" prop="base_url">
          <el-input v-model="formData.base_url" placeholder="请输入基础URL" />
        </el-form-item>
      </el-card>

      <!-- 公共Headers配置 -->
      <el-card class="form-card">
        <template #header>
          <div class="card-header">
            <span>公共Headers</span>
            <el-button type="primary" link @click="addHeader">
              <el-icon><Plus /></el-icon>添加Header
            </el-button>
          </div>
        </template>
        <div class="key-value-table">
          <div v-for="(item, index) in formData.headers" :key="index" class="key-value-row">
            <el-input v-model="item.key" placeholder="Key" class="key-input" />
            <el-input v-model="item.value" placeholder="Value" class="value-input">
              <template #append>
                <el-tooltip content="支持使用 {{变量名}} 引用变量" placement="top">
                  <el-icon><InfoFilled /></el-icon>
                </el-tooltip>
              </template>
            </el-input>
            <el-button type="danger" link @click="removeHeader(index)">
              <el-icon><Delete /></el-icon>
            </el-button>
          </div>
        </div>
      </el-card>

      <!-- 全局变量配置 -->
      <el-card class="form-card">
        <template #header>
          <div class="card-header">
            <span>全局变量配置</span>
            <el-button type="primary" @click="handleAddVariable">
              添加变量
            </el-button>
          </div>
        </template>
        <el-table :data="formData.variables" style="width: 100%">
          <el-table-column prop="name" label="变量名" min-width="150">
            <template #default="{ row }">
              <el-input v-model="row.name" placeholder="请输入变量名" />
            </template>
          </el-table-column>
          <el-table-column prop="value" label="变量值" min-width="200">
            <template #default="{ row }">
              <el-input v-model="row.value" placeholder="请输入变量值" />
            </template>
          </el-table-column>
          <el-table-column prop="description" label="描述" min-width="200">
            <template #default="{ row }">
              <el-input v-model="row.description" placeholder="请输入描述" />
            </template>
          </el-table-column>
          <el-table-column label="操作" width="250" fixed="right">
            <template #default="{ row, $index }">
              <el-button type="primary" link @click="handleExtractor(row)">
                提取器设置
              </el-button>
              <el-button type="danger" link @click="handleRemoveVariable($index)">
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>

      <!-- 底部操作栏 -->
      <div class="form-footer">
        <el-button @click="handleCancel">取消</el-button>
        <el-button type="primary" @click="handleSubmit">保存</el-button>
      </div>
    </el-form>

    <!-- 变量提取器对话框 -->
    <VariableExtractor
      v-model="showExtractor"
      :variable="currentVariable"
      @save="handleSaveExtractor"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Plus, Delete, InfoFilled } from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'
import VariableExtractor from '../../components/VariableExtractor.vue'

const route = useRoute()
const router = useRouter()
const formRef = ref<FormInstance>()

// 表单数据
const formData = reactive({
  name: '',
  base_url: '',
  headers: [] as { key: string; value: string }[],
  variables: [] as { name: string; value: string; description: string }[],
})

// 表单验证规则
const rules: FormRules = {
  name: [{ required: true, message: '请输入环境名称', trigger: 'blur' }],
  base_url: [{ required: true, message: '请输入基础URL', trigger: 'blur' }]
}

// 提取器相关
const showExtractor = ref(false)
const currentVariable = ref<any>(null)

// 添加Header
const addHeader = () => {
  formData.headers.push({ key: '', value: '' })
}

// 移除Header
const removeHeader = (index: number) => {
  formData.headers.splice(index, 1)
}

// 添加全局变量
const handleAddVariable = () => {
  formData.variables.push({ name: '', value: '', description: '' })
}

// 移除全局变量
const handleRemoveVariable = (index: number) => {
  formData.variables.splice(index, 1)
}

// 添加提取器设置处理函数
const handleExtractor = (row: any) => {
  currentVariable.value = row
  showExtractor.value = true
}

// 保存提取器配置
const handleSaveExtractor = (data: any) => {
  // TODO: 保存提取器配置
  console.log('保存提取器配置:', data)
  ElMessage.success('提取器配置已保存')
}

// 取消
const handleCancel = () => {
  router.back()
}

// 保存
const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate((valid) => {
    if (valid) {
      // TODO: 调用保存API
      ElMessage.success('保存成功')
      router.back()
    }
  })
}

// 获取环境详情
const fetchEnvironmentDetail = (id: string) => {
  // TODO: 调用获取详情API
  // 模拟数据
  Object.assign(formData, {
    name: '开发环境',
    base_url: 'http://dev-api.example.com',
    headers: [
      { key: 'Content-Type', value: 'application/json' },
      { key: 'Authorization', value: 'Bearer {{token}}' }
    ],
    variables: [
      { name: 'token', value: 'xxx', description: '认证令牌' },
      { name: 'version', value: 'v1', description: 'API版本' }
    ]
  })
}

// 初始化
onMounted(() => {
  const id = route.params.id
  if (id) {
    fetchEnvironmentDetail(id as string)
  }
})
</script>

<style scoped>
.environment-form {
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

.form-footer {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  gap: 16px;
}
</style> 