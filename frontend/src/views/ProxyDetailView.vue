<template>
  <!-- Страница просмотра деталей доверенности -->
  <div class="proxy-detail">
    <div class="header">
      <h2>Документ № {{ proxy.number }}</h2>
      <div>
        <button class="btn btn-primary me-2" @click="openEditForm">
          Редактировать
        </button>
        <button v-if="editMode" class="btn btn-success me-2" @click="saveProxy" :disabled="isSaving">
          <span v-if="isSaving" class="spinner-border spinner-border-sm"></span>
          Сохранить
        </button>
        <button style="background-color: orange; border-color: orange;" class="btn btn-info me-2" @click="printProxy">
          Печать
        </button>
        <router-link to="/proxies" class="btn btn-secondary">
          Назад к списку
        </router-link>
      </div>
    </div>

    <!-- Скрытый iframe для печати -->
    <iframe ref="printFrame" style="display: none; width: 0; height: 0; border: 0;"></iframe>

    <!-- Индикатор загрузки -->
    <div v-if="isLoading" class="text-center my-4">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Загрузка...</span>
      </div>
    </div>

    <!-- Сообщение об ошибке -->
    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <!-- Основное содержимое доверенности -->
    <div v-else-if="proxy" class="proxy-content">
      <div class="proxy-info">
        <!-- Информация о доверенности -->
        <div class="info-row">
          <span class="info-label">Номер:</span>
          <span v-if="!editMode" class="info-value">{{ proxy.number }}</span>
          <input v-else v-model="editableProxy.number" type="text" class="form-control">
        </div>
        <div class="info-row">
          <span class="info-label">Дата составления:</span>
          <span v-if="!editMode" class="info-value">{{ formatDate(proxy.date) }}</span>
          <input v-else type="date" class="form-control" v-model="editableProxy.date">
        </div>
        <div class="info-row">
          <span class="info-label">Организация:</span>
          <span v-if="!editMode" class="info-value">{{ organizationName }} (Адрес: {{
            organizationAddress }})</span>
          <select v-else v-model="editableProxy.organization" class="form-select">
            <option v-for="org in organizations" :key="org._id" :value="org._id">
              {{ org.title }}
            </option>
          </select>
        </div>
        <div class="info-row">
          <span class="info-label">Организация-поставщик:</span>
          <span v-if="!editMode" class="info-value">{{ payingOrganizationName }} (
            Адрес: {{ payingOrganizationAddress }})</span>
          <select v-else v-model="editableProxy.supplier_organization" class="form-select">
            <option v-for="org in organizations" :key="org._id" :value="org._id">
              {{ org.title }}
            </option>
          </select>
        </div>
        <div class="info-row">
          <span class="info-label">Физическое лицо:</span>
          <span v-if="!editMode" class="info-value">{{ individualName }}</span>
          <select v-else v-model="editableProxy.individual" class="form-select">
            <option v-for="individual in individuals" :key="individual._id" :value="individual._id">
              {{ individual.lastname }} {{ individual.firstname }} {{ individual.patronymic }}
            </option>
          </select>
        </div>
        <div class="info-row">
          <span class="info-label">Дата начала действия:</span>
          <span v-if="!editMode" class="info-value">{{ formatDate(proxy.period.from) }}</span>
          <input v-else type="date" class="form-control" v-model="periodFrom">
        </div>
        <div class="info-row">
          <span class="info-label">Дата окончания действия:</span>
          <span v-if="!editMode" class="info-value">{{ formatDate(proxy.period.until) }}</span>
          <input v-else type="date" class="form-control" v-model="periodUntil">
        </div>
      </div>

      <!-- Табличная часть с товарами -->
      <div class="proxy-items">
        <h3>Табличная часть</h3>
        <table class="table table-bordered">
          <thead>
            <tr>
              <th>№</th>
              <th>Товар</th>
              <th>Количество</th>
              <th v-if="editMode">Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in currentItems" :key="index">
              <td class="text-center">{{ index + 1 }}</td>
              <td>
                <span v-if="!editMode">{{ getItemName(item.item) }}</span>
                <select v-else v-model="editableProxy.items[index].item" class="form-select">
                  <option v-for="itemOption in items" :key="itemOption._id" :value="itemOption._id">
                    {{ itemOption.title }}
                  </option>
                </select>
              </td>
              <td class="text-center">
                <span v-if="!editMode">{{ item.count }}</span>
                <input v-else v-model.number="editableProxy.items[index].count" type="number" min="0" step="1" class="form-control">
              </td>
              <td v-if="editMode">
                <button class="btn btn-sm btn-danger" @click="removeItem(index)">
                  Удалить
                </button>
              </td>
            </tr>
            <tr v-if="editMode">
              <td :colspan="4">
                <button class="btn btn-sm btn-primary" @click="addItem">
                  Добавить строку
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <ProxyForm 
      :visible="showEditForm" 
      :initial-data="editingProxy" 
      :organizations="organizations" 
      :individuals="individuals" 
      :items="items"
      @submit="handleEditSubmit" 
      @cancel="closeEditForm" 
    />
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import ProxyForm from '@/components/ProxyForm.vue'

