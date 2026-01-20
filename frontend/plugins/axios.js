import axios from "axios";

export default defineNuxtPlugin((nuxtApp) => {
    const baseUrl = "http://localhost:5000";

    axios.defaults.baseURL = baseUrl;

    // Response interceptor
    axios.interceptors.response.use(
        (response) => response,
        (error) => {
            if (error.response && error.response.status === 401) {
                // Clear local storage
                if (process.client) {
                    localStorage.removeItem("token");
                    localStorage.removeItem("user");
                    window.dispatchEvent(new Event("user-updated"));

                    // Redirect to login if not already there
                    const router = useRouter(); // Use Nuxt router if available in context, or window.location
                    if (window.location.pathname !== '/login') {
                        window.location.href = '/login';
                    }
                }
            }
            return Promise.reject(error);
        }
    );

    return {
        provide: {
            axios: axios,
        },
    };
});
