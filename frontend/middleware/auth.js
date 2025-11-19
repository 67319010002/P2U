export default defineNuxtRouteMiddleware(() => {
  if (process.server) return
  const token = localStorage.getItem('token')
  if (!token || token === 'undefined' || token === 'null') {
    return navigateTo('/login')
  }
})