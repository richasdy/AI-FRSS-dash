import authRouter from '@/modules/auth/auth.routes';
import userRouter from '@/modules/user/user.routes';
import roleRouter from '@/modules/role/role.routes';
import express from 'express';

const router = express.Router();

router.use('/auth', authRouter);
router.use('/users', userRouter);
router.use('/roles', roleRouter);

export default router;
