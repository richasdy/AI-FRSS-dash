import axios from 'axios';

export const api = axios.create({
	baseURL: 'http://18.217.159.63:3000/api'
});

api.interceptors.request.use(
	(config) => {
		const token = localStorage.getItem('accessToken');
		if (token) {
			config.headers['Authorization'] = token;
		}
		// 💥 Tambahkan header anti cache
		config.headers['Cache-Control'] = 'no-cache';
		config.headers['Pragma'] = 'no-cache';
		config.headers['If-Modified-Since'] = '0';

		return config;
	},
	(error) => {
		localStorage.removeItem('accessToken');
		window.location.href = '/signin';
		return Promise.reject(error);
	}
);
