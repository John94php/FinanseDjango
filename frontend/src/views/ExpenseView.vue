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
            <div>
                <input type="file" @change="handleFileUpload">
                <button @click="uploadFile">Upload</button>
            </div>
            <el-button type="primary" @click="handleSubmitExpense">Zapisz</el-button>

        </el-form>

    </div>
</template>

<script>
import AuthLayout from '@/layout/AuthLayout.vue';
import axios from 'axios'
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
        AuthLayout
    },
    data() {
        return {
            form: {
                name: '',
                amount: '',
                file: null
            }

        }
    },
    methods: {
        handleFileUpload(event) {
            this.file = event.target.files[0];
        },
        async uploadFile() {
            if (!this.file) {
                return;
            }
            try {
                const formData = new FormData()
                const token = localStorage.getItem('token');
                const url = `${API_URL}/api/upload_file`

                formData.append('file', this.file);
                const response = await axios.post(url, formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                        'Authorization': `Token ${token}`,

                    }
                });

                console.log(response.data);
            } catch (error) {
                console.error('Błąd:', error);
            }
        },
        handleSubmitExpense() {

        }

    }
}
</script>