export default {
  name: 'ProxyDetailView',
  components: {
    ProxyForm
  },
  props: {
    id: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      isLoading: false,
      isSaving: false,
      error: null,
      editMode: false,
      originalProxy: null,
      editableProxy: {
        number: '',
        date: '',
        organization: null,
        supplier_organization: null,
        individual: null,
        period: {
          from: '',
          until: ''
        },
        items: []
      },
      periodFrom: '',
      periodUntil: '',
      showEditForm: false,
      editingProxy: null
    }
  },
  computed: {
    ...mapGetters([
      'currentProxy',
      'organizations',
      'items',
      'individuals',
      'getOrganizationById',
      'getItemById',
      'getIndividualById'
    ]),
    proxy() {
      return this.currentProxy || {}
    },
    individualName() {
      if (!this.proxy.individual) return 'Не указана'
      const individual = this.getIndividualById(this.proxy.individual)
      return individual ? `${individual.lastname} ${individual.firstname} ${individual.patronymic}` : 'Неизвестное физ.лицо'
    },
    organizationName() {
      if (!this.proxy.organization) return 'Не указана'
      const org = this.getOrganizationById(this.proxy.organization)
      return org ? `${org.title}` : 'Неизвестная организация'
    },
    payingOrganizationName() {
      if (!this.proxy.supplier_organization) return 'Не указана'
      const org = this.getOrganizationById(this.proxy.supplier_organization)
      return org ? `${org.title}` : 'Неизвестная организация'
    },
    organizationAddress() {
      if (!this.proxy.organization) return 'Не указан'
      const org = this.getOrganizationById(this.proxy.organization)
      return org ? `${org.address}` : 'Неизвестный адрес организации'
    },
    payingOrganizationAddress() {
      if (!this.proxy.supplier_organization) return 'Не указан'
      const org = this.getOrganizationById(this.proxy.supplier_organization)
      return org ? `${org.address}` : 'Неизвестный адрес организации'
    },
    currentItems() {
      if (!this.proxy.items) return []
      return this.proxy.items.map(item => ({
        item: item.item?._id || item.item,
        count: item.count
      }))
    }
  },
  methods: {
    ...mapActions([
      'fetchProxyById',
      'fetchOrganizations',
      'fetchItems',
      'updateProxy',
      'fetchIndividuals'
    ]),

    openEditForm() {
      this.editingProxy = JSON.parse(JSON.stringify(this.proxy))
      this.showEditForm = true
    },

    closeEditForm() {
      this.showEditForm = false
      this.editingProxy = null
    },

    async handleEditSubmit(proxyData) {
      try {
        await this.updateProxy(proxyData)
        await this.fetchProxyById(this.id)
        this.closeEditForm()
        this.editMode = false
      } catch (error) {
        console.error('Ошибка сохранения:', error)
        this.error = 'Не удалось сохранить документ'
      }
    },

    // Печать доверенности
    printProxy() {
      const getItemName = (itemId) => {
        if (!itemId) return 'Неизвестный товар';
        const item = this.items.find(i => i._id === itemId) ||
          (typeof itemId === 'object' ? itemId : null);
        return item ? item.title : 'Неизвестный товар';
      };

      const printContent = `
    <!DOCTYPE html>
    <html>
      <head>
        <title>Печать доверенности</title>
        <style>
          @page { size: auto; margin: 0mm; }
          body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
          h1 { text-align: center; margin-bottom: 30px; font-size: 20px; }
          .info-table { width: 100%; margin-bottom: 20px; border-collapse: collapse; }
          .info-table td { padding: 8px; border: 1px solid #ddd; }
          .info-table td:first-child { font-weight: bold; width: 30%; }
          .items-table { width: 100%; border-collapse: collapse; margin-top: 20px; }
          .items-table th, .items-table td { border: 1px solid #ddd; padding: 8px; text-align: left; }
          .items-table th { background-color: #f2f2f2; }
          .text-center { text-align: center; }
          .mt-20 { margin-top: 20px; }
        </style>
      </head>
      <body>
        <h1>Доверенность № ${this.proxy.number}</h1>
        
        <table class="info-table">
           <tr>
            <td>Дата составления:</td>
            <td>${this.formatDate(this.proxy.date)}</td>
           </tr>
           <tr>
            <td>Организация:</td>
            <td>${this.organizationName} (Адрес: ${this.organizationAddress})</td>
           </tr>
           <tr>
            <td>Организация-поставщик:</td>
            <td>${this.payingOrganizationName} (Адрес: ${this.payingOrganizationAddress})</td>
           </tr>
           <tr>
            <td>Физическое лицо:</td>
            <td>${this.individualName}</td>
           </tr>
           <tr>
            <td>Дата начала действия:</td>
            <td>${this.formatDate(this.proxy.period.from)}</td>
           </tr>
           <tr>
            <td>Дата окончания действия:</td>
            <td>${this.formatDate(this.proxy.period.until)}</td>
           </tr>
        </table>

        <h3 class="text-center">Табличная часть</h3>
        <table class="items-table">
          <thead>
             <tr>
              <th>№</th>
              <th>Товар</th>
              <th>Количество</th>
             </tr>
          </thead>
          <tbody>
            ${(this.proxy.items || []).map((item, index) => `
               <tr>
                <td class="text-center">${index + 1}</td>
                <td>${getItemName(item.item)}</td>
                <td class="text-center">${item.count}</td>
               </tr>
            `).join('')}
          </tbody>
        </table>

        <div class="mt-20">
          <p><strong>Подпись ответственного лица:</strong> _________________</p>
        </div>
      </body>
    </html>
  `;

      const printFrame = this.$refs.printFrame;
      printFrame.contentDocument.open();
      printFrame.contentDocument.write(printContent);
      printFrame.contentDocument.close();

      setTimeout(() => {
        printFrame.contentWindow.focus();
        printFrame.contentWindow.print();
      }, 300);
    },

    // Инициализация данных для редактирования
    initEditData() {
      this.originalProxy = JSON.parse(JSON.stringify(this.proxy))
      this.editableProxy = {
        _id: this.proxy._id,
        number: this.proxy.number,
        date: this.formatDateForInput(this.proxy.date),
        organization: this.proxy.organization?._id || this.proxy.organization,
        supplier_organization: this.proxy.supplier_organization?._id || this.proxy.supplier_organization,
        individual: this.proxy.individual?._id || this.proxy.individual,
        period: {
          from: this.formatDateForInput(this.proxy.period?.from),
          until: this.formatDateForInput(this.proxy.period?.until)
        },
        items: this.proxy.items?.map(item => ({
          item: item.item?._id || item.item,
          count: item.count
        })) || []
      }

      this.periodFrom = this.editableProxy.period.from
      this.periodUntil = this.editableProxy.period.until
    },

    // Форматирование даты для input[type="date"]
    formatDateForInput(dateStr) {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      const year = date.getUTCFullYear()
      const month = String(date.getUTCMonth() + 1).padStart(2, '0')
      const day = String(date.getUTCDate()).padStart(2, '0')
      return `${year}-${month}-${day}`
    },

    // Переключение режима редактирования
    toggleEditMode() {
      if (this.editMode) {
        this.editableProxy = JSON.parse(JSON.stringify(this.originalProxy))
      } else {
        this.initEditData()
      }
      this.editMode = !this.editMode
    },

    // Добавление строки с товаром
    addItem() {
      this.editableProxy.items.push({
        item: this.items[0]?._id || null,
        count: 0
      })
    },

    // Удаление строки с товаром
    removeItem(index) {
      this.editableProxy.items.splice(index, 1)
    },

    // Сохранение изменений
    async saveProxy() {
      this.isSaving = true
      this.error = null

      try {
        const dataToSave = {
          _id: this.id,
          number: this.editableProxy.number,
          date: this.editableProxy.date,
          organization: this.editableProxy.organization,
          supplier_organization: this.editableProxy.supplier_organization,
          individual: this.editableProxy.individual,
          period: {
            from: this.periodFrom,
            until: this.periodUntil
          },
          items: this.editableProxy.items.map(item => ({
            item: item.item,
            count: parseInt(item.count)
          }))
        }

        await this.updateProxy(dataToSave)
        await this.fetchProxyById(this.id)
        this.editMode = false
      } catch (error) {
        console.error('Ошибка сохранения:', error)
        this.error = 'Не удалось сохранить документ'
      } finally {
        this.isSaving = false
      }
    },

    // Форматирование даты
    formatDate(dateStr) {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      const day = String(date.getUTCDate()).padStart(2, '0')
      const month = String(date.getUTCMonth() + 1).padStart(2, '0')
      const year = date.getUTCFullYear()
      return `${day}.${month}.${year}`
    },

    // Получение названия товара
    getItemName(itemId) {
      const item = this.getItemById(itemId)
      return item ? item.title : 'Неизвестный товар'
    },

    // Загрузка данных
    async loadData() {
      this.isLoading = true
      this.error = null
      try {
        await this.fetchProxyById(this.id)
        await Promise.all([
          this.fetchOrganizations(),
          this.fetchIndividuals(),
          this.fetchItems()
        ])
        this.initEditData()
      } catch (error) {
        console.error('Ошибка загрузки данных:', error)
        this.error = 'Не удалось загрузить данные документа'
      } finally {
        this.isLoading = false
      }
    }
  },
  created() {
    this.loadData()
  }
}
</script>

<style scoped>
.date-inputs {
  display: flex;
  gap: 10px;
}

.date-inputs .form-control {
  flex: 1;
}

.proxy-detail {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.proxy-content {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.proxy-info {
  margin-bottom: 30px;
}

.info-row {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.info-label {
  font-weight: 500;
  width: 150px;
  color: #666;
}

.info-value {
  flex: 1;
}

.form-control,
.form-select {
  max-width: 400px;
}

.table {
  margin-top: 20px;
}

.alert {
  margin-top: 20px;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}

.spinner-border-sm {
  margin-right: 5px;
}

.text-center {
  text-align: center;
}
</style>