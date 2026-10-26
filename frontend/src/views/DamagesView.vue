<template>
  <!-- Страница управления повреждениями -->
  <div>
    <h2>Характеры повреждений</h2>
    <button class="btn btn-primary mb-3" @click="showForm = true">
      Добавить характер повреждения
    </button>

    <!-- Форма добавления/редактирования -->
    <DamageForm :visible="showForm" :initial-data="editingDamage" @submit="handleSubmit" @cancel="resetForm" />

    <!-- Таблица характеров повреждений -->
    <DamageTable :damages="damages" @edit="startEditing" @delete="handleDelete" />
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import DamageForm from '@/components/DamageForm.vue'
import DamageTable from '@/components/DamageTable.vue'

export default {
  components: {
    DamageForm,
    DamageTable
  },
  data() {
    return {
      showForm: false,        // Показать форму
      editingDamage: null,      // Данные для редактирования
      isProcessing: false     // Флаг обработки
    }
  },
  computed: {
    ...mapGetters(['damages', 'isLoading'])
  },
  methods: {
    ...mapActions(['fetchDamages', 'addDamage', 'updateDamage', 'deleteDamage']),

    // Обработка отправки формы
    async handleSubmit(damageData) {
      if (this.isProcessing) return;

      this.isProcessing = true;
      try {
        if (this.editingDamage) {
          await this.updateDamage({
            _id: this.editingDamage._id,
            ...damageData
          });
        } else {
          await this.addDamage(damageData);
        }
        this.resetForm();
      } catch (error) {
        console.error('Ошибка:', error);
      } finally {
        this.isProcessing = false;
      }
    },

    // Начало редактирования
    startEditing(damage) {
        this.editingDamage = { ...damage };
        this.showForm = true;
    },

    // Удаление товара
    async handleDelete(id) {
      if (confirm('Вы уверены, что хотите удалить характер повреждения?')) {
        try {
          await this.deleteDamage(id);
        } catch (error) {
          console.error('Ошибка удаления:', error);
        }
      }
    },

    // Сброс формы
    resetForm() {
      this.showForm = false;
      this.editingDamage = null;
    }
  },
  created() {
    this.fetchDamages();
  }
}
</script>