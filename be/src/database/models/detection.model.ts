
import { Detection } from '@/interfaces/detection.interfaces';
import { Sequelize, DataTypes, Model, Optional } from 'sequelize';

export type DetectionCreationAttributes = Optional<Detection, 'id' | 'createdAt' | 'updatedAt'>;

export class DetectionModel
    extends Model<Detection, DetectionCreationAttributes>
    implements Detection
{
    public id!: string;
    public imagePath!: string;
    public timestamp!: Date;
    public cameraId!: string;
    public confidence!: number;
    public box!: string;
    public phash!: string;

    public readonly createdAt!: Date;
    public readonly updatedAt!: Date;
}

export default function (sequelize: Sequelize): typeof DetectionModel {
    DetectionModel.init(
        {
            id: {
                primaryKey: true,
                type: DataTypes.UUID,
                defaultValue: DataTypes.UUIDV4,
            },
            imagePath: {
                allowNull: false,
                type: DataTypes.STRING,
                field: 'image_path',
            },
            timestamp: {
                allowNull: false,
                type: DataTypes.DATE,
            },
            cameraId: {
                allowNull: false,
                type: DataTypes.STRING,
                field: 'camera_id',
            },
            confidence: {
                allowNull: false,
                type: DataTypes.FLOAT,
            },
            box: {
                allowNull: false,
                type: DataTypes.TEXT, // JSON string
            },
            phash: {
                allowNull: false,
                type: DataTypes.STRING,
            },
        },
        {
            tableName: 'detections',
            sequelize,
            timestamps: true,
            createdAt: 'created_at',
            updatedAt: 'updated_at',
        },
    );

    return DetectionModel;
}
