import { DB } from '@/database';
import type { User, UserCreationData } from '@/interfaces/user.interfaces';
import { Op } from 'sequelize'; 

export const repo = {
    getUserProfile: async (userId: string | undefined): Promise<User | null> => {
        if (!userId) return null;
        const user = await DB.Users.findByPk(userId, {
            include: [{ model: DB.Roles, as: 'role' }], 
        });

        if (!user) return null;

        return user.toJSON() as User;
    },

    getAllUsers: async (search: string): Promise<User[]> => {
        let whereCondition: any = {};

        if (search && search.trim() !== '') {
            whereCondition = {
                [Op.or]: [ 
                    { name: { [Op.iLike]: `%${search.trim()}%` } },
                    { email: { [Op.iLike]: `%${search.trim()}%` } },
                    { username: { [Op.iLike]: `%${search.trim()}%` } }, 
                    { department: { [Op.iLike]: `%${search.trim()}%` } }, 
                ],
            };
        }

        const users = await DB.Users.findAll({
            where: whereCondition,
            include: [{ model: DB.Roles, as: 'role' }],
        });

        console.log('Sequelize users:', users);
        return users.map(user => user.toJSON() as User); 
    },

    approveUser: async (userId: string): Promise<[number]> => { 
        return await DB.Users.update(
            { isApproved: true },
            { where: { id: userId } }
        );
    },

    rejectUser: async (userId: string): Promise<number> => {
        return await DB.Users.destroy({ where: { id: userId } });
    },

    createUser: async (userData: UserCreationData): Promise<User> => {
        const dataToCreate = {
            ...userData,
            isApproved: userData.isApproved ?? false,
            isOnline: userData.isOnline ?? false,   
            lastLogin: userData.lastLogin || null,    
            department: userData.department || null,  
        };
        return await DB.Users.create(dataToCreate);
    },

    updateUser: async (userId: string, userData: Partial<UserCreationData>): Promise<[number]> => { 
        return await DB.Users.update(
            userData,
            { where: { id: userId } }
        );
    },

    deleteUser: async (userId: string): Promise<number> => {
        return await DB.Users.destroy({ where: { id: userId } });
    },
};
