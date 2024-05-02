<template>
    <div id="income" style="text-align: center">
        <AuthLayout />
        <el-form :model="form" label-width="auto" style="max-width: 800px;">
            <el-form-item label="Nazwa">
                <el-input v-model="form.name" />
            </el-form-item>
            <el-form-item label="Kwota">
                <el-input v-model="form.amount" type="text" placeholder="Wpisz liczbę"></el-input>

            </el-form-item>
            <el-button type="primary" @click="handleSubmitIncome">Create</el-button>

        </el-form>
        <h2>Przychody</h2>
        <div>
            <el-table v-if="isDesktop" :data="data">
                <el-table-column v-for="column in columnsDesktop" :key="column.key" :label="column.title"
                    :prop="column.key"></el-table-column>
                <el-table-column label="Akcje">
                    <template v-slot="scope">
                        <el-button type="primary" @click="editRow(scope.row)">Edytuj</el-button>
                        <el-button type="danger" @click="deleteRow(scope.row)">Usuń</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <div v-else>
                <el-card v-for="(item, index) in filteredData" :key="index">
                    <div class="card-item" v-for="(value, key) in item" :key="key">
                        <b>{{ keyMap[key] }}</b> <el-badge :value="value" class="item"></el-badge>
                       
                        <el-divider />

                    </div>
                    <el-card>
                        <el-button type="primary" @click="editRow(item)">Edytuj</el-button>
                        <el-button type="danger" @click="deleteRow(item)">Usuń</el-button>

                    </el-card>

                </el-card>
            </div>
        </div>
    </div>
    <el-dialog title="Edytuj wiersz" v-model="editDialogVisible" :before-close="handleCloseDialog">
        <!-- Formularz edycji -->
        <el-form :model="editedRow">
            <el-form-item label="Nazwa">
                <el-input v-model="editedRow.name"></el-input>
            </el-form-item>
            <el-form-item label="Kwota">
                <el-input v-model="editedRow.amount"></el-input>
            </el-form-item>
        </el-form>

        <div class="dialog-footer">
            <el-button @click="editDialogVisible = false">Anuluj</el-button>
            <el-button type="primary" @click="saveChanges">Zapisz</el-button>
        </div>
    </el-dialog>

</template>

<script>
import AuthLayout from '@/layout/AuthLayout.vue';
import { ElMessage } from 'element-plus'

import axios from 'axios';
var API_URL = ""
if (window.location.hostname == 'localhost') {
    API_URL = "http://127.0.0.1:8000"
}
if (window.location.hostname == 'finanse.xce.pl') {
    API_URL = "http://finanse.xce.pl"
}
export default {
    name: 'IncomeView',
    components: {
        AuthLayout
    },
    data() {
        return {
            form: {
                name: '',
                amount: ''
            },
            isDesktop: true,
            editedRow: {},

            columnsDesktop: [
                { key: 'name', title: 'Nazwa' },
                { key: 'amount', title: 'Kwota' },
                { key: 'income_date', title: 'Data' }

            ],
            keyMap: {
                'id': 'No.',
                'name': 'Nazwa',
                'amount': 'Kwota',
                'income_date': 'Data'
            },
            data: [],
            editDialogVisible: false
        };
    },
    created() {
        this.checkScreenWidth();
        window.addEventListener('resize', this.checkScreenWidth);

        this.getIncomeData();

    },
    beforeUnmount() {
        window.removeEventListener('resize', this.checkScreenWidth);
    },
    computed: {
        filteredData() {
            return this.data.map(item => {
                const filteredItem = {};
                for (const key in item) {
                    if (key !== 'user_id') {
                        filteredItem[key] = item[key];
                    }
                }
                return filteredItem;
            });
        }
    }
    ,
    methods: {
        handleCloseDialog(done) {
            done()
        },
        saveChanges() {
            console.log('Zapisano zmiany:', this.editedRow);
            this.editDialogVisible = false; 
        },
        editRow(row) {
            this.editDialogVisible = true
            this.editedRow = { ...row }; 


        },
        deleteRow(row) {
            console.log('Usuń wiersz:', row);
        },
        checkScreenWidth() {
            this.isDesktop = window.innerWidth >= 768;
        },
        getIncomeData() {
            const token = localStorage.getItem('token');
            const headers = {
                'Authorization': `Token ${token}`,
                'Content-Type': 'application/json'
            };

            axios.get(`${API_URL}/api/income/`, { headers })
                .then((response) => {
                    this.data = response.data.data;

                })
                .catch(error => {
                    console.error('Błąd:', error);
                });
        },
        handleSubmitIncome() {
            const token = localStorage.getItem('token');
            const headers = {
                'Authorization': `Token ${token}`,
                'Content-Type': 'application/json'
            };

            const data = {
                'name': this.form.name,
                'amount': this.form.amount
            };
            if (this.form.name !== '' && this.form.amount !== '') {
                axios.post(`${API_URL}/api/add_income/`, data, { headers })
                    .then((response) => {
                        console.log(response.data);
                        ElMessage.success('Dodano nowy przychód')
                        this.form.name = ''
                        this.form.amount = ''

                        this.getIncomeData();
                    })
                    .catch(error => {
                        console.error('Błąd:', error);
                        // Obsłuż błąd - wyświetl komunikat użytkownikowi lub podejmij odpowiednie działania
                    });

            } else {
                ElMessage.error('Formularz nie może być pusty')
            }
        }
    },
    watch: {
        'form.amount': function (newValue) {
            let cleanedValue = newValue.replace(/[^0-9.,]/g, '');

            cleanedValue = cleanedValue.replace(/,/g, '.');

            if (cleanedValue.includes('.')) {
                const parts = cleanedValue.split('.');
                if (parts.length === 2) {
                    cleanedValue = `${parts[0]}.${parts[1].slice(0, 2)}`;
                }
            }

            this.form.amount = cleanedValue;
        }
    }
};
</script>
<style scoped>
.card-item {
    margin-bottom: 10px;
}
</style>