import prisma from '@/lib/prisma';
import { User } from '@/interfaces/user.interfaces';

export const repo = {
  getUserProfile: async (userId: string | undefined): Promise<User | null> => {
    if (!userId) return null;

    const user = await prisma.user.findUnique({
      where: { id: userId },
    });

    if (!user) return null;

    const { createdAt, updatedAt, ...rest } = user;

    return {
      ...rest,
      created_at: createdAt,
      updated_at: updatedAt,
    };
  },

  getAllUsers: async (search: string): Promise<User[]> => {
    let whereCondition = {};

    if (search && search.trim() !== '') {
      whereCondition = {
        name: {
          not: null,
          contains: search,
          mode: 'insensitive',
        },
      };
    }

    const users = await prisma.user.findMany({
      where: whereCondition,
    });
    console.log('Prisma users:', users);
    return users.map(({ createdAt, updatedAt, ...rest }) => ({
      ...rest,
      created_at: createdAt,
      updated_at: updatedAt,
    }));
  },
};
