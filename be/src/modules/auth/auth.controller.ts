import { NextFunction, Request, Response } from 'express';
import { signInService, signUpService } from './auth.service';
import { DB } from '@/database/index';


export const signUpController = async (
    req: Request,
    res: Response,
    next: NextFunction,
): Promise<void> => {
    try {
        const userData = req.body;
        const response = await signUpService(userData);

        res.status(201).json({
            message: 'Successfully signed up',
            data: response.user,
        });
    } catch (error) {
        next(error);
    }
};

export const signInController = async (
    req: Request,
    res: Response,
    next: NextFunction,
): Promise<void> => {
    try {
        const userData = req.body;
        const response = await signInService(userData);

        res.status(200).json({
            message: 'Successfully signed in',
            data: response,
        });
    } catch (error) {
        next(error);
    }
};

export const register = async (req: Request, res: Response) => {
    try {
      const { email, name, username, password } = req.body;
      const user = await DB.Users.create({
            email,
            name,
            username,
            password,
            isApproved: false,
          } as any);
          
      res.status(201).json({ message: 'User created successfully', data: user });
    } catch (error) {
      res.status(500).json({ message: 'Failed to create user', error });
    }
  };