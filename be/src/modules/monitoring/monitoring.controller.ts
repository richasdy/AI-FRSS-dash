import { Router } from 'express';
import { getMonitoringFeedsFromDB, getStreamsFromDB, getLiveAlertsFromDB, getAllCamerasFromDB } from './monitoring.service';

const router = Router();

router.get('/', async (req, res) => {
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

router.get('/cameras', async (req, res) => {
    try {
        const { search, locationFilter, statusFilter } = req.query;
        const data = await getAllCamerasFromDB(
            search as string,
            locationFilter as string,
            statusFilter as 'Online' | 'Offline' | ''
        );
        res.json({ data });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

export default router;
