<template>
  <div class="modal-mask" v-if="visible" @click.self="$emit('cancel')">
    <div class="modal-wrapper">
      <div class="modal-container">
        <div class="modal-header">
          <h3>{{ editing ? 'Редактирование' : 'Добавление' }} заявки на ремонт</h3>
          <button class="modal-close" @click="handleCancel">&times;</button>
        </div>

        <div class="modal-body">
          <form @submit.prevent="handleSubmit">
            <div class="form-group">
              <label>Номер документа</label>
              <input type="text" class="form-control" v-model="localForm.number" required>
            </div>

            <div class="form-group">
              <label>Дата составления</label>
              <input type="date" class="form-control" v-model="localForm.date" required>
            </div>

            <div class="form-group">
              <label>Заказчик (физическое лицо)</label>
              <select class="form-select" v-model="localForm.customer" required @change="handleCustomerSelect">
                <option value="" disabled>Выберите заказчика</option>
                <option value="new" class="text-primary fw-bold">+ Добавить новое физическое лицо</option>
                <option v-for="individual in individuals" :key="individual._id" :value="individual._id">
                  {{ individual.lastname }} {{ individual.firstname }} {{ individual.patronymic }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label>Подрядчик (физическое лицо)</label>
              <select class="form-select" v-model="localForm.contractor" required @change="handleContractorSelect">
                <option value="" disabled>Выберите подрядчика</option>
                <option value="new" class="text-primary fw-bold">+ Добавить новое физическое лицо</option>
                <option v-for="individual in individuals" :key="individual._id" :value="individual._id">
                  {{ individual.lastname }} {{ individual.firstname }} {{ individual.patronymic }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <h4>Табличная часть</h4>
              <div class="table-responsive">
                <table class="table table-bordered">
                  <thead>
                    <tr>
                      <th style="min-width: 60px;">№</th>
                      <th style="min-width: 200px;">Товар</th>
                      <th style="min-width: 150px;">Дата приобретения</th>
                      <th style="min-width: 150px;">Дата ввода в эксплуатацию</th>
                      <th style="min-width: 150px;">Фактический срок эксплуатации (лет)</th>
                      <th style="min-width: 200px;">Характер повреждений</th>
                      <th style="min-width: 250px;">Обстоятельства повреждения</th>
                      <th style="min-width: 80px;">Действия</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(item, index) in localForm.items" :key="index">
                      <td>
                        <input type="number" class="form-control" v-model.number="item.number" min="1" required>
                      </td>
                      <td>
                        <select class="form-select" v-model="item.item" required @change="handleItemSelect(index)">
                          <option value="" disabled>Выберите товар</option>
                          <option value="new" class="text-primary fw-bold">+ Добавить новый товар</option>
                          <option v-for="itemOption in items" :key="itemOption._id" :value="itemOption._id">
                            {{ itemOption.title }}
                          </option>
                        </select>
                      </td>
                      <td>
                        <input type="date" class="form-control" v-model="item.purchase_date" required>
                      </td>
                      <td>
                        <input type="date" class="form-control" v-model="item.commissioning_date" required>
                      </td>
                      <td>
                        <input type="number" class="form-control" v-model.number="item.actual_service_life" step="0.1" min="0" required>
                      </td>
                      <td>
                        <select class="form-select" v-model="item.damage" required @change="handleDamageSelect(index)">
                          <option value="" disabled>Выберите повреждение</option>
                          <option value="new" class="text-primary fw-bold">+ Добавить новое повреждение</option>
                          <option v-for="damage in damages" :key="damage._id" :value="damage._id">
                            {{ damage.title }}
                          </option>
                        </select>
                      </td>
                      <td>
                        <input type="text" class="form-control" v-model="item.damage_circumstances" required>
                      </td>
                      <td>
                        <button type="button" class="btn btn-sm btn-danger" @click="removeItem(index)">
                          Удалить
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <button type="button" class="btn btn-sm btn-primary mt-2" @click="addItem">
                Добавить строку
              </button>
            </div>

            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="handleCancel" :disabled="isSubmitting">
                Отмена
              </button>
              <button type="submit" class="btn btn-primary" :disabled="isSubmitting || !formValid">
                {{ isSubmitting ? 'Сохранение...' : editing ? 'Обновить' : 'Сохранить' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>

  <IndividualForm :visible="showCustomerQuickForm" :positions="positions" @submit="handleNewCustomer" @cancel="showCustomerQuickForm = false" />
  <IndividualForm :visible="showContractorQuickForm" :positions="positions" @submit="handleNewContractor" @cancel="showContractorQuickForm = false" />
  <ItemForm :visible="showItemQuickForm" @submit="handleNewItem" @cancel="showItemQuickForm = false" />
  <DamageForm :visible="showDamageQuickForm" @submit="handleNewDamage" @cancel="showDamageQuickForm = false" />
</template>

<script>
import IndividualForm from '@/components/IndividualForm.vue'
import ItemForm from '@/components/ItemForm.vue'
import DamageForm from '@/components/DamageForm.vue'
import { mapGetters, mapActions } from 'vuex'

export default {
  emits: ['submit', 'cancel'],
  components: {
    IndividualForm,
    ItemForm,
    DamageForm
  },
  props: {
    visible: Boolean,
    initialData: Object,
    individuals: Array,
    items: Array,
    damages: Array
  },
  data() {
    return {
      localForm: this.getInitialForm(),
      isSubmitting: false,
      showCustomerQuickForm: false,
      showContractorQuickForm: false,
      showItemQuickForm: false,
      itemToUpdateIndex: null,
      showDamageQuickForm: false,
      damageToUpdateIndex: null,
      originalForm: null
    }
  },
  computed: {
    ...mapGetters(['positions']),
    editing() {
      return this.initialData !== null
    },
    formValid() {
      const baseValid = this.localForm.number &&
        this.localForm.date &&
        this.localForm.customer &&
        this.localForm.contractor

      const itemsValid = (this.localForm.items || []).every(item =>
        item.number &&
        item.item &&
        item.purchase_date &&
        item.commissioning_date &&
        item.actual_service_life !== undefined &&
        item.damage &&
        item.damage_circumstances
      )

      return baseValid && itemsValid
    }
  },
  watch: {
    initialData: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.localForm = {
            _id: newVal._id,
            number: newVal.number,
            date: this.formatDateForInput(newVal.date),
            customer: newVal.customer?._id || newVal.customer,
            contractor: newVal.contractor?._id || newVal.contractor,
            items: (newVal.items || []).map(item => ({
              number: item.number,
              item: item.item?._id || item.item,
              purchase_date: this.formatDateForInput(item.purchase_date),
              commissioning_date: this.formatDateForInput(item.commissioning_date),
              actual_service_life: item.actual_service_life,
              damage: item.damage?._id || item.damage,
              damage_circumstances: item.damage_circumstances
            }))
          }
          this.originalForm = JSON.parse(JSON.stringify(this.localForm))
        } else {
          this.resetForm()
        }
      }
    }
  },
  methods: {
    getInitialForm() {
      return {
        number: '',
        date: '',
        customer: null,
        contractor: null,
        items: []
      }
    },
    formatDateForInput(dateStr) {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      const year = date.getUTCFullYear()
      const month = String(date.getUTCMonth() + 1).padStart(2, '0')
      const day = String(date.getUTCDate()).padStart(2, '0')
      return `${year}-${month}-${day}`
    },
    handleSubmit() {
      if (this.isSubmitting || !this.formValid) return

      const formData = {
        number: this.localForm.number,
        date: this.localForm.date,
        customer: this.localForm.customer,
        contractor: this.localForm.contractor,
        items: this.localForm.items.map(item => ({
          number: parseInt(item.number),
          item: item.item,
          purchase_date: item.purchase_date,
          commissioning_date: item.commissioning_date,
          actual_service_life: parseFloat(item.actual_service_life),
          damage: item.damage,
          damage_circumstances: item.damage_circumstances.trim()
        }))
      }

      if (this.editing && this.localForm._id) {
        formData._id = this.localForm._id
      }

      this.isSubmitting = true

      try {
        this.$emit('submit', formData)
      } catch (error) {
        console.error('Ошибка отправки формы:', error)
      } finally {
        this.isSubmitting = false
      }
    },
    handleCancel() {
      if (this.editing && this.originalForm) {
        this.localForm = JSON.parse(JSON.stringify(this.originalForm))
      } else {
        this.resetForm()
      }
      this.$emit('cancel')
    },
    addItem() {
      this.localForm.items.push({
        number: this.localForm.items.length + 1,
        item: null,
        purchase_date: '',
        commissioning_date: '',
        actual_service_life: null,
        damage: null,
        damage_circumstances: ''
      })
    },
    removeItem(index) {
      this.localForm.items.splice(index, 1)
      this.localForm.items.forEach((item, idx) => {
        item.number = idx + 1
      })
    },
    resetForm() {
      this.localForm = this.getInitialForm()
      this.originalForm = null
    },
    handleCustomerSelect(event) {
      if (event.target.value === 'new') {
        this.$store.dispatch('fetchPositions').then(() => {
          this.showCustomerQuickForm = true
          this.localForm.customer = null
        })
      }
    },
    handleContractorSelect(event) {
      if (event.target.value === 'new') {
        this.$store.dispatch('fetchPositions').then(() => {
          this.showContractorQuickForm = true
          this.localForm.contractor = null
        })
      }
    },
    handleItemSelect(index) {
      if (this.localForm.items[index].item === 'new') {
        this.itemToUpdateIndex = index
        this.showItemQuickForm = true
        this.localForm.items[index].item = null
      }
    },
    handleDamageSelect(index) {
      if (this.localForm.items[index].damage === 'new') {
        this.damageToUpdateIndex = index
        this.showDamageQuickForm = true
        this.localForm.items[index].damage = null
      }
    },
    async handleNewCustomer(newIndividual) {
      try {
        const individualData = {
          lastname: newIndividual.lastname,
          firstname: newIndividual.firstname,
          patronymic: newIndividual.patronymic,
          position: newIndividual.position_id
        }

        await this.$store.dispatch('addIndividual', individualData)
        await this.$store.dispatch('fetchIndividuals')

        const individuals = this.$store.getters.individuals
        const newIndividualId = individuals[individuals.length - 1]._id
        this.localForm.customer = newIndividualId

        this.showCustomerQuickForm = false
      } catch (error) {
        console.error('Error creating customer:', error)
        this.showCustomerQuickForm = false
      }
    },
    async handleNewContractor(newIndividual) {
      try {
        const individualData = {
          lastname: newIndividual.lastname,
          firstname: newIndividual.firstname,
          patronymic: newIndividual.patronymic,
          position: newIndividual.position_id
        }

        await this.$store.dispatch('addIndividual', individualData)
        await this.$store.dispatch('fetchIndividuals')

        const individuals = this.$store.getters.individuals
        const newIndividualId = individuals[individuals.length - 1]._id
        this.localForm.contractor = newIndividualId

        this.showContractorQuickForm = false
      } catch (error) {
        console.error('Error creating contractor:', error)
        this.showContractorQuickForm = false
      }
    },
    // Обработка добавления нового повреждения
    async handleNewDamage(newDamage) {
      if (this.damageToUpdateIndex === null) return

      try {
        const currentDamageId = this.localForm.items[this.damageToUpdateIndex].damage
        this.localForm.items[this.damageToUpdateIndex].damage = null

        await this.$store.dispatch('addDamage', newDamage)
        await this.$store.dispatch('fetchDamages')

        const damages = this.$store.getters.damages
        const newDamageId = damages[damages.length - 1]._id
        this.localForm.items[this.damageToUpdateIndex].damage = newDamageId

        this.showDamageQuickForm = false
        this.damageToUpdateIndex = null
      } catch (error) {
        console.error('Ошибка создания товара:', error)
        if (this.damageToUpdateIndex !== null) {
          this.localForm.items[this.damageToUpdateIndex].damage = currentDamageId
        }
        this.showDamageQuickForm = false
      }
    },
    async handleNewItem(newItem) {
      if (this.itemToUpdateIndex === null) return

      try {
        const currentItemId = this.localForm.items[this.itemToUpdateIndex].item
        this.localForm.items[this.itemToUpdateIndex].item = null

        await this.$store.dispatch('addItem', newItem)
        await this.$store.dispatch('fetchItems')

        const items = this.$store.getters.items
        const newItemId = items[items.length - 1]._id
        this.localForm.items[this.itemToUpdateIndex].item = newItemId

        this.showItemQuickForm = false
        this.itemToUpdateIndex = null
      } catch (error) {
        console.error('Ошибка создания товара:', error)
        if (this.itemToUpdateIndex !== null) {
          this.localForm.items[this.itemToUpdateIndex].item = currentItemId
        }
        this.showItemQuickForm = false
      }
    }
  }
}
</script>

<style scoped>
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-wrapper {
  width: 100%;
  max-width: 1400px;
  padding: 20px;
}

.modal-container {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
}

.modal-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
}

.modal-body {
  padding: 20px;
}

.modal-footer {
  padding: 15px 20px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
}

.form-control,
.form-select {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.table-responsive {
  overflow-x: auto;
}

.table {
  width: 100%;
  margin-bottom: 1rem;
  border-collapse: collapse;
  min-width: 1100px;
}

.table th,
.table td {
  padding: 0.75rem;
  vertical-align: top;
  border: 1px solid #dee2e6;
}

.table thead th {
  background-color: #f8f9fa;
  font-weight: 600;
}

.table th:first-child,
.table td:first-child {
  min-width: 80px;
  width: 80px;
}

.modal-wrapper {
  max-width: 1600px;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}

.text-danger {
  color: #dc3545;
}

option.text-primary {
  color: #0d6efd;
  font-weight: bold;
}
</style>