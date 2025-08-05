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

    getAllUsers: async (
        search: string = '',
        roleFilter: string = '',
        statusFilter: 'Online' | 'Offline' | '' = '',
        approvalFilter: 'Approved' | 'Pending' | '' = ''
    ): Promise<User[]> => {
        let whereCondition: any = {};
        let includeOptions: any[] = [];

        const roleIncludeOption: any = {
            model: DB.Roles,
            as: 'role',
        };

        if (roleFilter && roleFilter.trim() !== '') {
            roleIncludeOption.where = {
                name: roleFilter.trim() 
            };
            roleIncludeOption.required = true; 
        }
        includeOptions.push(roleIncludeOption); 

        if (search && search.trim() !== '') {
            whereCondition[Op.or] = [
                { name: { [Op.iLike]: `%${search.trim()}%` } },
                { email: { [Op.iLike]: `%${search.trim()}%` } },
                { username: { [Op.iLike]: `%${search.trim()}%` } },
                { department: { [Op.iLike]: `%${search.trim()}%` } },
            ];
        }

        if (statusFilter) {
            whereCondition.isOnline = statusFilter === 'Online'; 
        }

        if (approvalFilter) {
            whereCondition.isApproved = approvalFilter === 'Approved'; 
        }
        console.log('--- Sequelize Query Debugging ---');
console.log('Final whereCondition:', JSON.stringify(whereCondition, null, 2));
console.log('Final includeOptions:', JSON.stringify(includeOptions, null, 2));
console.log('---------------------------------');

        const users = await DB.Users.findAll({
            where: whereCondition,
            include: includeOptions,
            order: [['created_at', 'DESC']] 
        });

        console.log('Sequelize users (filtered):', users.length, 'users found');


console.log('Sequelize raw users data (before toJSON):', users);
return users.map(user => user.toJSON() as User);
        return users.map(user => user.toJSON() as User);
    },

    approveUser: async (userId: string): Promise<[number]> => {
        return await DB.Users.update(
            { isApproved: true, updated_at: new Date() }, // Perbarui juga updated_at
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
        const createdUser = await DB.Users.create(dataToCreate);
        const userWithRole = await DB.Users.findByPk(createdUser.id, {
            include: [{ model: DB.Roles, as: 'role' }],
        });

        if (!userWithRole) {
            throw new Error('Failed to retrieve newly created user with role data.');
        }

        return userWithRole.toJSON();
    },

    updateUser: async (userId: string, userData: Partial<UserCreationData>): Promise<[number]> => {
        return await DB.Users.update(
            { ...userData, updated_at: new Date() }, 
            { where: { id: userId } }
        );
    },

    deleteUser: async (userId: string): Promise<number> => {
        return await DB.Users.destroy({ where: { id: userId } });
    },
};
