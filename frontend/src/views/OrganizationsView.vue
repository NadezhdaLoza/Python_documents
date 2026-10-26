<template>
  <!-- Страница управления организациями -->
  <div>
    <h2>Организации</h2>
    <button class="btn btn-primary mb-3" @click="showForm = true">
      Добавить организацию
    </button>

    <!-- Форма добавления/редактирования -->
    <OrganizationForm :visible="showForm" :initial-data="editingOrganization" @submit="handleSubmit"
      @cancel="resetForm" />

    <!-- Таблица организаций -->
    <OrganizationTable :organizations="organizations" @edit="startEditing" @delete="handleDelete" />
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import OrganizationForm from '@/components/OrganizationForm.vue'
import OrganizationTable from '@/components/OrganizationTable.vue'

export default {
  components: {
    OrganizationForm,
    OrganizationTable
  },
  data() {
    return {
      showForm: false,              // Показать форму
      editingOrganization: null,     // Данные для редактирования
      isProcessing: false           // Флаг обработки
    }
  },
  computed: {
    ...mapGetters(['organizations', 'isLoading'])
  },
  methods: {
    ...mapActions(['fetchOrganizations', 'addOrganization', 'updateOrganization', 'deleteOrganization']),

    // Обработка отправки формы
    async handleSubmit(organizationData) {
      if (this.isProcessing) return;

      this.isProcessing = true;
      try {
        if (this.editingOrganization) {
          await this.updateOrganization({
            _id: this.editingOrganization._id,
            ...organizationData
          });
        } else {
          await this.addOrganization(organizationData);
        }
        this.resetForm();
      } catch (error) {
        console.error('Ошибка:', error);
      } finally {
        this.isProcessing = false;
      }
    },

    // Начало редактирования
    startEditing(organization) {
      this.editingOrganization = { ...organization };
      this.showForm = true;
    },

    // Удаление организации
    async handleDelete(id) {
      if (confirm('Вы уверены, что хотите удалить эту организацию?')) {
        try {
          await this.deleteOrganization(id);
        } catch (error) {
          console.error('Ошибка удаления:', error);
        }
      }
    },

    // Сброс формы
    resetForm() {
      this.showForm = false;
      this.editingOrganization = null;
    }
  },
  created() {
    this.fetchOrganizations();
  }
}
</script>