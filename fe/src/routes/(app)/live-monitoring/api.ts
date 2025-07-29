import { api } from "$lib/axios";
import type { MonitoringDummy } from '@/routes/(app)/live-monitoring/types';

export const getMonitoringFeeds = async (): Promise<MonitoringDummy[]> => {
  const res = await api.get('/monitoring'); 
  return res.data;
};

export const getLiveAlerts = async () => {
  const res = await api.get('/alerts/live'); 
  return res.data;
};

export const getAllStream = async (): Promise<string[]> => {
    const res = await api.get('/monitoring/streams'); 
    return res.data;
  };
