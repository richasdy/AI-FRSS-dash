import { Router } from 'express';
import { DetectionController } from './detection.controller';

const detectionRouter = Router();
const detectionController = new DetectionController();

detectionRouter.get('/', detectionController.getDetections);
detectionRouter.post('/', detectionController.createDetection);

export default detectionRouter;
