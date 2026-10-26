<template>
  <!-- Модальное окно для добавления/редактирования физического лица -->
  <transition name="modal">
    <div class="modal-mask" v-if="visible">
      <div class="modal-wrapper">
        <div class="modal-container">
          <div class="modal-header">
            <h3>{{ modalTitle }}</h3>
            <button class="modal-close" @click="$emit('cancel')">&times;</button>
          </div>

          <div class="modal-body">
            <form @submit.prevent="handleSubmit">
              <!-- Поля формы для ФИО -->
              <div class="mb-3">
                <label class="form-label">Фамилия</label>
                <input type="text" class="form-control" v-model="form.lastname" required>
              </div>

              <div class="mb-3">
                <label class="form-label">Имя</label>
                <input type="text" class="form-control" v-model="form.firstname" required>
              </div>

              <div class="mb-3">
                <label class="form-label">Отчество</label>
                <input type="text" class="form-control" v-model="form.patronymic" required>
              </div>

              <!-- Выбор должности с возможностью добавления новой -->
              <div class="mb-3">
                <label class="form-label">Должность</label>
                <select class="form-select" v-model="form.position_id" required @change="handlePositionSelect">
                  <option value="" disabled>Выберите должность</option>
                  <option value="new" class="text-primary fw-bold">+ Добавить новую должность</option>
                  <option v-for="position in positions" :key="position._id" :value="position._id">
                    {{ position.title }}
                  </option>
                </select>
                <div v-if="!form.position_id && positions.length === 0" class="text-danger small">
                  Нет доступных должностей. Сначала добавьте должности.
                </div>
              </div>

              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="$emit('cancel')">
                  Отмена
                </button>
                <button type="submit" class="btn btn-primary" :disabled="!formValid || !positions.length">
                  {{ editing ? 'Обновить' : 'Сохранить' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </transition>

  <!-- Компонент для быстрого добавления должности -->
  <PositionForm :visible="showPositionQuickForm" @submit="handleNewPosition" @cancel="showPositionQuickForm = false" />
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import PositionForm from '@/components/PositionForm.vue'

export default {
  emits: ['submit', 'cancel'],
  components: {
    PositionForm
  },
  props: {
    visible: Boolean,         // Видимость модального окна
    initialData: Object,      // Данные для редактирования
    title: String,           // Заголовок окна
    positions: Array         // Список должностей
  },
  data() {
    return {
      form: {
        firstname: '',
        lastname: '',
        patronymic: '',
        position_id: null
      },
      showPositionQuickForm: false,  // Показать форму добавления должности
      tempPositionId: null           // Временное хранение ID должности
    }
  },
  computed: {
    // Проверяем, редактируем ли мы существующую запись
    editing() {
      return !!this.initialData
    },
    // Заголовок модального окна
    modalTitle() {
      if (this.title) return this.title
      return this.editing ? 'Редактирование физ. лица' : 'Добавление физ. лица'
    },
    // Проверка валидности формы
    formValid() {
      return this.form.firstname &&
        this.form.lastname &&
        this.form.patronymic &&
        this.form.position_id
    }
  },
  watch: {
    initialData: {
      immediate: true,
      deep: true,
      handler(newVal) {
        if (newVal) {
          this.form = {
            firstname: newVal.firstname || '',
            lastname: newVal.lastname || '',
            patronymic: newVal.patronymic || '',
            position_id: newVal.position_id || newVal.position?._id || newVal.position || null
          }
        } else {
          this.resetForm()
        }
      }
    }
  },
  methods: {
    // Сброс формы
    resetForm() {
      this.form = {
        firstname: '',
        lastname: '',
        patronymic: '',
        position_id: null
      }
    },

    // Обработка отправки формы
    handleSubmit() {
      if (!this.validateForm()) {
        console.warn('Form validation failed')
        return
      }

      this.$emit('submit', {
        lastname: this.form.lastname.trim(),
        firstname: this.form.firstname.trim(),
        patronymic: this.form.patronymic.trim(),
        position_id: this.form.position_id
      })
    },

    // Валидация формы
    validateForm() {
      const isValid = this.form.firstname &&
        this.form.lastname &&
        this.form.patronymic &&
        this.form.position_id
      return isValid
    },

    // Обработка выбора должности
    handlePositionSelect(event) {
      if (event.target.value === 'new') {
        this.tempPositionId = this.form.position_id
        this.form.position_id = null
        this.showPositionQuickForm = true
      }
    },

    // Обработка добавления новой должности
    async handleNewPosition(newPosition) {
      try {
        const currentPositionId = this.form.position_id
        this.form.position_id = null

        await this.$store.dispatch('addPosition', newPosition)
        await this.$store.dispatch('fetchPositions')

        const positions = this.$store.getters.positions

        if (positions.length > 0) {
          this.form.position_id = positions[positions.length - 1]._id
        }

        this.showPositionQuickForm = false
      } catch (error) {
        this.form.position_id = currentPositionId
        this.showPositionQuickForm = false
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
  transition: opacity 0.3s ease;
}

.modal-wrapper {
  width: 100%;
  max-width: 600px;
  padding: 20px;
}

.modal-container {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  max-height: 80vh;
  overflow-y: auto;
  transition: all 0.3s ease;
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
  margin-bottom: 15px;
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

option.text-primary {
  color: #0d6efd;
  font-weight: bold;
}

/* Анимации */
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  transform: scale(0.9);
}
</style>
