<template>
  <div class="home">
    <AuthLayout />
    <div class="stats-container">
      <div class="stat">
        Wydatki&nbsp;<el-tag type="danger">{{ expenseValue }} zł</el-tag>

      </div>
      <div class="stat">
        Przychody&nbsp;<el-tag type="success">{{ incomeValue }} zł</el-tag>

      </div>
      <div class="stat">
        Budżet&nbsp;<el-tag type="info">{{ balanceValue }} zł</el-tag>

      </div>
    </div>
  </div>

  <div class="monthly-report">
    <el-row :gutter="20">
      <el-col :xs="24" :sm="12" :md="8" :lg="6" v-for="(data, month) in monthlyReport" :key="month">
        <el-card>
          <p>{{ data.name }}</p>
        </el-card>
        <el-descriptions :bordered="true"  size="small">
          <el-descriptions-item label="Przychody">{{ data.incomes }} zł</el-descriptions-item>
          <el-descriptions-item label="Wydatki">{{ data.expenses }} zł</el-descriptions-item>
          <el-descriptions-item label="Bilans">{{ data.balance }} zł</el-descriptions-item>
        </el-descriptions>
      </el-col>
    </el-row>
  </div>
</template>

<script>

import AuthLayout from '@/layout/AuthLayout.vue'
import axios from 'axios';
var API_URL = ""
if (window.location.hostname == 'localhost') {
  API_URL = "http://127.0.0.1:8000"
}
if (window.location.hostname == 'finanse.xce.pl') {
  API_URL = "http://finanse.xce.pl"
}


export default {
  name: 'HomeView',
  components: {
    AuthLayout,
  },
  data() {
    return {
      expenseValue: 0,
      incomeValue: 0,
      balanceValue: 0,
      monthlyReport: {}


    }
  },
  created() {
    this.getStatisticValue()
  },
  methods: {
    async getStatisticValue() {
      try {
        const token = localStorage.getItem('token');
        const headers = {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json'
        };

        const response = await axios.get(`${API_URL}/api/statistics/`, { headers });
        const incomes = response.data.incomes;
        const expenses = response.data.expenses;
        const balance = response.data.balance;
        

        this.incomeValue = incomes;
        this.expenseValue = expenses;
        this.balanceValue = balance;
        this.monthlyReport = response.data.report
      } catch (error) {
        console.error('Błąd:', error);
        return [];
      }
    }
  }
}
</script>
<style scoped>
.monthly-report {
  padding: 20px;
}
.home {
  margin-top: 5px
}

.stats-container {
  display: flex;
  flex-wrap: wrap;
}

.stat {
  flex-basis: calc(33.33% - 20px);
  margin-right: 20px;
  margin-bottom: 20px;
}

@media screen and (max-width: 768px) {
  .stat {
    flex-basis: calc(100% - 20px);
    margin-right: 0;
  }
}
</style>