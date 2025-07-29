import { Router } from 'express';
import { getLiveData } from './monitoring.service';

const router = Router();

router.get('/live', async (req, res) => {
  try {
    const data = await getLiveData();
    res.json(data);
  } catch (err) {
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

router.get('/streams', (req, res) => {
	const streams = [
        'http://185.97.122.128:80/cgi-bin/faststream.jpg?stream=half&fps=15&rand=COUNTER',
		'http://85.220.149.7:80/cgi-bin/faststream.jpg?stream=half&;fps=15&;rand=COUNTER',
		'http://80.151.142.110:8080/?action=stream',
		'http://87.139.153.80:80/cgi-bin/faststream.jpg?stream=half&;fps=15&;rand=COUNTER',
		'http://37.182.240.202:82/cgi-bin/faststream.jpg?stream=half&;fps=15&;rand=COUNTER',
		'http://91.113.207.170:80/cgi-bin/faststream.jpg?stream=half&;fps=15&;rand=COUNTER',
		'http://86.121.159.16:80/cgi-bin/faststream.jpg?stream=half&;fps=15&;rand=COUNTER',
		'http://151.14.98.27:80/jpgmulreq/1/image.jpg?key=1516975535684&;lq=1&;1752166261',
		'http://77.89.48.24:89/cgi-bin/faststream.jpg?stream=half&;fps=15&;rand=COUNTER',
		'http://82.187.186.77:80/cgi-bin/faststream.jpg?stream=half&;fps=15&;rand=COUNTER'
	];

	res.json(streams);
});

export default router;
