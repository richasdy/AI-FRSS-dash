// src/modules/user/user.repo.ts
import { DB } from '@/database'; // Import DB object which contains Sequelize models
import type { User, UserCreationData } from '@/interfaces/user.interfaces';
import { Op } from 'sequelize'; // Import Op for Sequelize operators

export const repo = {
    getUserProfile: async (userId: string | undefined): Promise<User | null> => {
        if (!userId) return null;
        // Use Sequelize's findByPk for finding by primary key (id)
        const user = await DB.Users.findByPk(userId);

        if (!user) return null;

        // Sequelize models return properties as defined in the model (e.g., created_at)
        // No need for manual mapping from createdAt to created_at if model is configured correctly
        return user.toJSON() as User; // Convert Sequelize instance to plain JSON object
    },

    getAllUsers: async (search: string): Promise<User[]> => {
        let whereCondition: any = {};

        if (search && search.trim() !== '') {
            whereCondition = {
                [Op.or]: [ // Use Op.or for OR conditions
                    { name: { [Op.iLike]: `%${search.trim()}%` } }, // Case-insensitive search for name
                    { email: { [Op.iLike]: `%${search.trim()}%` } }, // Case-insensitive search for email
                    { username: { [Op.iLike]: `%${search.trim()}%` } }, // Case-insensitive search for username
                ],
            };
        }

        // Use Sequelize's findAll with a WHERE clause for searching
        const users = await DB.Users.findAll({
            where: whereCondition,
        });

        console.log('Sequelize users:', users);
        // Sequelize models return properties as defined in the model (e.g., created_at)
        // No need for manual mapping from createdAt to created_at if model is configured correctly
        return users.map(user => user.toJSON() as User); // Convert each instance to plain JSON object
    },

    // New methods for user management using Sequelize
    approveUser: async (userId: string): Promise<[number]> => { // Changed return type to [number]
        // Update user's isApproved status
        return await DB.Users.update(
            { isApproved: true },
            { where: { id: userId } }
        );
    },

    rejectUser: async (userId: string): Promise<number> => {
        // Delete user
        return await DB.Users.destroy({ where: { id: userId } });
    },

    createUser: async (userData: UserCreationData): Promise<User> => {
        // Ensure isApproved is explicitly boolean, defaulting to false if undefined
        const dataToCreate = {
            ...userData,
            isApproved: userData.isApproved ?? false, // Provide a default if undefined
        };
        return await DB.Users.create(dataToCreate);
    },

    updateUser: async (userId: string, userData: Partial<UserCreationData>): Promise<[number]> => { // Changed return type to [number]
        // Update user data
        return await DB.Users.update(
            userData,
            { where: { id: userId } }
        );
    },

    deleteUser: async (userId: string): Promise<number> => {
        // Delete user
        return await DB.Users.destroy({ where: { id: userId } });
    },
};
