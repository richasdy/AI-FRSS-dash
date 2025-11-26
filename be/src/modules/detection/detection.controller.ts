import { NextFunction, Request, Response } from 'express';
import { DetectionService } from './detection.service';

export class DetectionController {
    public detection = new DetectionService();

    public getDetections = async (
        req: Request,
        res: Response,
        next: NextFunction,
    ): Promise<void> => {
        try {
            const limit = req.query.limit ? Number(req.query.limit) : 100;
            const detections = await this.detection.findAllDetections(limit);
            res.status(200).json({ data: detections, message: 'findAll' });
        } catch (error) {
            next(error);
        }
    };

    public createDetection = async (
        req: Request,
        res: Response,
        next: NextFunction,
    ): Promise<void> => {
        try {
            const detectionData = req.body;
            // Add server-side timestamp if not provided
            if (!detectionData.timestamp) {
                detectionData.timestamp = new Date();
            }
            const createDetectionData = await this.detection.createDetection(detectionData);
            res.status(201).json({ data: createDetectionData, message: 'created' });
        } catch (error) {
            next(error);
        }
    };
}
