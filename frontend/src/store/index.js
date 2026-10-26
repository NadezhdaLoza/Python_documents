import { createStore } from "vuex";
import axios from "axios";

const isDevelopment = process.env.NODE_ENV === "development";

const api = axios.create({
  baseURL: "http://localhost:5000/api/",
  timeout: 5000,
});

export default createStore({
  state: {
    organizations: [],
    proxies: [],
    items: [],
    damages: [],
    positions: [],
    individuals: [],
    requests: [],
    currentRequest: null,
    isLoading: false,
    currentProxy: null,
  },
  mutations: {
    SET_ORGANIZATIONS(state, organizations) {
      state.organizations = organizations;
    },
    SET_ITEMS(state, items) {
      state.items = items;
    },
    SET_DAMAGES(state, damages) {
      state.damages = damages;
    },
    SET_POSITIONS(state, positions) {
      state.positions = positions;
    },
    SET_INDIVIDUALS(state, individuals) {
      state.individuals = individuals;
    },
    SET_PROXIES(state, proxies) {
      state.proxies = proxies;
    },
    SET_REQUESTS(state, requests) {
      state.requests = requests;
    },
    SET_CURRENT_REQUEST(state, request) {
      state.currentRequest = request;
    },
    SET_CURRENT_PROXY(state, proxy) {
      state.currentProxy = proxy;
    },
    SET_LOADING(state, isLoading) {
      state.isLoading = isLoading;
    },
  },
  actions: {
    async fetchItems({ commit }) {
      commit("SET_LOADING", true);
      try {
        const response = await api.get("/items/");
        commit("SET_ITEMS", response.data);
      } catch (error) {
        console.error("Error fetching items:", error);
        throw error;
      } finally {
        commit("SET_LOADING", false);
      }
    },

    async addItem({ commit, dispatch }, item) {
      commit("SET_LOADING", true);
      try {
        await api.post("/items/", { title: item.title });
        await dispatch("fetchItems");
      } catch (error) {
        console.error("Error adding item:", error);
        throw error;
      } finally {
        commit("SET_LOADING", false);
      }
    },

    async updateItem({ commit, dispatch }, { _id, ...item }) {
      commit("SET_LOADING", true);
      try {
        await api.put("/items/", { _id, title: item.title });
        await dispatch("fetchItems");
      } catch (error) {
        console.error("Error updating item:", error);
        throw error;
      } finally {
        commit("SET_LOADING", false);
      }
    },

    async deleteItem({ commit, dispatch }, id) {
      commit("SET_LOADING", true);
      try {
        await api.delete(`/items/${id}`);
        await dispatch("fetchItems");
      } catch (error) {
        console.error("Error deleting item:", error);
        throw error;
      } finally {
        commit("SET_LOADING", false);
      }
    },

    async fetchPositions({ commit }) {
      commit("SET_LOADING", true);
      try {
        const response = await api.get("/positions/");
        commit("SET_POSITIONS", response.data);
      } catch (error) {
        console.error("Error fetching positions:", error);
        throw error;
      } finally {
        commit("SET_LOADING", false);
      }
    },

    async addPosition({ commit, dispatch }, position) {
      commit("SET_LOADING", true);
      try {
        await api.post("/positions/", { title: position.title });
        await dispatch("fetchPositions");
      } catch (error) {
        console.error("Error adding position:", error);
        throw error;
      } finally {
        commit("SET_LOADING", false);
      }
    },

    async updatePosition({ commit, dispatch }, { _id, ...position }) {
      commit("SET_LOADING", true);
      try {
        await api.put("/positions/", { _id, title: position.title });
        await dispatch("fetchPositions");
      } catch (error) {
        console.error("Error updating position:", error);
        throw error;
      } finally {
        commit("SET_LOADING", false);
      }
    },

    async deletePosition({ commit, dispatch }, id) {
      commit("SET_LOADING", true);
      try {
        await api.delete(`/positions/${id}`);
        await dispatch("fetchPositions");
      } catch (error) {
        console.error("Error deleting position:", error);
        throw error;
      } finally {
        commit("SET_LOADING", false);
      }
    },

    // ========== Организации ==========
    async fetchOrganizations({ commit }) {
      commit("SET_LOADING", true);
      try {
        const response = await api.get("/organizations/");
        commit("SET_ORGANIZATIONS", response.data);
      } catch (error) {
        console.error("Error fetching organizations:", error);
        throw error;
      } finally {
        commit("SET_LOADING", false);
      }
    },

    async addOrganization({ commit, dispatch }, organization) {
      commit("SET_LOADING", true);
      try {
        await api.post("/organizations/", {
          title: organization.title,
          address: organization.address,
          OKPO: organization.OKPO,
        });
        await dispatch("fetchOrganizations");
      } catch (error) {
        console.error("Error adding organization:", error);
        throw error;
      } finally {
        commit("SET_LOADING", false);
      }
    },

    async updateOrganization({ commit, dispatch }, { _id, ...organization }) {
      commit("SET_LOADING", true);
      try {
        await api.put("/organizations/", {
          _id,
          title: organization.title,
          address: organization.address,
          OKPO: organization.OKPO,
        });
        await dispatch("fetchOrganizations");
      } catch (error) {
        console.error("Error updating organization:", error);
        throw error;
      } finally {
        commit("SET_LOADING", false);
      }
    },

    async deleteOrganization({ commit, dispatch }, id) {
      commit("SET_LOADING", true);
      try {
        await api.delete(`/organizations/${id}`);
        await dispatch("fetchOrganizations");
      } catch (error) {
        console.error("Error deleting organization:", error);
        throw error;
      } finally {
        commit("SET_LOADING", false);
      }
    },

    // ========== Физические лица ==========
    async fetchIndividuals({ commit }) {
      commit("SET_LOADING", true);
      try {
        const response = await api.get("/individuals/");
        commit("SET_INDIVIDUALS", response.data);
      } catch (error) {
        console.error("Error fetching individuals:", error);
        throw error;
      } finally {
        commit("SET_LOADING", false);
      }
    },

    async addIndividual({ commit, dispatch }, individual) {
      commit("SET_LOADING", true);
      try {
        const response = await api.post("/individuals/", {
          lastname: individual.lastname,
          firstname: individual.firstname,
          patronymic: individual.patronymic,
          position: individual.position,
        });
        await dispatch("fetchIndividuals");
        return response.data;
      } catch (error) {
        console.error("Error adding individual:", error);
        throw error;
      } finally {
        commit("SET_LOADING", false);
      }
    },

    async updateIndividual({ commit, dispatch }, { _id, ...individual }) {
      commit("SET_LOADING", true);
      try {
        await api.put("/individuals/", {
          _id,
          lastname: individual.lastname,
          firstname: individual.firstname,
          patronymic: individual.patronymic,
          position: individual.position,
        });
        await dispatch("fetchIndividuals");
      } catch (error) {
        console.error("Error updating individual:", error);
        throw error;
      } finally {
        commit("SET_LOADING", false);
      }
    },

    async deleteIndividual({ commit, dispatch }, id) {
      commit("SET_LOADING", true);
      try {
        await api.delete(`/individuals/${id}`);
        await dispatch("fetchIndividuals");
      } catch (error) {
        console.error("Error deleting individual:", error);
        throw error;
      } finally {
        commit("SET_LOADING", false);
      }
    },

    // ========== Повреждения ==========
    async fetchDamages({ commit }) {
      commit("SET_LOADING", true);
      try {
        const response = await api.get("/damages/");
        commit("SET_DAMAGES", response.data);
      } catch (error) {
        console.error("Error fetching damages:", error);
        throw error;
      } finally {
        commit("SET_LOADING", false);
      }
    },

    async addDamage({ commit, dispatch }, damage) {
      commit("SET_LOADING", true);
      try {
        await api.post("/damages/", { title: damage.title });
        await dispatch("fetchDamages");
      } catch (error) {
        console.error("Error adding damage:", error);
        throw error;
      } finally {
        commit("SET_LOADING", false);
      }
    },

    async updateDamage({ commit, dispatch }, { _id, ...damage }) {
      commit("SET_LOADING", true);
      try {
        await api.put("/damages/", { _id, title: damage.title });
        await dispatch("fetchDamages");
      } catch (error) {
        console.error("Error updating damage:", error);
        throw error;
      } finally {
        commit("SET_LOADING", false);
      }
    },

    async deleteDamage({ commit, dispatch }, id) {
      commit("SET_LOADING", true);
      try {
        await api.delete(`/damages/${id}`);
        await dispatch("fetchDamages");
      } catch (error) {
        console.error("Error deleting damage:", error);
        throw error;
      } finally {
        commit("SET_LOADING", false);
      }
    },

    // ========== Доверенности ==========
    async fetchProxies({ commit }) {
      commit("SET_LOADING", true);
      try {
        const response = await api.get("/proxies/");
        commit("SET_PROXIES", response.data);
      } catch (error) {
        console.error("Error fetching proxies:", error);
        throw error;
      } finally {
        commit("SET_LOADING", false);
      }
    },

    async fetchProxyById({ commit }, id) {
      commit("SET_LOADING", true);
      try {
        const response = await api.get(`/proxies/${id}`);
        const proxy = {
          _id: response.data._id,
          number: response.data.number,
          date: response.data.date,
          organization:
            response.data.organization?._id || response.data.organization,
          supplier_organization:
            response.data.supplier_organization?._id ||
            response.data.supplier_organization,
          individual: response.data.individual?._id || response.data.individual,
          period: response.data.period || { from: "", until: "" },
          items: response.data.items || [],
        };
        commit("SET_CURRENT_PROXY", proxy);
        return proxy;
      } catch (error) {
        console.error("Error fetching proxy by id:", error);
        throw error;
      } finally {
        commit("SET_LOADING", false);
      }
    },

    async addProxy({ commit, dispatch }, proxy) {
      commit("SET_LOADING", true);
      try {
        const proxyData = {
          number: proxy.number,
          date: proxy.date,
          organization: proxy.organization,
          supplier_organization: proxy.supplier_organization,
          individual: proxy.individual,
          period: {
            from: proxy.period.from,
            until: proxy.period.until,
          },
          items: proxy.items.map((item) => ({
            item: item.item,
            count: parseInt(item.count),
          })),
        };

        const response = await api.post("/proxies/", proxyData);
        await dispatch("fetchProxies");
        return response.data;
      } catch (error) {
        console.error("Error adding proxy:", error);
        throw error;
      } finally {
        commit("SET_LOADING", false);
      }
    },

    async updateProxy({ commit, dispatch }, proxy) {
      commit("SET_LOADING", true);
      try {
        const proxyData = {
          _id: proxy._id,
          number: proxy.number,
          date: proxy.date,
          organization: proxy.organization,
          supplier_organization: proxy.supplier_organization,
          individual: proxy.individual,
          period: {
            from: proxy.period.from,
            until: proxy.period.until,
          },
          items: proxy.items.map((item) => ({
            item: item.item,
            count: parseInt(item.count),
          })),
        };

        await api.put("/proxies/", proxyData);
        await dispatch("fetchProxies");
      } catch (error) {
        console.error("Error updating proxy:", error);
        throw error;
      } finally {
        commit("SET_LOADING", false);
      }
    },

    async deleteProxy({ commit, dispatch }, id) {
      commit("SET_LOADING", true);
      try {
        await api.delete(`/proxies/${id}`);
        await dispatch("fetchProxies");
      } catch (error) {
        console.error("Error deleting proxy:", error);
        throw error;
      } finally {
        commit("SET_LOADING", false);
      }
    },

    // ========== Заявки на ремонт ==========
    async fetchRequests({ commit }) {
      commit("SET_LOADING", true);
      try {
        const response = await api.get("/repair_requests/");
        commit("SET_REQUESTS", response.data);
      } catch (error) {
        console.error("Error fetching requests:", error);
        throw error;
      } finally {
        commit("SET_LOADING", false);
      }
    },

    async fetchRequestById({ commit }, id) {
      commit("SET_LOADING", true);
      try {
        const response = await api.get(`/repair_requests/${id}`);
        commit("SET_CURRENT_REQUEST", response.data);
        return response.data;
      } catch (error) {
        console.error("Error fetching request by id:", error);
        throw error;
      } finally {
        commit("SET_LOADING", false);
      }
    },

    async addRequest({ commit, dispatch }, request) {
      commit("SET_LOADING", true);
      try {
        const response = await api.post("/repair_requests/", request);
        await dispatch("fetchRequests");
        return response.data;
      } catch (error) {
        console.error("Error adding request:", error);
        throw error;
      } finally {
        commit("SET_LOADING", false);
      }
    },

    async updateRequest({ commit, dispatch }, request) {
      commit("SET_LOADING", true);
      try {
        await api.put("/repair_requests/", request);
        await dispatch("fetchRequests");
      } catch (error) {
        console.error("Error updating request:", error);
        throw error;
      } finally {
        commit("SET_LOADING", false);
      }
    },

    async deleteRequest({ commit, dispatch }, id) {
      commit("SET_LOADING", true);
      try {
        await api.delete(`/repair_requests/${id}`);
        await dispatch("fetchRequests");
      } catch (error) {
        console.error("Error deleting request:", error);
        throw error;
      } finally {
        commit("SET_LOADING", false);
      }
    },
  },
  getters: {
    organizations: (state) => state.organizations,
    individuals: (state) => state.individuals,
    proxies: (state) => state.proxies,
    items: (state) => state.items,
    damages: (state) => state.damages,
    positions: (state) => state.positions,
    requests: (state) => state.requests,
    currentRequest: (state) => state.currentRequest,
    isLoading: (state) => state.isLoading,
    currentProxy: (state) => state.currentProxy,

    getItemById: (state) => (id) => state.items.find((item) => item._id === id),
    getDamageById: (state) => (id) =>
      state.damages.find((damage) => damage._id === id),
    getPositionById: (state) => (id) =>
      state.positions.find((pos) => pos._id === id),
    getOrganizationById: (state) => (id) =>
      state.organizations.find((org) => org._id === id),
    getIndividualById: (state) => (id) =>
      state.individuals.find((ind) => ind._id === id),
    getProxyById: (state) => (id) =>
      state.proxies.find((proxy) => proxy._id === id),
    getRequestById: (state) => (id) =>
      state.requests.find((request) => request._id === id),
  },
});
