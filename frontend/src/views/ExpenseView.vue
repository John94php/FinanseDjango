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
        <h2>Wydatki</h2>
        <div>
            <el-table v-if="isDesktop" :data="data">
                <el-table-column v-for="column in columnsDesktop" :key="column.key" :label="column.title"
                    :prop="column.key">
                    <template v-slot="{ row }">
                        <template v-if="column.key !== 'expense_file'">
                            {{ row[column.key] }}
                        </template>
                        <template v-else>
                            <el-table-column title="Zdjęcie">
                                <template v-slot="{ row }">
                                    <template v-if="row.expense_file">
                                        <img :src="getImageUrl(row.expense_file)"
                                            @click="showImagePreview(row.expense_file)"
                                            style="max-width: 100px; max-height: 100px; cursor: pointer;" />

                                    </template>

                                    <template v-else>
                                        <span>Nie ma zdjęcia</span>
                                    </template>
                                </template>
                            </el-table-column>
                        </template>
                    </template>
                </el-table-column>
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
    <el-dialog v-model="imagePreviewVisible" @close="imagePreviewVisible = false">
        <img :src="selectedImage" style="width: 100%;" />
    </el-dialog>

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
import axios from 'axios';
import { ElMessage } from 'element-plus';
import { ElLoading } from 'element-plus';
import moment from 'moment';

const djangoApiUrl = process.env.VUE_APP_DJANGO_API_URL;
const mediaUrl = `${djangoApiUrl}`;

var API_URL = "";
if (window.location.hostname == 'localhost') {
    API_URL = "http://127.0.0.1:8000";
}
if (window.location.hostname == 'finanse.xce.pl') {
    API_URL = "http://finanse.xce.pl";
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
            isDesktop: true,
            editedRow: {},
            columnsDesktop: [
                { key: 'name', title: 'Nazwa' },
                { key: 'amount', title: 'Kwota' },
                { key: 'expense_date', title: 'Data' },
                { key: 'expense_file', title: 'Zdjęcie' },
            ],
            keyMap: {
                'id': 'No.',
                'name': 'Nazwa',
                'amount': 'Kwota',
                'expense_date': 'Data',
                'expense_file': 'Zdjęcie',
            },
            data: [],
            editDialogVisible: false,
            dialogImageVisible: false,
            selectedImage: null,
            imagePreviewVisible: false,
            isPreviewVisible: false
        };
    },
    created() {
        this.checkScreenWidth();
        window.addEventListener('resize', this.checkScreenWidth);
        this.getExpenseData();
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
        },
    },
    methods: {
        showImagePreview(filename) {
            this.selectedImage = `${mediaUrl}/${filename}`;
            this.imagePreviewVisible = true;
        },
        getImageUrl(filename) {
            this.selectedImage = `${mediaUrl}/${filename}`;
            return `${mediaUrl}/${filename}`;
        },
        getExpenseData() {
            const token = localStorage.getItem('token');
            const headers = {
                'Authorization': `Token ${token}`,
                'Content-Type': 'application/json',
            };
            axios.get(`${API_URL}/api/expenses`, { headers })
                .then((response) => {
                    this.data = response.data.data;
                })
                .catch(error => {
                    console.error('Błąd:', error);
                });
        },
        handleCloseDialog(done) {
            done();
        },
        saveChanges() {
            console.log('Zapisano zmiany:', this.editedRow);
            this.editDialogVisible = false;
        },
        editRow(row) {
            this.editDialogVisible = true;
            this.editedRow = { ...row };
        },
        deleteRow(row) {
            console.log('Usuń wiersz:', row);
        },
        checkScreenWidth() {
            this.isDesktop = window.innerWidth >= 768;
        },
        formatAmount() {
            this.form.amount = this.form.amount.replace(/[^0-9.]/g, "");
        },
        disabledDate(time) {
            const today = new Date().setHours(0, 0, 0, 0);
            return time.getTime() > today;
        },
        handleFileUpload(e) {
            this.form.file = e.target.files[0];
        },
        startLoading() {
            this.loadingInstance = ElLoading.service({
                lock: true,
                text: 'Ładowanie danych...',
                background: 'rgba(0, 0, 0, 0.7)',
            });
        },
        endLoading() {
            if (this.loadingInstance) {
                this.loadingInstance.close();
            }
        },
        handleSubmitExpense() {
            const token = localStorage.getItem('token');
            const headers = {
                'Authorization': `Token ${token}`,
                'Content-Type': 'multipart/form-data',
            };
            const url = `${API_URL}/api/add_expense/`;
            moment.locale('pl');
            const formattedPickedDate = moment(this.form.pickedDate).format('YYYY-MM-DD HH:mm:ss');
            const data2 = new FormData();
            data2.append('name', this.form.name);
            data2.append('amount', this.form.amount);
            data2.append('file', this.form.file);
            data2.append('date', formattedPickedDate);
            this.startLoading();
            axios.post(url, data2, { headers })
                .then((response) => {
                    ElMessage.success('Wydatek został zapisany');
                    this.endLoading();
                    console.log(response.data);
                })
                .catch(error => {
                    console.error('Błąd:', error);
                    ElMessage.warning(error);
                });
        },
    },
};
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