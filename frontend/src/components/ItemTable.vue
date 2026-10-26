<template>
  <!-- Таблица для отображения списка товаров -->
  <table class="table table-striped table-bordered">
    <thead>
      <tr>
        <th>Название</th>
        <th>Действия</th>
      </tr>
    </thead>
    <tbody>
      <!-- Строки таблицы с данными товаров -->
      <tr v-for="item in items" :key="item.id">
        <td>{{ item.title }}</td>
        <td>
          <!-- Кнопки действий -->
          <button class="btn btn-sm btn-warning me-2" @click="$emit('edit', item)">
            Редактировать
          </button>
          <button class="btn btn-sm btn-danger" @click="$emit('delete', item._id)">
            Удалить
          </button>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: 'ItemTable',
  props: {
    items: {    // Список товаров
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