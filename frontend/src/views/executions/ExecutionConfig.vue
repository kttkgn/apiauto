<template>
  <div class="execution-config">
    <el-card class="config-card">
      <template #header>
        <div class="card-header">
          <span>{{ isEdit ? '编辑执行' : '新增执行' }}</span>
        </div>
      </template>

      <el-form
        ref="formRef"
        :model="formData"
        :rules="rules"
        label-width="100px"
      >
        <!-- 基本信息 -->
        <el-form-item label="用例名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入用例名称" />
        </el-form-item>

        <!-- 执行范围 -->
        <el-form-item label="执行范围" prop="scope">
          <el-select v-model="formData.scope" placeholder="请选择执行范围" @change="handleScopeChange">
            <el-option label="单个用例" value="single" />
            <el-option label="模块用例" value="module" />
            <el-option label="全部用例" value="all" />
          </el-select>
        </el-form-item>

        <!-- 用例选择（单个用例时显示） -->
        <el-form-item v-if="formData.scope === 'single'" label="选择用例" prop="case_id">
          <el-select v-model="formData.case_id" placeholder="请选择用例">
            <el-option
              v-for="item in caseList"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>

        <!-- 模块选择（模块用例时显示） -->
        <el-form-item v-if="formData.scope === 'module'" label="选择模块" prop="module_id">
          <el-select v-model="formData.module_id" placeholder="请选择模块">
            <el-option
              v-for="item in moduleList"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>

        <!-- 环境选择 -->
        <el-form-item label="环境" prop="environment">
          <el-select v-model="formData.environment" placeholder="请选择环境">
            <el-option
              v-for="env in environments"
              :key="env.id"
              :label="env.name"
              :value="env.id"
            />
          </el-select>
        </el-form-item>

        <!-- 执行参数 -->
        <el-form-item label="执行参数" prop="parameters">
          <el-input
            v-model="formData.parameters"
            type="textarea"
            :rows="4"
            placeholder="请输入执行参数（JSON格式）"
          />
          <div class="form-tip">支持使用 {{变量名}} 引用环境变量</div>
        </el-form-item>

        <!-- 底部按钮 -->
        <div class="form-footer">
          <el-button @click="handleCancel">取消</el-button>
          <el-button type="primary" @click="handleSubmit">开始执行</el-button>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'

const route = useRoute()
const router = useRouter()
const formRef = ref<FormInstance>()

// 是否为编辑模式
const isEdit = ref(false)

// 表单数据
const formData = reactive({
  name: '',
  scope: '',
  case_id: '',
  module_id: '',
  environment: '',
  parameters: ''
})

// 表单验证规则
const rules: FormRules = {
  name: [{ required: true, message: '请输入用例名称', trigger: 'blur' }],
  scope: [{ required: true, message: '请选择执行范围', trigger: 'change' }],
  case_id: [{ required: true, message: '请选择用例', trigger: 'change' }],
  module_id: [{ required: true, message: '请选择模块', trigger: 'change' }],
  environment: [{ required: true, message: '请选择环境', trigger: 'change' }]
}

// 环境列表（模拟数据）
const environments = ref([
  { id: 1, name: '开发环境' },
  { id: 2, name: '测试环境' },
  { id: 3, name: '生产环境' }
])

// 用例列表（模拟数据）
const caseList = ref([
  { id: 1, name: '用户登录接口测试' },
  { id: 2, name: '订单创建接口测试' }
])

// 模块列表（模拟数据）
const moduleList = ref([
  { id: 1, name: '用户模块' },
  { id: 2, name: '订单模块' }
])

// 执行范围改变
const handleScopeChange = (value: string) => {
  // 清空相关字段
  formData.case_id = ''
  formData.module_id = ''
}

// 取消
const handleCancel = () => {
  router.back()
}

// 提交
const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate((valid) => {
    if (valid) {
      // TODO: 调用执行API
      ElMessage.success('执行成功')
      router.push('/executions')
    }
  })
}

// 获取执行详情
const fetchExecutionDetail = (id: string) => {
  // TODO: 调用获取详情API
  // 模拟数据
  Object.assign(formData, {
    name: '用户登录接口测试',
    scope: 'single',
    case_id: 1,
    environment: 1,
    parameters: JSON.stringify({ userId: 123, token: 'xxx' }, null, 2)
  })
}

// 初始化
onMounted(() => {
  const id = route.query.id
  if (id) {
    isEdit.value = true
    fetchExecutionDetail(id as string)
  }
})
</script>

<style scoped>
.execution-config {
  height: 100%;
  padding: 20px;
}

.config-card {
  max-width: 800px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.form-footer {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  gap: 16px;
}
</style> 