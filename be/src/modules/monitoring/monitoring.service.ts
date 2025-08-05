import { DB } from '@/database'; 
import type { MonitoringAttributes } from '@/database/models/monitoring.model';

export const getMonitoringFeedsFromDB = async () => {
    return DB.Monitoring.findAll();
};

export const getStreamsFromDB = async () => {
    const rows = await DB.Monitoring.findAll({ attributes: ['streamUrl'] }); 
    return rows.map((r: { streamUrl: string }) => r.streamUrl);
};


