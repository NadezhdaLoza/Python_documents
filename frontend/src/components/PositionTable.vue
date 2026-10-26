<template>
  <!-- Таблица для отображения списка должностей -->
  <table class="table table-striped table-bordered">
    <thead>
      <tr>
        <th>Название</th>
        <th>Действия</th>
      </tr>
    </thead>
    <tbody>
      <!-- Строки таблицы с данными должностей -->
      <tr v-for="position in positions" :key="position.id">
        <td>{{ position.title }}</td>
        <td>
          <!-- Кнопки действий -->
          <button class="btn btn-sm btn-warning me-2" @click="$emit('edit', position)">
            Редактировать
          </button>
          <button class="btn btn-sm btn-danger" @click="$emit('delete', position._id)">
            Удалить
          </button>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: 'PositionTable',
  props: {
    positions: {    // Список должностей
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
