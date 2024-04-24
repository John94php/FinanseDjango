<template>
    <div id="expense">
        <AuthLayout />
        <el-form :model="form" label-width="auto" style="max-width: 800px;">
            <el-form-item label="Nazwa">
                <el-input v-model="form.name" />
            </el-form-item>
            <el-form-item label="Kwota">
                <el-input v-model="form.amount" type="text" placeholder="Wpisz liczbę"></el-input>

            </el-form-item>
            <el-form-item label="Zdjęcie">
                <el-input v-model="form.file" type="file"></el-input>

            </el-form-item>

            <el-button type="primary" @click="handleSubmitExpense">Create</el-button>

        </el-form>



    </div>
</template>

<script>
import AuthLayout from '@/layout/AuthLayout.vue';
import axios from 'axios'
import { ElMessage } from 'element-plus'

var API_URL = ""
if (window.location.hostname == 'localhost') {
    API_URL = "http://127.0.0.1:8000"
}
if (window.location.hostname == 'finanse.xce.pl') {
    API_URL = "http://finanse.xce.pl"
}
export default {
    name: 'ExpenseView',
    components: {
        AuthLayout,

    },
    data() {
        return {
            form: {
                name: '',
                amount: '',
            },

        }
    },
    methods: {

        handleSubmitExpense() {
            const token = localStorage.getItem('token')
            const headers = {
                'Authorization': `Token ${token}`,

            };
            const url = `${API_URL}/api/add_expense/`;
            const data = new FormData();
            data.append('name', this.form.name);
            data.append('amount', this.form.amount);
            data.append('file', this.form.file);
            console.log(this.form.file)
            axios.post(url, data, { headers })
                .then((response) => {
                    ElMessage.success('Wydatek został zapisany')
                    console.log(response.data.data)

                })
                .catch(error => {
                    console.error('Błąd:', error);
                });


        }

    }
}
</script>
<style scoped>
.form-container {
    display: flex;
    justify-content: center;
}

.form-card {
    width: 300px;
    margin-bottom: 20px;
}
</style>