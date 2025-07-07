import { api } from "$lib/axios";

// Get all users
export const getAllUsers = async (search: string) => {
	const response = await api.get(`/users?search=${search}`);
	return response.data.data; // pastikan ini
};

// Approve user
export const approveUser = async (userId: string) => {
	try {
		const response = await api.patch(`/users/${userId}/approve`, null, {
			headers: {
				Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
			},
		});
		return response.data;
	} catch (error) {
		console.error(`Failed to approve user ${userId}:`, error);
		throw error;
	}
};


// Reject user
export const rejectUser = async (userId: string) => {
	try {
		const response = await api.patch(`/users/${userId}/reject`, null, {
			headers: {
				Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
			},
		});
		return response.data;
	} catch (error) {
		console.error(`Failed to reject user ${userId}:`, error);
		throw error;
	}
};

// Delete user
export const deleteUser = async (userId: string) => {
	try {
		const response = await api.delete(`/users/${userId}`, {
			headers: {
				Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
			},
		});
		return response.data;
	} catch (error) {
		console.error(`Failed to delete user ${userId}:`, error);
		throw error;
	}
};


// Update user
export const updateUser = async (userId: string, payload: object) => {
	try {
		const response = await api.put(`/users/${userId}`, payload);
		return response.data;
	} catch (error) {
		console.error(`Failed to update user ${userId}:`, error);
		throw error;
	}
};

// Reset user password (opsional)
export const resetUserPassword = async (userId: string) => {
	try {
		const response = await api.post(`/users/${userId}/reset-password`);
		return response.data;
	} catch (error) {
		console.error(`Failed to reset password for user ${userId}:`, error);
		throw error;
	}
};
