<template>
  <!-- Модальное окно для добавления/редактирования доверенности -->
  <div class="modal-mask" v-if="visible" @click.self="$emit('cancel')">
    <div class="modal-wrapper">
      <div class="modal-container">
        <div class="modal-header">
          <h3>{{ editing ? 'Редактирование' : 'Добавление' }} доверенности</h3>
          <button class="modal-close" @click="handleCancel">&times;</button>
        </div>

        <div class="modal-body">
          <form @submit.prevent="handleSubmit">
            <!-- Основные поля доверенности -->
            <div class="form-group">
              <label>Номер документа</label>
              <input type="text" class="form-control" v-model="localForm.number" required>
            </div>

            <div class="form-group">
              <label>Дата составления</label>
              <input type="date" class="form-control" v-model="localForm.date" required>
            </div>

            <!-- Выбор организации с возможностью добавления новой -->
            <div class="form-group">
              <label>Организация</label>
              <select class="form-select" v-model="localForm.organization" required @change="handleOrganizationSelect">
                <option value="" disabled>Выберите организацию</option>
                <option value="new" class="text-primary fw-bold">+ Добавить новую организацию</option>
                <option v-for="org in organizations" :key="org._id" :value="org._id">
                  {{ org.title }} (Адрес: {{ org.address }})
                </option>
              </select>
            </div>

            <!-- Выбор организации-поставщика -->
            <div class="form-group">
              <label>Организация-поставщик</label>
              <select class="form-select" v-model="localForm.supplier_organization" required
                @change="handlePayingOrganizationSelect">
                <option value="" disabled>Выберите организацию-поставщика</option>
                <option value="new" class="text-primary fw-bold">+ Добавить новую организацию</option>
                <option v-for="org in organizations" :key="org._id" :value="org._id">
                  {{ org.title }} (Адрес: {{ org.address }})
                </option>
              </select>
            </div>

            <!-- Выбор физического лица -->
            <div class="form-group">
              <label>Физическое лицо</label>
              <select class="form-select" v-model="localForm.individual" required @change="handleIndividualSelect">
                <option value="" disabled>Выберите физическое лицо</option>
                <option value="new" class="text-primary fw-bold">+ Добавить новое физическое лицо</option>
                <option v-for="individual in individuals" :key="individual._id" :value="individual._id">
                  {{ individual.lastname }} {{ individual.firstname }} {{ individual.patronymic }}
                </option>
              </select>
            </div>

            <!-- Период действия доверенности -->
            <div class="form-group">
              <label>Дата начала действия</label>
              <input type="date" class="form-control" v-model="periodFrom" required>
            </div>

            <div class="form-group">
              <label>Дата окончания действия</label>
              <input type="date" class="form-control" v-model="periodUntil" required>
            </div>

            <!-- Табличная часть с товарами -->
            <div class="form-group">
              <h4>Табличная часть</h4>
              <div class="table-responsive">
                <table class="table table-bordered">
                  <thead>
                    <tr>
                      <th>Товар</th>
                      <th>Количество</th>
                      <th>Действия</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(item, index) in localForm.items" :key="index">
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
                        <input type="number" class="form-control" v-model.number="item.count" min="0" step="1" required>
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
              <button type="button" class="btn btn-sm btn-primary mt-2" @click="addItem" :disabled="!items.length">
                Добавить строку
              </button>
              <div v-if="!items.length" class="text-danger mt-2">
                Справочник товаров пуст. Сначала добавьте товары.
              </div>
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

  <!-- Компоненты для быстрого добавления сущностей -->
  <OrganizationForm :visible="showOrgQuickForm" @submit="handleNewOrganization" @cancel="showOrgQuickForm = false" />
  <OrganizationForm :visible="showPayingOrgQuickForm" @submit="handleNewPayingOrganization"
    @cancel="showPayingOrgQuickForm = false" />
  <IndividualForm :visible="showIndividualQuickForm" :positions="positions" @submit="handleNewIndividual"
    @cancel="showIndividualQuickForm = false" @position-added="handlePositionAdded" />
  <ItemForm :visible="showItemQuickForm" @submit="handleNewItem" @cancel="showItemQuickForm = false" />
