<template>
  <!-- Страница управления товарами -->
  <div>
    <h2>Товары</h2>
    <button class="btn btn-primary mb-3" @click="showForm = true">
      Добавить товар
    </button>

    <!-- Форма добавления/редактирования -->
    <ItemForm :visible="showForm" :initial-data="editingItem" @submit="handleSubmit" @cancel="resetForm" />

    <!-- Таблица товаров -->
    <ItemTable :items="items" @edit="startEditing" @delete="handleDelete" />
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import ItemForm from '@/components/ItemForm.vue'
import ItemTable from '@/components/ItemTable.vue'

export default {
  components: {
    ItemForm,
    ItemTable
  },
  data() {
    return {
      showForm: false,        // Показать форму
      editingItem: null,      // Данные для редактирования
      isProcessing: false     // Флаг обработки
    }
  },
  computed: {
    ...mapGetters(['items', 'isLoading'])
  },
  methods: {
    ...mapActions(['fetchItems', 'addItem', 'updateItem', 'deleteItem']),

    // Обработка отправки формы
    async handleSubmit(itemData) {
      if (this.isProcessing) return;

      this.isProcessing = true;
      try {
        if (this.editingItem) {
          await this.updateItem({
            _id: this.editingItem._id,
            ...itemData
          });
        } else {
          await this.addItem(itemData);
        }
        this.resetForm();
      } catch (error) {
        console.error('Ошибка:', error);
      } finally {
        this.isProcessing = false;
      }
    },

    // Начало редактирования
    startEditing(item) {
      this.editingItem = { ...item };
      this.showForm = true;
    },

    // Удаление товара
    async handleDelete(id) {
      if (confirm('Вы уверены, что хотите удалить этот товар?')) {
        try {
          await this.deleteItem(id);
        } catch (error) {
          console.error('Ошибка удаления:', error);
        }
      }
    },

    // Сброс формы
    resetForm() {
      this.showForm = false;
      this.editingItem = null;
    }
  },
  created() {
    this.fetchItems();
  }
}
</script>