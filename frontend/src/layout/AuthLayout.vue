<template>
    <el-menu class="el-menu-demo" mode="horizontal" style="margin-bottom: 25px">
        <el-menu-item index="1" @click="goHome">Strona główna</el-menu-item>
        <el-sub-menu index="2">
            <template #title>Dodaj</template>
            <el-menu-item index="2-1" @click="goExpense">Wydatek</el-menu-item>
            <el-menu-item index="2-2" @click="goIncome">Przychód</el-menu-item>
            <el-menu-item index="2-3">Rachunek</el-menu-item>
            <el-menu-item index="2-3">Lista zakupów</el-menu-item>

        </el-sub-menu>
        <el-sub-menu index="3">
            <template #title>{{ this.fullName }}</template>
            <el-menu-item index="3-1">Profil</el-menu-item>
            <el-menu-item index="3-2" @click="handleLogout">Wyloguj</el-menu-item>

        </el-sub-menu>

    </el-menu>
</template>
<script>
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
    name: 'AuthLayout',
    data() {
        return {
            fullName: ''

        }
    },
    created() {
        this.checkAuthenticated()
    },
    methods: {
        goHome() {
            this.$router.push('/main')
        },
        goIncome() {
            this.$router.push('/income')
        },
        goExpense() {
            this.$router.push('/expense')
        },
        checkAuthenticated() {
            const token = localStorage.getItem('token')
            if (!token) {
                ElMessage.error('Zaloguj się, aby uzyskać dostęp do tej strony')
                this.$router.push('/')
                return
            }
            const headers = {
                'Authorization': `Token ${token}`,
                'Content-Type': 'application/json' // Możesz dostosować typ zawartości w zależności od potrzeb
            }
            axios.get(`${API_URL}/api/userdata/`, { headers })
                .then((response) => {
                    //                    const username = response.data.username
                    const name = response.data.name
                    const surname = response.data.surname
                    //                    const email = response.data.email
                    this.fullName = name + " " + surname

                })
                .catch(error => {
                    // Obsłuż błąd żądania
                    console.error('Błąd podczas sprawdzania statusu logowania:', error)
                    ElMessage.error('Zaloguj się, aby uzyskać dostęp do tej strony')
                    this.$router.push('/')
                    return

                })

        },
        handleLogout() {
            const token = localStorage.getItem('token')
            const logoutUrl = `${API_URL}/api/logout/`

            const headers = {
                'Authorization': `Token ${token}`,
                'Content-Type': 'application/json'
            }
            axios.post(logoutUrl, null, { headers })
                .then((response) => {
                    ElMessage.info(response.data.message)

                    localStorage.removeItem('token')
                    this.$router.push('/')
                })
                .catch(error => {
                    // Obsługa błędu
                    console.error('Błąd podczas wylogowywania:', error)
                })

        }
    }
}
</script>