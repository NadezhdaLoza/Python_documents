<template>
  <div class="repair-requests-view">
    <div class="header">
      <h2>Заявки на ремонт оборудования</h2>
      <button class="btn btn-primary" @click="openForm" :disabled="isLoading">
        Добавить заявку
      </button>
    </div>

    <RepairRequestForm 
      :visible="showForm" 
      :initial-data="editingRequest" 
      :individuals="individuals" 
      :items="items" 
      :damages="damages"
      @submit="handleSubmit" 
      @cancel="closeForm" 
    />

    <div v-if="isLoading" class="text-center my-4">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Загрузка...</span>
      </div>
    </div>

    <RepairRequestTable 
      v-else 
      :requests="requests" 
      :individuals="individuals"
      :is-loading="isLoading" 
      @edit="startEditing" 
      @delete="handleDelete" 
    />
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import RepairRequestForm from '@/components/RepairRequestForm.vue'
import RepairRequestTable from '@/components/RepairRequestTable.vue'

export default {
  name: 'RepairRequestsView',
  components: {
    RepairRequestForm,
    RepairRequestTable
  },
  data() {
    return {
      showForm: false,
      editingRequest: null,
      isProcessing: false,
      error: null
    }
  },
  computed: {
    ...mapGetters([
      'requests',
      'individuals',
      'items',
      'damages',
      'isLoading'
    ])
  },
  methods: {
    ...mapActions([
      'fetchRequests',
      'addRequest',
      'updateRequest',
      'deleteRequest',
      'fetchIndividuals',
      'fetchItems',
      'fetchDamages',
      'fetchRequestById'
    ]),

    async loadData() {
      this.error = null
      try {
        await Promise.all([
          this.fetchIndividuals(),
          this.fetchItems(),
          this.fetchDamages(),
          this.fetchRequests()
        ])
      } catch (error) {
        console.error('Ошибка загрузки данных:', error)
        this.error = 'Не удалось загрузить данные'
      }
    },

    openForm() {
      this.showForm = true
      this.editingRequest = null
    },

    closeForm() {
      this.showForm = false
      this.editingRequest = null
    },

    async handleSubmit(requestData) {
      if (this.isProcessing) return

      this.isProcessing = true
      this.error = null

      try {
        if (this.editingRequest) {
          await this.updateRequest(requestData)
        } else {
          await this.addRequest(requestData)
        }
        this.closeForm()
      } catch (error) {
        console.error('Ошибка сохранения заявки:', error)
        this.error = 'Ошибка при сохранении заявки'
      } finally {
        this.isProcessing = false
      }
    },

    async startEditing(id) {
      try {
        const request = await this.fetchRequestById(id)
        this.editingRequest = { ...request }
        this.showForm = true
      } catch (error) {
        console.error('Ошибка загрузки заявки:', error)
      } finally {
      }
    },

    async handleDelete(id) {
      if (confirm('Вы уверены, что хотите удалить эту заявку?') && !this.isProcessing) {
        this.isProcessing = true
        try {
          await this.deleteRequest(id)
        } catch (error) {
          console.error('Ошибка удаления заявки:', error)
          this.error = 'Ошибка при удалении заявки'
        } finally {
          this.isProcessing = false
        }
      }
    }
  },
  created() {
    this.loadData()
  }
}
</script>

<style scoped>
.repair-requests-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style>