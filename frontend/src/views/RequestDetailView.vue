<template>
  <div class="repair-request-detail">
    <div class="header">
      <h2>Заявка на ремонт оборудования № {{ request.number }}</h2>
      <div>
        <button class="btn btn-primary me-2" @click="openEditForm">
          Редактировать
        </button>
        <button style="background-color: orange; border-color: orange;" class="btn btn-info me-2" @click="printRequest">
          Печать
        </button>
        <router-link to="/repair_requests" class="btn btn-secondary">
          Назад к списку
        </router-link>
      </div>
    </div>

    <iframe ref="printFrame" style="display: none; width: 0; height: 0; border: 0;"></iframe>

    <div v-if="isLoading" class="text-center my-4">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Загрузка...</span>
      </div>
    </div>

    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-else-if="request" class="request-content">
      <div class="request-info">
        <div class="info-row">
          <span class="info-label">Номер:</span>
          <span v-if="!editMode" class="info-value">{{ request.number }}</span>
          <input v-else v-model="editableRequest.number" type="text" class="form-control">
        </div>
        <div class="info-row">
          <span class="info-label">Дата составления:</span>
          <span v-if="!editMode" class="info-value">{{ formatDate(request.date) }}</span>
          <input v-else type="date" class="form-control" v-model="editableRequest.date">
        </div>
        <div class="info-row">
          <span class="info-label">Заказчик:</span>
          <span v-if="!editMode" class="info-value">{{ customerName }}</span>
          <select v-else v-model="editableRequest.customer" class="form-select">
            <option v-for="individual in individuals" :key="individual._id" :value="individual._id">
              {{ individual.lastname }} {{ individual.firstname }} {{ individual.patronymic }}
            </option>
          </select>
        </div>
        <div class="info-row">
          <span class="info-label">Подрядчик:</span>
          <span v-if="!editMode" class="info-value">{{ contractorName }}</span>
          <select v-else v-model="editableRequest.contractor" class="form-select">
            <option v-for="individual in individuals" :key="individual._id" :value="individual._id">
              {{ individual.lastname }} {{ individual.firstname }} {{ individual.patronymic }}
            </option>
          </select>
        </div>
      </div>

      <div class="request-items">
        <h3>Табличная часть</h3>
        <table class="table table-bordered">
          <thead>
            <tr>
              <th>№</th>
              <th>Товар</th>
              <th>Дата приобретения</th>
              <th>Дата ввода в эксплуатацию</th>
              <th>Фактический срок эксплуатации (лет)</th>
              <th>Характер повреждений</th>
              <th>Обстоятельства повреждения</th>
              <th v-if="editMode">Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in currentItems" :key="index">
              <td class="text-center">{{ item.number }}</td>
              <td>
                <span v-if="!editMode">{{ getItemName(item.item) }}</span>
                <select v-else v-model="editableRequest.items[index].item" class="form-select">
                  <option v-for="itemOption in items" :key="itemOption._id" :value="itemOption._id">
                    {{ itemOption.title }}
                  </option>
                </select>
              </td>
              <td class="text-center">
                <span v-if="!editMode">{{ formatDate(item.purchase_date) }}</span>
                <input v-else type="date" class="form-control" v-model="editableRequest.items[index].purchase_date">
              </td>
              <td class="text-center">
                <span v-if="!editMode">{{ formatDate(item.commissioning_date) }}</span>
                <input v-else type="date" class="form-control" v-model="editableRequest.items[index].commissioning_date">
              </td>
              <td class="text-center">
                <span v-if="!editMode">{{ item.actual_service_life }}</span>
                <input v-else v-model.number="editableRequest.items[index].actual_service_life" type="number" step="0.1" min="0" class="form-control">
              </td>
              <td>
                <span v-if="!editMode">{{ getDamageName(item.damage) }}</span>
                <select v-else v-model="editableRequest.items[index].damage" class="form-select">
                  <option v-for="damage in damages" :key="damage._id" :value="damage._id">
                    {{ damage.title }}
                  </option>
                </select>
              </td>
              <td>
                <span v-if="!editMode">{{ item.damage_circumstances }}</span>
                <input v-else v-model="editableRequest.items[index].damage_circumstances" type="text" class="form-control">
              </td>
              <td v-if="editMode">
                <button class="btn btn-sm btn-danger" @click="removeItem(index)">
                  Удалить
                </button>
              </td>
            </tr>
            <tr v-if="editMode">
              <td :colspan="8">
                <button class="btn btn-sm btn-primary" @click="addItem">
                  Добавить строку
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <RepairRequestForm 
      :visible="showEditForm" 
      :initial-data="editingRequest" 
      :individuals="individuals" 
      :items="items" 
      :damages="damages"
      @submit="handleEditSubmit" 
      @cancel="closeEditForm" 
    />
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import RepairRequestForm from '@/components/RepairRequestForm.vue'

