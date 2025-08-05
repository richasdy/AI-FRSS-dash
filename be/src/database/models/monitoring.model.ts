import { DataTypes, Sequelize, Model, Optional } from 'sequelize';

export interface MonitoringAttributes {
    id: number;
    name: string;
    isOnline: boolean; 
    streamUrl: string; 
    location: string;
    createdAt?: Date;
    updatedAt?: Date;
}

export type MonitoringCreationAttributes = Optional<MonitoringAttributes, 'id' | 'createdAt' | 'updatedAt'>;

export default (sequelize: Sequelize) => {
    class Monitoring extends Model<MonitoringAttributes, MonitoringCreationAttributes>
        implements MonitoringAttributes {
        public id!: number;
        public name!: string;
        public isOnline!: boolean;
        public streamUrl!: string;
        public location!: string;
        public createdAt?: Date;
        public updatedAt?: Date;
    }

    Monitoring.init(
        {
            id: {
                type: DataTypes.INTEGER,
                autoIncrement: true,
                primaryKey: true,
            },
            name: {
                type: DataTypes.STRING,
                allowNull: false,
            },
            isOnline: { 
                type: DataTypes.BOOLEAN,
                field: 'is_online', 
                allowNull: false,
            },
            streamUrl: { 
                type: DataTypes.STRING,
                field: 'stream_url', 
                allowNull: false,
            },
            location: {
                type: DataTypes.STRING,
                allowNull: true,
            },
        },
        {
            sequelize,
            tableName: 'monitoring_feeds', 
            timestamps: true, 
            createdAt: 'created_at', 
            updatedAt: 'updated_at', 
        }
    );

    return Monitoring;
};