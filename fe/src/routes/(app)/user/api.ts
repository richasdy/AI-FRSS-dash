import { api } from "$lib/axios"

export const getAllUsers = async (search: string) => {
    const response = await api.get(`/users?search=${search}`)

    return response.data
}