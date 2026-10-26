<template>
  <table class="table table-striped table-bordered">
    <thead>
      <tr>
        <th>Номер</th>
        <th>Дата</th>
        <th>Заказчик</th>
        <th>Подрядчик</th>
        <th>Действия</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="request in requests" :key="request._id" @dblclick="$router.push(`/repair_requests/${request._id}`)" style="cursor: pointer;">
        <td>{{ request.number }}</td>
        <td>{{ formatDate(request.date) }}</td>
        <td>{{ getIndividualName(request.customer) }}</td>
        <td>{{ getIndividualName(request.contractor) }}</td>
        <td>
          <button class="btn btn-sm btn-warning me-2" @click.stop="$emit('edit', request._id)" :disabled="isLoading">
            Редактировать
          </button>
          <button class="btn btn-sm btn-danger" @click.stop="$emit('delete', request._id)" :disabled="isLoading">
            Удалить
          </button>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: 'RepairRequestTable',
  props: {
    requests: {
      type: Array,
      required: true
    },
    individuals: {
      type: Array,
      required: true
    },
    isLoading: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    getIndividualName(individual) {
      if (!individual) return 'Не указано'

      if (individual.lastname) {
        return `${individual.lastname} ${individual.firstname} ${individual.patronymic || ''}`.trim()
      }

      const found = this.individuals.find(i => i._id === individual)
      return found ? `${found.lastname} ${found.firstname} ${found.patronymic || ''}`.trim() : 'Неизвестно'
    },
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