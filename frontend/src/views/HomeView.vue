<template>
  <!-- Главная страница приложения -->
  <div class="home">
    <h1>Vue-Flask App</h1>

    <div class="sections-container">
      <!-- Секция документов -->
      <div class="section">
        <h2>Документы</h2>
        <div class="cards-container">
          <router-link to="/proxies" class="card">
            <div class="card-content">
              <h3>Доверенности</h3>
              <p>Управление доверенностями</p>
            </div>
          </router-link>
          <router-link to="/repair_requests" class="card">
            <div class="card-content">
              <h3>Заявки на ремонт оборудования</h3>
              <p>Управление заявками на ремонт оборудования</p>
            </div>
          </router-link>
        </div>
      </div>

      <!-- Секция справочников -->
      <div class="section">
        <h2>Справочники</h2>
        <div class="cards-container">
          <router-link to="/organizations" class="card">
            <div class="card-content">
              <h3>Организации</h3>
              <p>Справочник контрагентов</p>
            </div>
          </router-link>
          <router-link to="/items" class="card">
            <div class="card-content">
              <h3>Товары</h3>
              <p>Справочник товаров</p>
            </div>
          </router-link>
          <router-link to="/positions" class="card">
            <div class="card-content">
              <h3>Должности</h3>
              <p>Справочник должностей</p>
            </div>
          </router-link>
          <router-link to="/individuals" class="card">
            <div class="card-content">
              <h3>Физические лица</h3>
              <p>Справочник физических лиц</p>
            </div>
          </router-link>
          <router-link to="/damages" class="card">
            <div class="card-content">
              <h3>Повреждения</h3>
              <p>Справочник видов повреждений</p>
            </div>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeView'
}
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.sections-container {
  margin-top: 40px;
}

.section {
  margin-bottom: 40px;
}

.section h2 {
  color: #2c3e50;
  border-bottom: 2px solid #eee;
  padding-bottom: 10px;
  margin-bottom: 20px;
}

.cards-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.card {
  display: block;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
  text-decoration: none;
  color: inherit;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.card-content {
  padding: 20px;
}

.card h3 {
  margin-top: 0;
  color: #2c3e50;
}

.card p {
  color: #666;
  margin-bottom: 0;
}

@media (max-width: 768px) {
  .cards-container {
    grid-template-columns: 1fr;
  }
}
</style>