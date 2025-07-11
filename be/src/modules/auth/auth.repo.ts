import { DB } from '@/database';
import type { User, UserCreationData } from '@/interfaces/user.interfaces';

const repo = {
    findUserByEmail: async (email: string): Promise<User | null> => {
        return await DB.Users.findOne({ where: { email } });
    },
      
    createUser: async (userData: UserCreationData): Promise<User> => {
        return await DB.Users.create({
            ...userData,
            isApproved: false // default jika belum diset
        } as any);
    },    
};

export default repo;
