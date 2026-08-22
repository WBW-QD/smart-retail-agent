import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 120000
})

export const chat = (message, context = '') =>
  api.post('/chat', { message, context }).then(r => r.data)

export const getRecommendation = (customer_id) =>
  api.post('/recommend', { customer_id }).then(r => r.data)

export const getCustomerProfile = (customer_id) =>
  api.get('/customer/profile', { params: { customer_id } }).then(r => r.data)

export const getCustomers = () =>
  api.get('/customers').then(r => r.data)

export const getMarketing = (customer_id, activity_type = '会员促销') =>
  api.post('/customer/marketing', { customer_id, activity_type }).then(r => r.data)

export const getInventory = () =>
  api.get('/inventory').then(r => r.data)

export const getRestockSuggestion = (product_id) =>
  api.post('/inventory/restock', { product_id }).then(r => r.data)

export const getDashboardSales = () =>
  api.get('/dashboard/sales').then(r => r.data)

export const queryDashboard = (question) =>
  api.post('/dashboard/query', { question }).then(r => r.data)

export const getHistory = () =>
  api.get('/history').then(r => r.data)

export const clearHistory = () =>
  api.delete('/history').then(r => r.data)

export const getProducts = () =>
  api.get('/products').then(r => r.data)

export default api
