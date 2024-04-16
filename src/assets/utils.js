window.dccFunctions = window.dccFunctions || {};
window.dccFunctions.ordinalToDateStr = function(ordinal) {
    // Calculate the year
    let year = Math.floor((ordinal - 1) / 365.2425) + 1;

    // Calculate the day within the year
    const dayOfYear = ordinal - ((year - 1) * 365 + Math.floor((year - 1) / 4) - Math.floor((year - 1) / 100) + Math.floor((year - 1) / 400));

    // Determine if it's a leap year
    const isLeapYear = (year % 4 === 0 && year % 100 !== 0) || (year % 400 === 0);

    // Define months and their respective days
    const months = [31, isLeapYear ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];

    // Calculate the month and day within the month
    let month;
    let dayOfMonth = dayOfYear;
    for (month = 0; month < 12; month++) {
        const daysInMonth = months[month];
        if (dayOfMonth <= daysInMonth) {
            break;
        }
        dayOfMonth -= daysInMonth;
    }
    if (month === 12) {
        month = 0;
        year++;
    }
    return `${year}-${month + 1}-${dayOfMonth}`
}
