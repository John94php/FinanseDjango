<template>
  <div class="home">
    <AuthLayout />
    <div class="stats-container">
      <div class="stat">
        <el-statistic title="Wydatki" :value="expenseValue" />
        zł
      </div>
      <div class="stat">
        <el-statistic title="Przychody" :value="incomeValue" />
        zł
      </div>
      <div class="stat" >
        <el-statistic title="Bilans" :value="balanceValue" />
        zł
      </div>
    </div>
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
      balanceValue: 0

    }
  },
  created() {
    this.getIncomeValue()
  },
  methods: {
    getIncomeValue() {
      const token = localStorage.getItem('token');
      const headers = {
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json'
      };

      axios.get(`${API_URL}/api/statistics/`, { headers })
        .then((response) => {
          const incomes = response.data.incomes
          const expenses = response.data.expenses
          const balance = response.data.balance
          this.incomeValue = incomes
          this.expenseValue = expenses
          this.balanceValue = balance
        })
        .catch(error => {
          console.error('Błąd:', error);
        });

    }
  }
}
</script>
<style scoped>
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