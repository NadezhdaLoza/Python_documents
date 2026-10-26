<template>
  <!-- Страница управления должностями -->
  <div>
    <h2>Должности</h2>
    <button 
      class="btn btn-primary mb-3" 
      @click="showForm = true"
    >
      Добавить должность
    </button>

    <!-- Форма добавления/редактирования -->
    <PositionForm 
      :visible="showForm"
      :initial-data="editingPosition"
      @submit="handleSubmit"
      @cancel="resetForm"
    />

    <!-- Таблица должностей -->
    <PositionTable 
      :positions="positions"
      @edit="startEditing"
      @delete="handleDelete"
    />
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import PositionForm from '@/components/PositionForm.vue'
import PositionTable from '@/components/PositionTable.vue'

export default {
  components: {
    PositionForm,
    PositionTable
  },
  data() {
    return {
      showForm: false,            // Показать форму
      editingPosition: null,      // Данные для редактирования
      isProcessing: false         // Флаг обработки
    }
  },
  computed: {
    ...mapGetters(['positions', 'isLoading'])
  },
  methods: {
    ...mapActions(['fetchPositions', 'addPosition', 'updatePosition', 'deletePosition']),

    // Обработка отправки формы
    async handleSubmit(positionData) {
      if (this.isProcessing) return;
      
      this.isProcessing = true;
      try {
        if (this.editingPosition) {
          await this.updatePosition({
            _id: this.editingPosition._id,
            ...positionData
          });
        } else {
          await this.addPosition(positionData);
        }
        this.resetForm();
      } catch (error) {
        console.error('Ошибка:', error);
      } finally {
        this.isProcessing = false;
      }
    },

    // Начало редактирования
    startEditing(position) {
      this.editingPosition = { ...position };
      this.showForm = true;
    },

    // Удаление должности
    async handleDelete(id) {
      if (confirm('Вы уверены, что хотите удалить эту должность?')) {
        try {
          await this.deletePosition(id);
        } catch (error) {
          console.error('Ошибка удаления:', error);
        }
      }
    },

    // Сброс формы
    resetForm() {
      this.showForm = false;
      this.editingPosition = null;
    }
  },
  created() {
    this.fetchPositions();
  }
}
</script>
