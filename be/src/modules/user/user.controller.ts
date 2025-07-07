import { NextFunction, Request, Response } from 'express';
import { getAllUsersService, getUserProfileService } from './user.service';
import prisma from '@/lib/prisma';

export const getUserProfileController = async (
  req: Request,
  res: Response,
  next: NextFunction,
): Promise<void> => {
  try {
    const authorization = req.headers.authorization;
    if (!authorization) {
      res.status(404).json({ message: 'User not found' });
      return;
    }

    const accessToken = authorization.split(' ')[1];
    const response = await getUserProfileService(accessToken);

    res.status(200).json({ message: 'User data fetched', data: response });
  } catch (error) {
    next(error);
  }
};

export const getAllUsersController = async (req: Request, res: Response, next: NextFunction): Promise<void> => {
  try {
    const search = req.query.search;
    const authorization = req.headers.authorization;

    console.log('Search:', search);
    console.log('Authorization:', authorization);

    if (!authorization) {
      res.status(404).json({ message: 'Users not found' });
      return;
    }

    const accessToken = authorization.split(' ')[1];
    console.log('Access token:', accessToken);

    const response = await getAllUsersService(accessToken, search as string);
    console.log('Response data:', response);

    res.status(200).json({ message: 'User data fetched', data: response });
  } catch (error) {
    console.error('getAllUsersController error:', error);
    next(error);
  }
};



export const approveUser = async (req: Request, res: Response) => {
  try {
    const userId = req.params.id;
    await prisma.user.update({
      where: { id: userId },
      data: { isApproved: true },
    });
    res.status(200).json({ message: 'User approved successfully' });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Failed to approve user', error });
  }
};

export const rejectUser = async (req: Request, res: Response) => {
  try {
    const userId = req.params.id;
    await prisma.user.delete({
      where: { id: userId },
    });
    res.status(200).json({ message: 'User rejected and deleted successfully' });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Failed to reject (delete) user', error });
  }
};


export const createUser = async (req: Request, res: Response) => {
  try {
    const user = await prisma.user.create({ data: req.body });
    res.status(201).json({ message: 'User created successfully', data: user });
  } catch (error) {
    res.status(500).json({ message: 'Failed to create user', error });
  }
};

export const updateUser = async (req: Request, res: Response) => {
  try {
    const userId = req.params.id;
    const updatedUser = await prisma.user.update({
      where: { id: userId },
      data: req.body,
    });
    res.status(200).json({ message: 'User updated successfully', data: updatedUser });
  } catch (error) {
    res.status(500).json({ message: 'Failed to update user', error });
  }
};

export const deleteUser = async (req: Request, res: Response) => {
  try {
    const userId = req.params.id;
    await prisma.user.delete({ where: { id: userId } });
    res.status(200).json({ message: 'User deleted successfully' });
  } catch (error) {
    res.status(500).json({ message: 'Failed to delete user', error });
  }
};
