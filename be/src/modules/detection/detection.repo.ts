import { DB } from '@/database';
import { Detection } from '@/interfaces/detection.interfaces';
import { DetectionModel } from '@/database/models/detection.model';

export class DetectionRepository {
    public async findAll(limit: number = 100): Promise<DetectionModel[]> {
        return await DB.Detections.findAll({
            limit,
            order: [['created_at', 'DESC']],
        });
    }

    public async create(data: Partial<Detection>): Promise<DetectionModel> {
        return await DB.Detections.create(data as any);
    }
}
