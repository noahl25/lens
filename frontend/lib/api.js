export const useApi = () => {

    const makeRequest = async (endpoint, options = {}) => {

        const response = await fetch(`http://localhost:10000/api/${endpoint}`, {
            ...options,
            headers: {
                "Content-Type": "application/json"
            }
        })

        if (!response.ok) {
            const errorData = await response.json().catch(() => null);
            throw new Error(errorData?.detail || "An error occured.");
        }

        return response.json();
    }

    return { makeRequest };

}