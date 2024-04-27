<template>
    <div id="expense">
        <AuthLayout />
        <form :model="form" label-width="auto" style="max-width: 800px;" enctype="multipart/form-data">
            <el-form-item label="Nazwa">
                <el-input v-model="form.name" required />
            </el-form-item>
            <el-form-item label="Kwota">
                <el-input v-model="form.amount" type="text" @input="formatAmount" placeholder="Wpisz liczbę"
                    required></el-input>

            </el-form-item>
            <el-form-item label="Zdjęcie">
                <input type="file" @change="handleFileUpload" name="file" />

            </el-form-item>
            <el-form-item label="Data wydatku">
                <el-date-picker v-model="form.pickedDate" type="datetime" placeholder="Select date and time"
                    :default-time="defaultTime" required />

            </el-form-item>

            <el-button type="primary" @click="handleSubmitExpense">Create</el-button>

        </form>



    </div>
</template>

<script>
import AuthLayout from '@/layout/AuthLayout.vue';
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { ElLoading } from 'element-plus'
import moment from 'moment'
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
                file: [],
                pickedDate: '',
            },
            defaultTime: new Date(2000, 1, 1, 12, 0, 0),

        }
    },
    methods: {
        formatAmount() {
            this.form.amount = this.form.amount.replace(/[^0-9.]/g, "");
        },
        disabledDate(time) {
            const today = new Date().setHours(0, 0, 0, 0);
            return time.getTime() > today;
        },
        handleFileUpload(e) {
            this.form.file = e.target.files[0]
        },
        startLoading() {
            this.loadingInstance = ElLoading.service({
                lock: true,
                text: 'Ładowanie danych...',
                background: 'rgba(0, 0, 0, 0.7)'
            });
        },
        endLoading() {
            if (this.loadingInstance) {
                this.loadingInstance.close();
            }
        },
        handleSubmitExpense() {
            const token = localStorage.getItem('token')
            const headers = {
                'Authorization': `Token ${token}`,
                'Content-Type': 'multipart/form-data'

            };
            const url = `${API_URL}/api/add_expense/`;
            moment.locale('pl')
            const formattedPickedDate = moment(this.form.pickedDate).format('YYYY-MM-DD HH:mm:ss')

            const data2 = new FormData();
            data2.append('name', this.form.name)
            data2.append('amount', this.form.amount)
            data2.append('file', this.form.file)
            data2.append('date', formattedPickedDate)
            this.startLoading()

            axios.post(url, data2, { headers })
                .then((response) => {
                    ElMessage.success('Wydatek został zapisany')
                    this.endLoading()
                    
                    console.log(response.data)

                })
                .catch(error => {
                    console.error('Błąd:', error);
                    ElMessage.warning(error)

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