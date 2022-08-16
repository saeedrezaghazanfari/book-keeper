export default {

    get_time_from_iso(date_time, input) {
        if(input === 'date') {
            let date = new Date(date_time);
            let year = date.getFullYear();
            let month = date.getMonth()+1;
            let day = date.getDate();
            return `${year} - ${month} - ${day}` /* 2022 - 02 - 07 */
        } else if(input === 'time') {
            let date = new Date(date_time);
            let hour = date.getHours();
            let min = date.getMinutes();
            let sec = date.getSeconds();
            if (hour < 10) hour = `0${hour}`;
            if (min < 10) min = `0${min}`;
            if (sec < 10) sec = `0${sec}`;
            return `${hour} : ${min} : ${sec}`; /* 20 : 09 : 42 */
        }
    },

    fa_to_en(value){
        let text = value
        text = String(text)
        text = text.replace(/۰/g, "0")
        text = text.replace(/۱/g, "1")
        text = text.replace(/۲/g, "2")
        text = text.replace(/۳/g, "3")
        text = text.replace(/۴/g, "4")
        text = text.replace(/۵/g, "5")
        text = text.replace(/۶/g, "6")
        text = text.replace(/۷/g, "7")
        text = text.replace(/۸/g, "8")
        text = text.replace(/۹/g, "9")
        text = text.replace(/٤/g, "4")
        text = text.replace(/٥/g, "5")
        text = text.replace(/٦/g, "6")
        return text
    },

    en_to_fa(value){
        if (!value) return ""
        const persianDigits = "۰۱۲۳۴۵۶۷۸۹"
        const persianMap = persianDigits.split("")
        return value.replace(/\d/g, function (m) {
            return persianMap[parseInt(m)]
        })
    },

    digit(value, lang) {
        if (!value) return ""
        if (lang === 'fa') {
            const persianDigits = "۰۱۲۳۴۵۶۷۸۹"
            const persianMap = persianDigits.split("")
            return value.replace(/\d/g, function (m) {
                return persianMap[parseInt(m)]
            })
        } else {
            let text = value
            text = String(text)
            text = text.replace(/۰/g, "0")
            text = text.replace(/۱/g, "1")
            text = text.replace(/۲/g, "2")
            text = text.replace(/۳/g, "3")
            text = text.replace(/۴/g, "4")
            text = text.replace(/۵/g, "5")
            text = text.replace(/۶/g, "6")
            text = text.replace(/۷/g, "7")
            text = text.replace(/۸/g, "8")
            text = text.replace(/۹/g, "9")
            text = text.replace(/٤/g, "4")
            text = text.replace(/٥/g, "5")
            text = text.replace(/٦/g, "6")
            return text
        }
    }
}