const { config } = require('dotenv');
config({ path: `.env.${process.env.NODE_ENV || 'development'}` });

const {
  DB_PORT,
  DB_USERNAME,
  DB_PASSWORD,
  DB_NAME,
  DB_HOST,
  DB_DIALECT,
} = process.env;

module.exports = {
  username: DB_USERNAME || 'root',
  password: DB_PASSWORD || '',
  database: DB_NAME || 'sv-fs',
  host: DB_HOST || '127.0.0.1',
  port: DB_PORT || 3306,
  dialect: DB_DIALECT || 'mysql',
  migrationStorageTableName: 'sequelize_migrations',
  seederStorageTableName: 'sequelize_seeds',
};
