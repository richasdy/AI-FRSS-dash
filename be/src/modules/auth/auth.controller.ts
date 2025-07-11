import { NextFunction, Request, Response } from 'express';
import { signInService, signUpService } from './auth.service';
import { DB } from '@/database/index';
import bcrypt from 'bcrypt';  // Pastikan sudah install bcrypt

export const signUpController = async (
    req: Request,
    res: Response,
    next: NextFunction
): Promise<void> => {
    try {
        const userData = req.body;
        const response = await signUpService(userData);

        res.status(201).json({
            message: 'Successfully signed up',
            data: response.user,
        });
    } catch (error) {
        console.error('Error in signUpController:', error);
        next(error);
    }
};

export const signInController = async (
    req: Request,
    res: Response,
    next: NextFunction
): Promise<void> => {
    try {
        const userData = req.body;
        const response = await signInService(userData);

        res.status(200).json({
            message: 'Successfully signed in',
            data: response,
        });
    } catch (error) {
        console.error('Error in signInController:', error);
        next(error);
    }
};

export const register = async (req: Request, res: Response) => {
    try {
        const { email, name, username, password } = req.body;

        // Pastikan password di-hash
        const hashedPassword = await bcrypt.hash(password, 10);

        const user = await DB.Users.create({
            email,
            name,
            username,
            password: hashedPassword,
            isApproved: false,
            created_at: new Date(),
            updated_at: new Date(),
        });

        res.status(201).json({ message: 'User created successfully', data: user });
    } catch (error) {
        console.error('Error in register:', error);

        // Convert error to Error type
        const errorMessage = error instanceof Error ? error.message : String(error);

        res.status(500).json({ message: 'Failed to create user', error: errorMessage });
    }
};
