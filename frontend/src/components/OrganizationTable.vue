<template>
  <!-- Таблица для отображения списка организаций -->
  <table class="table table-striped table-bordered">
    <thead>
      <tr>
        <th>Название</th>
        <th>Адрес</th>
        <th>Действия</th>
      </tr>
    </thead>
    <tbody>
      <!-- Строки таблицы с данными организаций -->
      <tr v-for="org in organizations" :key="org.id">
        <td>{{ org.title }}</td>
        <td>{{ org.address }}</td>
        <td>
          <!-- Кнопки действий -->
          <button class="btn btn-sm btn-warning me-2" @click="$emit('edit', org)">
            Редактировать
          </button>
          <button class="btn btn-sm btn-danger" @click="$emit('delete', org._id)">
            Удалить
          </button>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: 'OrganizationTable',
  props: {
    organizations: {    // Список организаций
      type: Array,
      required: true
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