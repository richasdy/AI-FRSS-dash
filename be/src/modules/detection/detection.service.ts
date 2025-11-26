import { DetectionRepository } from './detection.repo';
import { Detection } from '@/interfaces/detection.interfaces';

export class DetectionService {
    public detectionRepository = new DetectionRepository();

    public async findAllDetections(limit?: number): Promise<Detection[]> {
        const detections = await this.detectionRepository.findAll(limit);
        return detections;
    }

    public async createDetection(detectionData: Partial<Detection>): Promise<Detection> {
        const createDetectionData = await this.detectionRepository.create(detectionData);
        return createDetectionData;
    }
}
