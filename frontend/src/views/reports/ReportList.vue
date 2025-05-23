<template>
  <div class="report-list">
    <!-- 顶部操作栏 -->
    <div class="operation-bar">
      <div class="left">
        <el-input
          v-model="searchQuery"
          placeholder="请输入报告名称"
          clearable
          @keyup.enter="handleSearch"
          class="search-input"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-select v-model="dateRange" placeholder="时间范围" @change="handleSearch">
          <el-option label="全部" value="" />
          <el-option label="今天" value="today" />
          <el-option label="本周" value="week" />
          <el-option label="本月" value="month" />
        </el-select>
      </div>
      <div class="right">
        <el-button type="primary" @click="handleRefresh">
          <el-icon><Refresh /></el-icon>刷新
        </el-button>
      </div>
    </div>

    <!-- 报告列表 -->
    <el-table
      v-loading="loading"
      :data="reportList"
      style="width: 100%"
    >
      <el-table-column prop="name" label="报告名称" min-width="200">
        <template #default="{ row }">
          <el-tooltip :content="row.name" placement="top" :show-after="500">
            <span class="ellipsis">{{ row.name }}</span>
          </el-tooltip>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="执行时间" width="180">
        <template #default="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column prop="total_cases" label="用例总数" width="100" />
      <el-table-column prop="pass_rate" label="通过率" width="120">
        <template #default="{ row }">
          <el-progress 
            :percentage="row.pass_rate" 
            :status="getPassRateStatus(row.pass_rate)"
          />
        </template>
      </el-table-column>
      <el-table-column label="操作" width="220" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" link @click="handleView(row)">
            查看
          </el-button>
          <el-button type="primary" link @click="handleDownload(row)">
            下载
          </el-button>
          <el-button type="danger" link @click="handleDelete(row)">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <div class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Refresh } from '@element-plus/icons-vue'

const router = useRouter()
const loading = ref(false)

// 搜索和筛选
const searchQuery = ref('')
const dateRange = ref('')

// 分页
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 报告列表（模拟数据）
const reportList = ref([
  {
    id: 1,
    name: '用户模块测试报告',
    created_at: '2024-03-20 10:00:00',
    total_cases: 10,
    pass_rate: 90
  },
  {
    id: 2,
    name: '订单模块测试报告',
    created_at: '2024-03-20 11:00:00',
    total_cases: 15,
    pass_rate: 80
  },
  {
    id: 3,
    name: '支付模块测试报告',
    created_at: '2024-03-20 12:00:00',
    total_cases: 8,
    pass_rate: 100
  }
])

// 获取通过率状态
const getPassRateStatus = (rate: number) => {
  if (rate >= 90) return 'success'
  if (rate >= 60) return 'warning'
  return 'exception'
}

// 格式化日期
const formatDate = (date: string) => {
  return date
}

// 搜索
const handleSearch = () => {
  // TODO: 调用搜索API
  console.log('搜索:', searchQuery.value, dateRange.value)
}

// 刷新
const handleRefresh = () => {
  // TODO: 调用刷新API
  console.log('刷新')
}

// 下载报告
const handleDownload = (row: any) => {
  // TODO: 调用下载API
  ElMessage.success('开始下载报告')
}

// 删除报告
const handleDelete = (row: any) => {
  ElMessageBox.confirm(
    '确定要删除该报告吗？',
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    // TODO: 调用删除API
    ElMessage.success('删除成功')
  }).catch(() => {})
}

// 查看报告
const handleView = (row: any) => {
  router.push(`/reports/${row.id}`)
}

// 分页大小改变
const handleSizeChange = (val: number) => {
  pageSize.value = val
  // TODO: 重新加载数据
}

// 页码改变
const handleCurrentChange = (val: number) => {
  currentPage.value = val
  // TODO: 重新加载数据
}

// 初始化
onMounted(() => {
  // TODO: 加载初始数据
})
</script>

<style scoped>
.report-list {
  height: 100%;
  padding: 20px;
  display: flex;
  flex-direction: column;
}

.operation-bar {
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.left {
  display: flex;
  gap: 16px;
}

.search-input {
  width: 300px;
}

.right {
  display: flex;
  gap: 16px;
}

.ellipsis {
  display: inline-block;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style> 