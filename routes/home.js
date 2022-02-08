const express = require('express');
const router = express.Router();
const data = require('../data');
const homeData = data.home;

router.get('/start', (req, res) => {
  try {
    const distance = res.app.get('distance');
    const hours = res.app.get('hours');
    const minutes = res.app.get('minutes');
    const seconds = res.app.get('seconds');
    const totalSeconds = res.app.get('totalSeconds');
    const speed = res.app.get('speed');

    const {spawn} = require('child_process');
    const pythonProcess = spawn('python', ['newlights.py', distance, hours, minutes, seconds, totalSeconds, speed]);
    pythonProcess.stdout.on('data', function (data) {
      res.status(200).send(data.toString());
    });
  } catch (e) {
    res.status(500).render('error', {
      title: 'Error', 
      error: e
    });
  }
});

router.get('/', async (req, res) => {
  const distance = res.app.get('distance');
  const hours = res.app.get('hours');
  const minutes = res.app.get('minutes');
  const seconds = res.app.get('seconds');
  const speed = res.app.get('speed');
  try {
    res.render('home', {
      title: 'TrackRabbit',
      distance: distance,
      hours: hours,
      minutes: minutes,
      seconds: seconds,
      speed: speed
    });
  } catch (e) {
    res.status(500).render('error', {
      title: 'Error', 
      error: e
    });
  }
});

router.post('/', async (req, res) => {
  let distance = res.app.get('distance');
  let hours = res.app.get('hours');
  let minutes = res.app.get('minutes');
  let seconds = res.app.get('seconds');
  let speed = res.app.get('speed');

  const speedInfo = req.body;
  speedInfo.distance = parseInt(speedInfo.distance);
  if(typeof speedInfo.distance !== 'number' || isNaN(speedInfo.distance) || speedInfo.distance < 0) {
    res.status(400).render('home', {
      title: 'TrackRabbit',
      speedInfo: speedInfo,
      distance: distance,
      hours: hours,
      minutes: minutes,
      seconds: seconds,
      speed: speed,
      error: 'Error: Distance must be a number greater than or equal to 0.'
    });
    return;
  }
  if(speedInfo.hours === '') speedInfo.hours = '0';
  speedInfo.hours = parseInt(speedInfo.hours);
  if(typeof speedInfo.hours !== 'number' || isNaN(speedInfo.hours) || speedInfo.hours < 0) {
    res.status(400).render('home', {
      title: 'TrackRabbit',
      speedInfo: speedInfo,
      distance: distance,
      hours: hours,
      minutes: minutes,
      seconds: seconds,
      speed: speed,
      error: 'Error: Hours must be a number greater than or equal to 0.'
    });
    return;
  }
  if(speedInfo.minutes === '') speedInfo.minutes = '0';
  speedInfo.minutes = parseInt(speedInfo.minutes);
  if(typeof speedInfo.minutes !== 'number' || isNaN(speedInfo.minutes) || speedInfo.minutes < 0) {
    res.status(400).render('home', {
      title: 'TrackRabbit',
      speedInfo: speedInfo,
      distance: distance,
      hours: hours,
      minutes: minutes,
      seconds: seconds,
      speed: speed,
      error: 'Error: Minutes must be a number greater than or equal to 0.'
    });
    return;
  }
  if(speedInfo.seconds === '') speedInfo.seconds = '0';
  speedInfo.seconds = parseInt(speedInfo.seconds);
  if(typeof speedInfo.seconds !== 'number' || isNaN(speedInfo.seconds) || speedInfo.seconds < 0) {
    res.status(400).render('home', {
      title: 'TrackRabbit',
      speedInfo: speedInfo,
      distance: distance,
      hours: hours,
      minutes: minutes,
      seconds: seconds,
      speed: speed,
      error: 'Error: Seconds must be a number greater than or equal to 0.'
    });
    return;
  }
  const totalSeconds = speedInfo.hours*3600 + speedInfo.minutes*60 + speedInfo.seconds;
  if(totalSeconds === 0) {
    res.status(400).render('home', {
      title: 'TrackRabbit',
      speedInfo: speedInfo,
      distance: distance,
      hours: hours,
      minutes: minutes,
      seconds: seconds,
      speed: speed,
      error: 'Error: Time must be a number greater than 0.'
    });
    return;
  }
  try {
    speed = homeData.calculateSpeed(speedInfo.distance, speedInfo.hours, speedInfo.minutes, speedInfo.seconds);
    res.app.set('distance', speedInfo.distance);
    res.app.set('hours', speedInfo.hours);
    res.app.set('minutes', speedInfo.minutes);
    res.app.set('seconds', speedInfo.seconds);
    res.app.set('totalSeconds', totalSeconds);
    res.app.set('speed', speed);
    distance = res.app.get('distance');
    hours = res.app.get('hours');
    minutes = res.app.get('minutes');
    seconds = res.app.get('seconds');
    res.status(200).render('home', {
      title: 'TrackRabbit',
      speedInfo: speedInfo,
      distance: distance,
      hours: hours,
      minutes: minutes,
      seconds: seconds,
      speed: speed
    });
  } catch (e) {
    res.status(500).render('error', {
      title: 'Error', 
      error: e
    });
  }
});

router.get('/json', async (req, res) => {
  try {
    const distance = res.app.get('distance');
    const hours = res.app.get('hours');
    const minutes = res.app.get('minutes');
    const seconds = res.app.get('seconds');
    const totalSeconds = res.app.get('totalSeconds');
    const speed = res.app.get('speed');
    res.status(200).json({
      distance: distance,
      hours: hours,
      minutes: minutes,
      seconds: seconds,
      totalSeconds: totalSeconds,
      speed: speed
    });
  } catch (e) {
    res.status(500).render('error', {
      title: 'Error', 
      error: e
    });
  }
});

module.exports = router;