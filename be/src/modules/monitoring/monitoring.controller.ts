import { Router } from 'express';
import { getMonitoringFeedsFromDB, getStreamsFromDB } from './monitoring.service'; 

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

export default router;
