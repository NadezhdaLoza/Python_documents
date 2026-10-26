<template>
  <!-- Таблица для отображения списка доверенностей -->
  <table class="table table-striped table-bordered">
    <thead>
      <tr>
        <th>Номер</th>
        <th>Дата</th>
        <th>Организация</th>
        <th>Действия</th>
      </tr>
    </thead>
    <tbody>
      <!-- Строки таблицы с данными доверенностей -->
      <tr v-for="doc in proxies" :key="doc._id" @dblclick="$router.push(`/proxies/${doc._id}`)"
        style="cursor: pointer;">
        <td>{{ doc.number }}</td>
        <td>{{ formatDate(doc.date) }}</td>
        <td>{{ getOrganizationName(doc.organization) }}</td>
        <td>
          <!-- Кнопки действий -->
          <button class="btn btn-sm btn-warning me-2" @click.stop="$emit('edit', doc._id)" :disabled="isLoading">
            Редактировать
          </button>
          <button class="btn btn-sm btn-danger" @click.stop="$emit('delete', doc._id)" :disabled="isLoading">
            Удалить
          </button>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: 'ProxyTable',
  props: {
    proxies: {          // Список доверенностей
      type: Array,
      required: true
    },
    organizations: {    // Список организаций
      type: Array,
      required: true
    },
    isLoading: {        // Флаг загрузки
      type: Boolean,
      default: false
    }
  },
  methods: {
    // Получение названия организации по ID
    getOrganizationName(id) {
      if (!id) return 'Не указана'
      const org = this.organizations.find(o => o._id === id) ||
        (typeof id === 'object' ? id : null)
      return org ? `${org.title}` : 'Неизвестно'
    },
    // Форматирование даты
    formatDate(dateStr) {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      return date.toLocaleDateString()
    }
  }
}
</script>

<style scoped>
.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}
</style>