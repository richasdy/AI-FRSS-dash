export const getLiveData = async () => {
    return {
      timestamp: new Date(),
      status: 'ok',
      activeUsers: 5,
    };
  };
  