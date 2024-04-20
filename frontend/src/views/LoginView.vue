<template>
    <div id="login">
        <div style="margin-top: 10px; margin-bottom: 10px">
            <el-alert title="Aplikacja w trybie rozwoju, prace trwają" type="warning" effect="dark"/>

        </div>

        <el-form :model="form" label-width="auto" style="max-width: 700px;">
            <el-form-item label="Użytkownik">
                <el-input v-model="form.username" clearable placeholder="Wpisz nazwę użytkownika" />
            </el-form-item>
            <el-form-item label="Hasło">
                <el-input v-model="form.password" clearable placeholder="Wpisz hasło" show-password type="password" />
            </el-form-item>
            <el-button type="primary" @click="handleLogin">Zaloguj</el-button>

        </el-form>

    </div>
</template>

<script>
import axios from 'axios'
var API_URL = ""
if (window.location.hostname == 'localhost') {
    API_URL = "http://127.0.0.1:8000"
} 
if(window.location.hostname == 'finanse.xce.pl') {
    API_URL = "http://finanse.xce.pl"
}
export default {
    name: 'LoginView',
    data() {
        return {
            form: {
                username: '',
                password: '',

            }
        }
    },
    methods: {
        handleLogin() {
            const data = {
                'username': this.form.username,
                'password': this.form.password
            }
            axios.post(`${API_URL}/api/login/`, data)
                .then((response) => {
                    const token = response.data.token;
                    localStorage.setItem('token', token)
                    this.$router.push('/main')

                })

        }
    }
}
</script>