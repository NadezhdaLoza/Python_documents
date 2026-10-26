<template>
  <!-- Страница управления физическими лицами -->
  <div>
    <h2>Физические лица</h2>
    <button class="btn btn-primary mb-3" @click="showForm = true">
      Добавить физ. лицо
    </button>

    <!-- Форма добавления/редактирования -->
    <IndividualForm :visible="showForm" :initial-data="editingIndividual" :positions="positions" @submit="handleSubmit"
      @cancel="resetForm" />

    <!-- Таблица физических лиц -->
    <IndividualTable :individuals="individuals" :positions="positions" @edit="startEditing" @delete="handleDelete" />
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import IndividualForm from '@/components/IndividualForm.vue'
import IndividualTable from '@/components/IndividualTable.vue'

export default {
  components: {
    IndividualForm,
    IndividualTable
  },
  data() {
    return {
      showForm: false,          // Показать форму
      editingIndividual: null,  // Данные для редактирования
      isProcessing: false       // Флаг обработки
    }
  },
  computed: {
    ...mapGetters(['individuals', 'positions', 'isLoading'])
  },
  methods: {
    ...mapActions([
      'fetchIndividuals',
      'addIndividual',
      'updateIndividual',
      'deleteIndividual',
      'fetchPositions'
    ]),

    // Обработка отправки формы
    async handleSubmit(individualData) {
      if (this.isProcessing) return;

      this.isProcessing = true;
      try {
        const dataToSend = {
          lastname: individualData.lastname,
          firstname: individualData.firstname,
          patronymic: individualData.patronymic,
          position: individualData.position_id
        };

        if (this.editingIndividual) {
          dataToSend._id = this.editingIndividual._id;
          await this.updateIndividual(dataToSend)
        } else {
          await this.addIndividual(dataToSend)
        }

        await this.fetchIndividuals()
        this.resetForm()
      } catch (error) {
        console.error('Error saving individual:', error)
      } finally {
        this.isProcessing = false
      }
    },

    // Начало редактирования
    startEditing(individual) {
      this.editingIndividual = {
        ...individual,
        position_id: individual.position?._id || individual.position
      }
      this.showForm = true
    },

    // Удаление физического лица
    async handleDelete(id) {
      if (confirm('Вы уверены, что хотите удалить это физ. лицо?')) {
        try {
          await this.deleteIndividual(id)
        } catch (error) {
          console.error('Ошибка удаления:', error)
        }
      }
    },

    // Сброс формы
    resetForm() {
      this.showForm = false
      this.editingIndividual = null
    }
  },
  async created() {
    try {
      await this.fetchIndividuals()
      await this.fetchPositions()
    } catch (error) {
      console.error('Error loading data:', error)
    }
  }
}
</script>
