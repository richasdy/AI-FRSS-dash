import { DB } from '@/database';
import { User } from '@/interfaces/user.interfaces';

export const repo = {
    getUserProfile: async (
        userId: string | undefined,
    ): Promise<User | null> => {
        return await DB.Users.findOne({ where: { id: userId } });
    },

    getAllUsers: async (search: string): Promise<User[]> => {
        let users =  await DB.Users.findAll({
            where: {
                name: {
                    [DB.Sequelize.Op.like]: `%${search ?? ''}%`
                }
            },
        });

        return users;
    }
};
