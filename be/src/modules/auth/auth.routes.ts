import express from 'express';
import { signInController, signUpController, register } from './auth.controller';


const authRouter = express.Router();

authRouter.post('/signup', signUpController);
authRouter.post('/signin', signInController);
authRouter.post('/register', register);

export default authRouter;
