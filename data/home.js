function calculateSpeed(distance, hours, minutes, seconds) {
    if(typeof distance !== 'number' || isNaN(distance) || distance < 0) {
        throw new Error('Parameter 1 [distance] must be a number greater than or equal to 0.');
    }
    if(typeof hours !== 'number' || isNaN(hours) || hours < 0) {
        throw new Error('Parameter 2 [hours] must be a number greater than or equal to 0.');
    }
    if(typeof minutes !== 'number' || isNaN(minutes) || minutes < 0) {
        throw new Error('Parameter 3 [minutes] must be a number greater than or equal to 0.');
    }
    if(typeof seconds !== 'number' || isNaN(seconds) || seconds < 0) {
        throw new Error('Parameter 4 [seconds] must be a number greater than or equal to 0.');
    }
    const totalSeconds = hours*3600 + minutes*60 + seconds;
    if(totalSeconds === 0) throw new Error('Time must be a number greater than 0.');    
    return distance / totalSeconds;
}

module.exports = {
    calculateSpeed
};