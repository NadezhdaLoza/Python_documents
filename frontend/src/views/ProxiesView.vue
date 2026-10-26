<template>
  <!-- Страница управления доверенностями -->
  <div class="proxies-view">
    <div class="header">
      <h2>Доверенности</h2>
      <button class="btn btn-primary" @click="openForm" :disabled="isLoading">
        Добавить документ
      </button>
    </div>

    <!-- Форма добавления/редактирования -->
    <ProxyForm :visible="showForm" :initial-data="editingProxy" :organizations="organizations"
      :individuals="individuals" :items="items" @submit="handleSubmit" @cancel="closeForm" />

    <!-- Индикатор загрузки -->
    <div v-if="isLoading" class="text-center my-4">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Загрузка...</span>
      </div>
    </div>

    <!-- Таблица доверенностей -->
    <ProxyTable v-else :proxies="proxies" :organizations="organizations" :individuals="individuals"
      :is-loading="isLoading" @edit="startEditing" @delete="handleDelete" />
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import ProxyForm from '@/components/ProxyForm.vue'
import ProxyTable from '@/components/ProxyTable.vue'

export default {
  name: 'ProxiesView',
  components: {
    ProxyForm,
    ProxyTable
  },
  data() {
    return {
      showForm: false,          // Показать форму
      editingProxy: null,       // Данные для редактирования
      isProcessing: false,      // Флаг обработки
      error: null               // Ошибка
    }
  },
  computed: {
    ...mapGetters([
      'proxies',
      'organizations',
      'individuals',
      'items',
      'isLoading'
    ])
  },
  methods: {
    ...mapActions([
      'fetchProxies',
      'addProxy',
      'updateProxy',
      'deleteProxy',
      'fetchOrganizations',
      'fetchIndividuals',
      'fetchItems',
      'fetchProxyById'
    ]),

    // Загрузка данных
    async loadData() {
      this.error = null
      try {
        await Promise.all([
          this.fetchOrganizations(),
          this.fetchIndividuals(),
          this.fetchItems(),
          this.fetchProxies()
        ])
      } catch (error) {
        console.error('Ошибка загрузки данных:', error)
        this.error = 'Не удалось загрузить данные'
      }
    },

    // Открытие формы
    openForm() {
      this.showForm = true
      this.editingProxy = null
    },

    // Закрытие формы
    closeForm() {
      this.showForm = false
      this.editingProxy = null
    },

    // Обработка отправки формы
    async handleSubmit(proxyData) {
      if (this.isProcessing) return

      this.isProcessing = true
      this.error = null

      try {
        if (this.editingProxy) {
          await this.updateProxy(proxyData)
        } else {
          await this.addProxy(proxyData)
        }
        this.closeForm()
      } catch (error) {
        console.error('Ошибка сохранения документа:', error)
        this.error = 'Ошибка при сохранении документа'
      } finally {
        this.isProcessing = false
      }
    },

    // Начало редактирования
    async startEditing(id) {
      this.isLoading = true
      try {
        const proxy = await this.fetchProxyById(id)
        this.editingProxy = proxy
        this.showForm = true
      } catch (error) {
        console.error('Ошибка загрузки документа:', error)
      } finally {
        this.isLoading = false
      }
    },

    // Удаление доверенности
    async handleDelete(id) {
      if (confirm('Вы уверены, что хотите удалить этот документ?') && !this.isProcessing) {
        this.isProcessing = true
        try {
          await this.deleteProxy(id)
        } catch (error) {
          console.error('Ошибка удаления документа:', error)
          this.error = 'Ошибка при удалении документа'
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
.proxies-view {
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