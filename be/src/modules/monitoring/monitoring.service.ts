import { DB } from '@/database';
import { Op } from 'sequelize';
import type { MonitoringAttributes } from '@/database/models/monitoring.model';

export const getMonitoringFeedsFromDB = async () => {
    return DB.Monitoring.findAll(); 
};

export const getAllCamerasFromDB = async (
    search: string = '',
    locationFilter: string = '',
    statusFilter: 'Online' | 'Offline' | '' = ''
) => {
    let whereCondition: any = {};

    if (search && search.trim() !== '') {
        whereCondition[Op.or] = [
            { name: { [Op.iLike]: `%${search.trim()}%` } },
            { location: { [Op.iLike]: `%${search.trim()}%` } },
            { ipAddress: { [Op.iLike]: `%${search.trim()}%` } },
        ];
    }

    if (locationFilter && locationFilter.trim() !== '') {
        whereCondition.location = locationFilter.trim();
    }

    if (statusFilter) {
        whereCondition.isOnline = statusFilter === 'Online';
    }

    return DB.Monitoring.findAll({
        where: whereCondition,
        order: [['lastUpdated', 'DESC']],
    });
};

export const getStreamsFromDB = async () => {
    const rows = await DB.Monitoring.findAll({ attributes: ['streamUrl'] }); 
    return rows.map((r: { streamUrl: string }) => r.streamUrl); 
};

export const getLiveAlertsFromDB = async () => {
    return DB.Alerts.findAll({
        where: { isResolved: false },
        order: [['createdAt', 'DESC']],
        limit: 10
    });
};
