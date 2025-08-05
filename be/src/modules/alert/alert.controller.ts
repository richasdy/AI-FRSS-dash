import { Router } from 'express';
import { getLiveAlertsFromDB, getAlertHistoryFromDB } from './alert.service'; 

const router = Router();

// Endpoint untuk mendapatkan semua live alerts
router.get('/live', async (req, res) => {
    try {
        const data = await getLiveAlertsFromDB();
        res.json({ data });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

// Endpoint baru untuk mendapatkan riwayat alert dengan filter
router.get('/history', async (req, res) => {
    try {
        const { typeFilter, locationFilter, dateRangeFilter } = req.query;

        const data = await getAlertHistoryFromDB(
            typeFilter as string,
            locationFilter as string,
            dateRangeFilter as string
        );
        res.json({ data });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

export default router;
