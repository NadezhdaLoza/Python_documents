import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import ProxiesView from "../views/ProxiesView.vue";
import ProxyDetailView from "../views/ProxyDetailView.vue";
import OrganizationsView from "../views/OrganizationsView.vue";
import ItemsView from "../views/ItemsView.vue";
import PositionsView from "../views/PositionsView.vue";
import DamagesView from "../views/DamagesView.vue";
import IndividualsView from "../views/IndividualsView.vue";
import RepairRequestsView from "../views/RequestsView.vue";
import RepairRequestDetailView from "../views/RequestDetailView.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/proxies",
    name: "proxies",
    component: ProxiesView,
  },
  {
    path: "/proxies/:id",
    name: "proxy-detail",
    component: ProxyDetailView,
    props: true,
  },
  {
    path: "/organizations",
    name: "organizations",
    component: OrganizationsView,
  },
  {
    path: "/items",
    name: "items",
    component: ItemsView,
  },
  {
    path: "/positions",
    name: "positions",
    component: PositionsView,
  },
  {
    path: "/individuals",
    name: "individuals",
    component: IndividualsView,
  },
  {
    path: "/damages",
    name: "damages",
    component: DamagesView,
  },
  {
    path: "/repair_requests",
    name: "repair_requests",
    component: RepairRequestsView,
  },
  {
    path: "/repair_requests/:id",
    name: "repair-request-detail",
    component: RepairRequestDetailView,
    props: true,
  },
  // Редирект для несуществующих путей
  {
    path: "/:pathMatch(.*)*",
    redirect: "/",
  },
];

// Создание роутера с историей браузера
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
