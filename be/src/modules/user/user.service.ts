import { repo } from './user.repo';
import { CustomError } from '@/utils/custom-error';
import { verifyJWT } from '@/middlewares/jwt.service';
import { JWT_ACCESS_TOKEN_SECRET } from '@/config';
import type { User } from '../../interfaces/user.interfaces';

export const getUserProfileService = async (accessToken: string): Promise<User> => {
    const decodeToken = await verifyJWT(
        accessToken,
        JWT_ACCESS_TOKEN_SECRET as string,
    );

    const userId = decodeToken.userId;

    const user = await repo.getUserProfile(userId);
    if (!user) {
        throw new CustomError('User not found', 404);
    }

    return user;
};

export const getAllUsersService = async (
    accessToken: string,
    search: string = '',
    roleFilter: string = '',
    statusFilter: 'Online' | 'Offline' | '' = '',
    approvalFilter: 'Approved' | 'Pending' | '' = ''
): Promise<User[]> => {
    await verifyJWT(
        accessToken,
        JWT_ACCESS_TOKEN_SECRET as string,
    );

    const users = await repo.getAllUsers(search, roleFilter, statusFilter, approvalFilter);

    return users;
};

