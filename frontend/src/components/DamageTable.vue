<template>
  <!-- Таблица для отображения списка повреждений -->
  <table class="table table-striped table-bordered">
    <thead>
      <tr>
        <th>Название</th>
        <th>Действия</th>
      </tr>
    </thead>
    <tbody>
      <!-- Строки таблицы с данными повреждений -->
      <tr v-for="damage in damages" :key="damage.id">
        <td>{{ damage.title }}</td>
        <td>
          <!-- Кнопки действий -->
          <button class="btn btn-sm btn-warning me-2" @click="$emit('edit', damage)">
            Редактировать
          </button>
          <button class="btn btn-sm btn-danger" @click="$emit('delete', damage._id)">
            Удалить
          </button>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: 'DamageTable',
  props: {
    damages: {    // Список повреждений
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