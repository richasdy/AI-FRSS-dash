import { Router } from 'express';
import { getMonitoringFeedsFromDB, getStreamsFromDB, getLiveAlertsFromDB, getRecordingListFromDB } from '../monitoring/monitoring.service';

import path from 'path';

const router = Router();

router.get('/feeds', async (req, res) => {
    try {
        const data = await getMonitoringFeedsFromDB();
        res.json({ data });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

router.get('/streams', async (req, res) => {
    try {
        const streams = await getStreamsFromDB();
        res.json({ data: streams });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

router.get('/alerts/live', async (req, res) => {
    try {
        const alerts = await getLiveAlertsFromDB();
        res.json({ data: alerts });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

router.get('/recordings', async (req, res) => {
    try {
        const { personName, cameraName, date } = req.query;
        const data = await getRecordingListFromDB(
            personName as string,
            cameraName as string,
            date ? new Date(date as string) : null
        );
        res.json({ data });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

router.get('/recordings/files/:filename', (req, res) => {
    const filename = req.params.filename;
    const filePath = path.join(__dirname, '../../../uploads', filename);
    res.sendFile(filePath, (err) => {
        if (err) {
            console.error('Failed to send file:', err);
            res.status(404).send('File not found.');
        }
    });
});

export default router;
