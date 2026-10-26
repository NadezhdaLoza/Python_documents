<template>
  <!-- Таблица для отображения списка физических лиц -->
  <table class="table table-striped table-bordered">
    <thead>
      <tr>
        <th>ФИО</th>
        <th>Должность</th>
        <th>Действия</th>
      </tr>
    </thead>
    <tbody>
      <!-- Строки таблицы с данными физических лиц -->
      <tr v-for="individual in individuals" :key="individual._id">
        <td>{{ fullName(individual) }}</td>
        <td>{{ getPositionTitle(individual.position) }}</td>
        <td>
          <!-- Кнопки действий -->
          <button class="btn btn-sm btn-warning me-2" @click="$emit('edit', individual)">
            Редактировать
          </button>
          <button class="btn btn-sm btn-danger" @click="$emit('delete', individual._id)">
            Удалить
          </button>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: 'IndividualTable',
  props: {
    individuals: {   // Список физических лиц
      type: Array,
      required: true
    },
    positions: {     // Список должностей
      type: Array,
      required: true
    }
  },
  methods: {
    // Формирование полного имени
    fullName(individual) {
      return `${individual.lastname} ${individual.firstname} ${individual.patronymic || ''}`.trim()
    },
    // Получение названия должности
    getPositionTitle(position) {
      if (!position) return 'Не указана'

      if (typeof position === 'object' && position.title) {
        return position.title
      }

      const foundPosition = this.positions.find(p => p._id === position)
      return foundPosition ? foundPosition.title : 'Неизвестная должность'
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