export default {
  name: 'RepairRequestDetailView',
  components: {
    RepairRequestForm
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
      originalRequest: null,
      editableRequest: {
        number: '',
        date: '',
        customer: null,
        contractor: null,
        items: []
      },
      showEditForm: false,
      editingRequest: null
    }
  },
  computed: {
    ...mapGetters([
      'currentRequest',
      'individuals',
      'items',
      'damages',
      'getIndividualById',
      'getItemById',
      'getDamageById'
    ]),
    request() {
      return this.currentRequest || {}
    },
    customerName() {
      if (!this.request.customer) return 'Не указан'
      if (typeof this.request.customer === 'object' && this.request.customer.lastname) {
        return `${this.request.customer.lastname} ${this.request.customer.firstname} ${this.request.customer.patronymic || ''}`.trim()
      }
      const individual = this.getIndividualById(this.request.customer)
      return individual ? `${individual.lastname} ${individual.firstname} ${individual.patronymic || ''}`.trim() : 'Неизвестно'
    },
    contractorName() {
      if (!this.request.contractor) return 'Не указан'
      if (typeof this.request.contractor === 'object' && this.request.contractor.lastname) {
        return `${this.request.contractor.lastname} ${this.request.contractor.firstname} ${this.request.contractor.patronymic || ''}`.trim()
      }
      const individual = this.getIndividualById(this.request.contractor)
      return individual ? `${individual.lastname} ${individual.firstname} ${individual.patronymic || ''}`.trim() : 'Неизвестно'
    },
    currentItems() {
      if (!this.request.items) return []
      return this.request.items.map(item => ({
        number: item.number,
        item: item.item?._id || item.item,
        purchase_date: item.purchase_date,
        commissioning_date: item.commissioning_date,
        actual_service_life: item.actual_service_life,
        damage: item.damage?._id || item.damage,
        damage_circumstances: item.damage_circumstances
      }))
    }
  },
  methods: {
    ...mapActions([
      'fetchRequestById',
      'fetchIndividuals',
      'fetchItems',
      'fetchDamages',
      'updateRequest'
    ]),

    openEditForm() {
      this.editingRequest = JSON.parse(JSON.stringify(this.request))
      this.showEditForm = true
    },

    closeEditForm() {
      this.showEditForm = false
      this.editingRequest = null
    },

    async handleEditSubmit(requestData) {
      try {
        await this.updateRequest(requestData)
        await this.fetchRequestById(this.id)
        this.closeEditForm()
        this.editMode = false
      } catch (error) {
        console.error('Ошибка сохранения:', error)
        this.error = 'Не удалось сохранить заявку'
      }
    },

    initEditData() {
      this.originalRequest = JSON.parse(JSON.stringify(this.request))
      this.editableRequest = {
        _id: this.request._id,
        number: this.request.number,
        date: this.formatDateForInput(this.request.date),
        customer: this.request.customer?._id || this.request.customer,
        contractor: this.request.contractor?._id || this.request.contractor,
        items: this.request.items?.map(item => ({
          number: item.number,
          item: item.item?._id || item.item,
          purchase_date: this.formatDateForInput(item.purchase_date),
          commissioning_date: this.formatDateForInput(item.commissioning_date),
          actual_service_life: item.actual_service_life,
          damage: item.damage?._id || item.damage,
          damage_circumstances: item.damage_circumstances
        })) || []
      }
    },

    toggleEditMode() {
      if (this.editMode) {
        this.editableRequest = JSON.parse(JSON.stringify(this.originalRequest))
      } else {
        this.initEditData()
      }
      this.editMode = !this.editMode
    },

    addItem() {
      const newNumber = (this.editableRequest.items.length + 1).toString()
      this.editableRequest.items.push({
        number: newNumber,
        item: this.items[0]?._id || null,
        purchase_date: '',
        commissioning_date: '',
        actual_service_life: null,
        damage: this.damages[0]?._id || null,
        damage_circumstances: ''
      })
    },

    removeItem(index) {
      this.editableRequest.items.splice(index, 1)
      this.editableRequest.items.forEach((item, idx) => {
        item.number = (idx + 1).toString()
      })
    },

    async saveRequest() {
      this.isSaving = true
      this.error = null

      try {
        const dataToSave = {
          _id: this.id,
          number: this.editableRequest.number,
          date: this.editableRequest.date,
          customer: this.editableRequest.customer,
          contractor: this.editableRequest.contractor,
          items: this.editableRequest.items.map(item => ({
            number: parseInt(item.number),
            item: item.item,
            purchase_date: item.purchase_date,
            commissioning_date: item.commissioning_date,
            actual_service_life: parseFloat(item.actual_service_life),
            damage: item.damage,
            damage_circumstances: item.damage_circumstances
          }))
        }

        await this.updateRequest(dataToSave)
        await this.fetchRequestById(this.id)
        this.editMode = false
      } catch (error) {
        console.error('Ошибка сохранения:', error)
        this.error = 'Не удалось сохранить заявку'
      } finally {
        this.isSaving = false
      }
    },

    printRequest() {
      const getItemName = (itemId) => {
        if (!itemId) return 'Неизвестный товар'
        if (typeof itemId === 'object' && itemId.title) return itemId.title
        const item = this.items.find(i => i._id === itemId)
        return item ? item.title : 'Неизвестный товар'
      }

      const getDamageName = (damageId) => {
        if (!damageId) return 'Не указано'
        if (typeof damageId === 'object' && damageId.title) return damageId.title
        const damage = this.damages.find(d => d._id === damageId)
        return damage ? damage.title : 'Неизвестно'
      }

      const printContent = `
        <!DOCTYPE html>
        <html>
          <head>
            <title>Печать заявки на ремонт оборудования</title>
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
              .items-table th:nth-child(2), .items-table td:nth-child(2) { width: 200px; }
              .mt-20 { margin-top: 20px; }
              .info-block {
                margin-top: 30px;
              }
              .info-row {
                margin-bottom: 25px;
                display: flex;
                font-size: 14px;
              }
              .info-label {
                font-weight: bold;
                width: 180px;
                font-size: 14px;
              }
              .info-value {
                flex: 1;
                padding-left: 20px;
                align-items: baseline;     
                border-bottom: 1px solid #000;
                padding-bottom: 8px;
                max-width: 50vw;
              }
            </style>
          </head>
          <body>
            <h1>Заявка на ремонт оборудования № ${this.request.number}</h1>
            <div class="info-block">
               <div class="info-row"><span class="info-label">Дата составления:</span><span class="info-value">${this.formatDate(this.request.date)}</span></div>
               <div class="info-row"><span class="info-label">Заказчик:</span><span class="info-value">${this.customerName}</span></div>
               <div class="info-row"><span class="info-label">Подрядчик:</span><span class="info-value">${this.contractorName}</span></div>

            </div>
            <table class="items-table">
              <thead>
                  <tr><th>№</th><th>Товар</th><th>Дата приобретения</th><th>Дата ввода в эксплуатацию</th><th>Срок эксплуатации (лет)</th><th>Характер повреждений</th><th>Обстоятельства повреждения</th></tr>
              </thead>
              <tbody>
                ${(this.request.items || []).map((item) => `
                  <tr>
                    <td class="text-center">${item.number}</td>
                    <td>${getItemName(item.item)}</td>
                    <td class="text-center">${this.formatDate(item.purchase_date)}</td>
                    <td class="text-center">${this.formatDate(item.commissioning_date)}</td>
                    <td class="text-center">${item.actual_service_life}</td>
                    <td>${getDamageName(item.damage)}</td>
                    <td>${item.damage_circumstances || ''}</td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
            <div class="mt-20">
              <p><strong>Подпись заказчика:</strong>   __________________(__________________)</p>
            </div>
          </body>
        </html>
      `

      const printFrame = this.$refs.printFrame
      printFrame.contentDocument.open()
      printFrame.contentDocument.write(printContent)
      printFrame.contentDocument.close()

      setTimeout(() => {
        printFrame.contentWindow.focus()
        printFrame.contentWindow.print()
      }, 300)
    },

    formatDate(dateStr) {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      const day = String(date.getUTCDate()).padStart(2, '0')
      const month = String(date.getUTCMonth() + 1).padStart(2, '0')
      const year = date.getUTCFullYear()
      return `${day}.${month}.${year}`
    },

    formatDateForInput(dateStr) {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      const year = date.getUTCFullYear()
      const month = String(date.getUTCMonth() + 1).padStart(2, '0')
      const day = String(date.getUTCDate()).padStart(2, '0')
      return `${year}-${month}-${day}`
    },

    getItemName(itemId) {
      const item = this.getItemById(itemId)
      return item ? item.title : 'Неизвестный товар'
    },

    getDamageName(damageId) {
      const damage = this.getDamageById(damageId)
      return damage ? damage.title : 'Неизвестно'
    },

    async loadData() {
      this.isLoading = true
      this.error = null
      try {
        await this.fetchRequestById(this.id)
        await Promise.all([
          this.fetchIndividuals(),
          this.fetchItems(),
          this.fetchDamages()
        ])
      } catch (error) {
        console.error('Ошибка загрузки данных:', error)
        this.error = 'Не удалось загрузить данные заявки'
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
.repair-request-detail {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.request-content {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.request-info {
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

.table th {
  background-color: #f8f9fa;
}

.table th:nth-child(2),
.table td:nth-child(2) {
  min-width: 250px;
  max-width: 300px;
  word-wrap: break-word;
  white-space: normal;
}

.table th:first-child,
.table td:first-child {
  min-width: 60px;
  width: 60px;
}

.table td {
  vertical-align: top;
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