import { NextFunction, Request, Response, RequestHandler } from 'express'; // Import RequestHandler
import { getAllUsersService, getUserProfileService } from './user.service';
import { repo } from './user.repo'; // Import the repo which now uses Sequelize

export const getUserProfileController: RequestHandler = async ( // Added RequestHandler type
    req,
    res,
    next,
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

export const getAllUsersController: RequestHandler = async (req, res, next): Promise<void> => { // Added RequestHandler type
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

export const approveUser: RequestHandler = async (req, res) => { // Added RequestHandler type
    try {
        const userId = req.params.id;
        const [affectedRows] = await repo.approveUser(userId); // Use repo method
        if (affectedRows === 0) {
            res.status(404).json({ message: 'User not found or already approved' });
            return; // Explicitly return void
        }
        res.status(200).json({ message: 'User approved successfully' });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Failed to approve user', error });
    }
};

export const rejectUser: RequestHandler = async (req, res) => { // Added RequestHandler type
    try {
        const userId = req.params.id;
        const deletedRows = await repo.rejectUser(userId); // Use repo method
        if (deletedRows === 0) {
            res.status(404).json({ message: 'User not found' });
            return; // Explicitly return void
        }
        res.status(200).json({ message: 'User rejected and deleted successfully' });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Failed to reject (delete) user', error });
    }
};

export const createUser: RequestHandler = async (req, res) => { // Added RequestHandler type
    try {
        const user = await repo.createUser(req.body); // Use repo method
        res.status(201).json({ message: 'User created successfully', data: user });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Failed to create user', error });
    }
};

export const updateUser: RequestHandler = async (req, res) => { // Added RequestHandler type
    try {
        const userId = req.params.id;
        // Sequelize update returns [affectedRows], not the updated user object directly
        const [affectedRows] = await repo.updateUser(userId, req.body); // Use repo method
        if (affectedRows === 0) {
            res.status(404).json({ message: 'User not found or no changes made' });
            return; // Explicitly return void
        }
        // To return the updated user, you'd typically fetch it after the update
        const updatedUser = await repo.getUserProfile(userId); // Fetch the updated user
        res.status(200).json({ message: 'User updated successfully', data: updatedUser });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Failed to update user', error });
    }
};

export const deleteUser: RequestHandler = async (req, res) => { // Added RequestHandler type
    try {
        const userId = req.params.id;
        const deletedRows = await repo.deleteUser(userId); // Use repo method
        if (deletedRows === 0) {
            res.status(404).json({ message: 'User not found' });
            return; // Explicitly return void
        }
        res.status(200).json({ message: 'User deleted successfully' });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Failed to delete user', error });
    }
};
