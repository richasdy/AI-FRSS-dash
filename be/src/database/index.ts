import { Sequelize } from 'sequelize';
import logger from '@/utils/logger';
import userModel from './models/user.model';
import {
    DB_DIALECT,
    DB_HOST,
    DB_NAME,
    DB_PASSWORD,
    DB_PORT,
    DB_USERNAME,
    NODE_ENV,
} from '@/config';

const sequelize = new Sequelize(
    DB_NAME as string,
    DB_USERNAME as string,
    DB_PASSWORD,
    {
        dialect: (DB_DIALECT as any) || 'mysql', // ✅ fix di sini
        host: DB_HOST,
        port: parseInt(DB_PORT as string, 10),
        timezone: '+09:00',
        define: {
            charset: 'utf8mb4',
            collate: 'utf8mb4_general_ci',
            underscored: true,
            freezeTableName: true,
        },
        pool: {
            min: 0,
            max: 5,
        },
        logQueryParameters: NODE_ENV === 'development',
        logging: (query, time) => {
            logger.info(`${time}ms ${query}`);
        },
        benchmark: true,
    },
);

(async () => {
    try {
        await sequelize.authenticate();
        logger.info('Database connection established ✅');
    } catch (error) {
        logger.error('Unable to connect to the database ❌', error);
    }
})();

export const DB = {
    Users: userModel(sequelize),
    sequelize,
    Sequelize,
};
