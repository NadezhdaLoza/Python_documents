<template>
  <!-- Модальное окно для добавления/редактирования организации -->
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
              <!-- Поля формы для организации -->
              <div class="mb-3">
                <label class="form-label">Название организации</label>
                <input type="text" class="form-control" v-model="form.title" required>
              </div>

              <div class="mb-3">
                <label class="form-label">Адрес</label>
                <input type="text" class="form-control" v-model="form.address" required>
              </div>

              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="$emit('cancel')">
                  Отмена
                </button>
                <button type="submit" class="btn btn-primary">
                  {{ editing ? 'Обновить' : 'Сохранить' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  props: {
    visible: Boolean,     // Видимость модального окна
    initialData: Object,  // Данные для редактирования
    title: String        // Заголовок окна
  },
  emits: ['submit', 'cancel'],
  data() {
    return {
      form: this.initialData ? { ...this.initialData } : { title: '', address: '' }
    }
  },
  computed: {
    // Проверяем, редактируем ли мы существующую запись
    editing() {
      return this.initialData !== null
    },
    // Заголовок модального окна
    modalTitle() {
      if (this.title) return this.title
      return this.editing ? 'Редактирование организации' : 'Добавление организации'
    }
  },
  methods: {
    // Обработка отправки формы
    handleSubmit() {
      if (!this.form.title) return

      const data = {
        title: this.form.title.trim(),
        address: this.form.address.trim()
      }

      if (this.editing) {
        data._id = this.form._id
      }

      this.$emit('submit', data)
    }
  },
  watch: {
    // Отслеживаем изменения initialData для заполнения формы
    initialData: {
      immediate: true,
      handler(newVal) {
        this.form = newVal ? { ...newVal } : { title: '', address: '' }
      }
    }
  }
}
</script>

<style scoped>
/* Стили модального окна */
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
  max-width: 500px;
  padding: 20px;
}

.modal-container {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
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