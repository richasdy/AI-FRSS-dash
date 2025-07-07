import express from 'express';
import { 
  getAllUsersController, 
  getUserProfileController,
  createUser,
  updateUser,
  deleteUser,
  approveUser,
  rejectUser
} from './user.controller';
import { authMiddleware } from '@/middlewares/auth.middleware';

const userRouter = express.Router();

userRouter.get('/', authMiddleware, getAllUsersController);
userRouter.get('/profile', authMiddleware, getUserProfileController);

userRouter.post('/', createUser);
userRouter.put('/:id', updateUser);
userRouter.delete('/:id', deleteUser);
userRouter.patch('/:id/approve', approveUser);
userRouter.patch('/:id/reject', rejectUser);

export default userRouter;
