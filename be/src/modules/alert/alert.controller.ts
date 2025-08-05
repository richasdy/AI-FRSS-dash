import { Router } from 'express';
import { getLiveAlertsFromDB } from './alert.service'; 

const router = Router();

router.get('/live', async (req, res) => {
    try {
        const alerts = await getLiveAlertsFromDB();
        res.json({ data: alerts }); 
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

export default router;