</template>

<script>
import OrganizationForm from '@/components/OrganizationForm.vue'
import IndividualForm from '@/components/IndividualForm.vue'
import ItemForm from '@/components/ItemForm.vue'
import { mapGetters, mapActions } from 'vuex'

export default {
  emits: ['submit', 'cancel', 'position-added'],
  components: {
    OrganizationForm,
    IndividualForm,
    ItemForm
  },
  props: {
    visible: Boolean,         // Видимость модального окна
    initialData: Object,      // Данные для редактирования
    organizations: Array,     // Список организаций
    individuals: Array,       // Список физических лиц
    items: Array              // Список товаров
  },
  data() {
    return {
      localForm: this.getInitialForm(),  // Локальная копия формы
      isSubmitting: false,               // Флаг отправки формы
      showOrgQuickForm: false,           // Показать форму организации
      showPayingOrgQuickForm: false,     // Показать форму организации-поставщика
      showIndividualQuickForm: false,    // Показать форму физ. лица
      showItemQuickForm: false,          // Показать форму товара
      itemToUpdateIndex: null,           // Индекс редактируемого товара
      originalForm: null,                // Оригинальные данные формы
      periodFrom: '',                    // Дата начала периода
      periodUntil: ''                    // Дата окончания периода
    }
  },
  computed: {
    ...mapGetters(['positions']),
    // Проверяем, редактируем ли мы существующую запись
    editing() {
      return this.initialData !== null
    },
    // Проверка валидности формы
    formValid() {
      const baseValid = this.localForm.number &&
        this.localForm.organization &&
        this.localForm.supplier_organization &&
        this.localForm.individual &&
        this.localForm.date &&
        this.periodFrom &&
        this.periodUntil

      const itemsValid = (this.localForm.items || []).every(item =>
        item.item && item.count !== undefined && item.count !== null
      )

      return baseValid && itemsValid
    }
  },
  watch: {
    // Отслеживаем изменения initialData для заполнения формы
    initialData: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.localForm = {
            _id: newVal._id,
            number: newVal.number,
            date: this.formatDateForInput(newVal.date),
            organization: newVal.organization?._id || newVal.organization,
            supplier_organization: newVal.supplier_organization?._id || newVal.supplier_organization,
            individual: newVal.individual?._id || newVal.individual,
            period: {
              from: this.formatDateForInput(newVal.period?.from),
              until: this.formatDateForInput(newVal.period?.until)
            },
            items: newVal.items?.map(item => ({
              item: item.item?._id || item.item,
              count: item.count
            })) || []
          }

          this.originalForm = JSON.parse(JSON.stringify(this.localForm))
          this.periodFrom = this.localForm.period.from
          this.periodUntil = this.localForm.period.until
        } else {
          this.resetForm()
        }
      }
    }
  },
  methods: {
    // Инициализация формы
    getInitialForm() {
      return {
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
      }
    },
    // Форматирование даты для input[type="date"]
    formatDateForInput(dateStr) {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      return date.toISOString().split('T')[0]
    },
    // Обработка отправки формы
    handleSubmit() {
      if (this.isSubmitting || !this.formValid) return

      const formData = {
        number: this.localForm.number,
        date: this.localForm.date,
        organization: this.localForm.organization,
        supplier_organization: this.localForm.supplier_organization,
        individual: this.localForm.individual,
        period: {
          from: this.periodFrom,
          until: this.periodUntil
        },
        items: this.localForm.items.map(item => ({
          item: item.item,
          count: parseInt(item.count)
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
    // Обработка отмены
    handleCancel() {
      if (this.editing && this.originalForm) {
        this.localForm = JSON.parse(JSON.stringify(this.originalForm))
      } else {
        this.resetForm()
      }
      this.$emit('cancel')
    },
    // Добавление строки с товаром
    addItem() {
      if (this.items.length) {
        this.localForm.items.push({
          item: this.items[0]?._id || null,
          count: 0
        })
      }
    },
    // Удаление строки с товаром
    removeItem(index) {
      this.localForm.items.splice(index, 1)
    },
    // Сброс формы
    resetForm() {
      this.localForm = this.getInitialForm()
      this.originalForm = null
      this.periodFrom = ''
      this.periodUntil = ''
    },
    // Обработка выбора организации
    handleOrganizationSelect(event) {
      if (event.target.value === 'new') {
        this.showOrgQuickForm = true
        this.localForm.organization = null
      }
    },
    // Обработка выбора организации-поставщика
    handlePayingOrganizationSelect(event) {
      if (event.target.value === 'new') {
        this.showPayingOrgQuickForm = true
        this.localForm.supplier_organization = null
      }
    },
    // Обработка выбора физ. лица
    handleIndividualSelect(event) {
      if (event.target.value === 'new') {
        this.$store.dispatch('fetchPositions').then(() => {
          this.showIndividualQuickForm = true
          this.localForm.individual = null
        })
      }
    },
    // Обработка выбора товара
    handleItemSelect(index) {
      if (this.localForm.items[index].item === 'new') {
        this.itemToUpdateIndex = index
        this.showItemQuickForm = true
        this.localForm.items[index].item = null
      }
    },
    // Обработка добавления новой организации
    async handleNewOrganization(newOrg) {
      try {
        const currentOrgId = this.localForm.organization
        this.localForm.organization = null

        await this.$store.dispatch('addOrganization', newOrg)
        await this.$store.dispatch('fetchOrganizations')

        const orgs = this.$store.getters.organizations
        const newOrgId = orgs[orgs.length - 1]._id
        this.localForm.organization = newOrgId

        this.showOrgQuickForm = false
      } catch (error) {
        console.error('Ошибка создания организации:', error)
        this.localForm.organization = currentOrgId
        this.showOrgQuickForm = false
      }
    },
    // Обработка добавления новой организации-поставщика
    async handleNewPayingOrganization(newOrg) {
      try {
        const currentOrgId = this.localForm.supplier_organization
        this.localForm.supplier_organization = null

        await this.$store.dispatch('addOrganization', newOrg)
        await this.$store.dispatch('fetchOrganizations')

        const orgs = this.$store.getters.organizations
        const newOrgId = orgs[orgs.length - 1]._id
        this.localForm.supplier_organization = newOrgId

        this.showPayingOrgQuickForm = false
      } catch (error) {
        console.error('Ошибка создания организации:', error)
        this.localForm.supplier_organization = currentOrgId
        this.showPayingOrgQuickForm = false
      }
    },
    // Обработка добавления нового физ. лица
    async handleNewIndividual(newIndividual) {
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
        this.localForm.individual = newIndividualId

        this.showIndividualQuickForm = false
        return newIndividualId
      } catch (error) {
        console.error('Error creating individual:', error.response?.data || error.message)
        throw error
      }
    },
    // Обработка добавления нового товара
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
    },
    // Обработка добавления новой должности
    async handlePositionAdded() {
      await this.$store.dispatch('fetchPositions')
    }
  }
}
</script>

<style scoped>
date-inputs {
  display: flex;
  gap: 10px;
}

.date-inputs .form-control {
  flex: 1;
}

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
  max-width: 800px;
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
  color: #212529;
  border-collapse: collapse;
}

.table th,
.table td {
  padding: 0.75rem;
  vertical-align: top;
  border-top: 1px solid #dee2e6;
}

.table thead th {
  vertical-align: bottom;
  border-bottom: 2px solid #dee2e6;
}

.table-bordered {
  border: 1px solid #dee2e6;
}

.table-bordered th,
.table-bordered td {
  border: 1px solid #dee2e6;
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