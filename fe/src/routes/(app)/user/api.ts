import { api } from "$lib/axios"; 
import type { User } from '$lib/interfaces/user.interfaces'; 
import type { Role } from '$lib/interfaces/role.interfaces'; 

export const getAllUsers = async (search: string = ''): Promise<User[]> => {
    try {
        const response = await api.get(`/users?search=${search}`);
        // Asumsi API mengembalikan { message: "...", data: [...] }
        return response.data.data;
    } catch (error) {
        console.error('Failed to fetch users:', error);
        throw error;
    }
};

export const getAllRoles = async (): Promise<Role[]> => {
    try {
        const response = await api.get(`/roles`);
        return response.data.data;
    } catch (error) {
        console.error('Failed to fetch roles:', error);
        throw error;
    }
};

export const approveUser = async (userId: string): Promise<void> => {
    try {
        await api.patch(`/users/${userId}/approve`); 
    } catch (error) {
        console.error(`Failed to approve user ${userId}:`, error);
        throw error;
    }
};

export const rejectUser = async (userId: string): Promise<void> => {
    try {
        await api.patch(`/users/${userId}/reject`); 
    } catch (error) {
        console.error(`Failed to reject user ${userId}:`, error);
        throw error;
    }
};

export const deleteUser = async (userId: string): Promise<void> => {
    try {
        await api.delete(`/users/${userId}`);
    } catch (error) {
        console.error(`Failed to delete user ${userId}:`, error);
        throw error;
    }
};

export const updateUser = async (userId: string, payload: object): Promise<User> => {
    try {
        const response = await api.put(`/users/${userId}`, payload);
        return response.data.data;
    } catch (error) {
        console.error(`Failed to update user ${userId}:`, error);
        throw error;
    }
};

export const resetUserPassword = async (userId: string): Promise<void> => {
    try {
        await api.post(`/users/${userId}/reset-password`);
    } catch (error) {
        console.error(`Failed to reset password for user ${userId}:`, error);
        throw error;
    }
};
