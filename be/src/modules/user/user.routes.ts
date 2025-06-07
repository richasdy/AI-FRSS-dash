import express from 'express';
import { getAllUsersController, getUserProfileController } from './user.controller';
import { authMiddleware } from '@/middlewares/auth.middleware';

const userRouter = express.Router();

userRouter.get('/', authMiddleware, getAllUsersController)
userRouter.get('/profile', authMiddleware, getUserProfileController);

export default userRouter;
