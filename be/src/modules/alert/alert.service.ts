import { DB } from '@/database'; 

export const getLiveAlertsFromDB = async () => {
    return DB.Alerts.findAll({
        where: { isResolved: false }, 
        order: [['createdAt', 'DESC']], 
        limit: 10
    });
};
