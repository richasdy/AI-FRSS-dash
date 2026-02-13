export interface Detection {
    id: string;
    imagePath: string;
    timestamp: Date;
    cameraId: string;
    confidence: number;
    box: string; // JSON string of the bounding box
    phash: string;
    createdAt?: Date;
    updatedAt?: Date;
}
