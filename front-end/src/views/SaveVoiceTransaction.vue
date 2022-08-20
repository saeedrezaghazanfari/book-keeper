<template>
    <div class="opacity-wrapper" :class="{'opacity-wrapper-ltr': $i18n.locale == 'en'}">
        
        <div class="wrapper-surement" v-if="show_surement">
            <p>{{ $t('If You are Ready to Register the Transaction, Click the Button Below') }}</p>
            <button @click="fire_progressive"><i class="ti-microphone-alt"></i></button>
        </div>

        <h4><i class="ti-marker-alt"></i> {{ $t('Transaction Registration') }}</h4>
        <form novalidate @submit.prevent="save_transaction">
            <div class="forminput-control">
                <input type="text" id="bank_name_field" ref="bank_name_field" v-model="transaction.bank_name" required disabled />
                <label for="bank_name_field">{{ $t('Bank Name') }} <i class="ti-microphone blink-animation d-none" ref="bank_name_field_mic"></i></label>
                <div class="after--forminput-control d-none" ref="suggestions1"></div>
            </div>
            <div class="wrapper-twofield">
                <div class="forminput-control">
                    <input v-model="transaction.price" type="number" id="price_field" ref="price_field" required disabled class="text-center">
                    <label for="price_field">{{ $t('Price') }} <i class="ti-microphone blink-animation d-none" ref="price_field_mic"></i></label>
                </div>
                <div class="forminput-control">
                    <input v-model="transaction.type" type="text" id="type_transaction_field" ref="type_transaction_field" required disabled />
                    <label for="type_transaction_field">{{ $t('Transaction Type') }} <i class="ti-microphone blink-animation d-none" ref="transaction_type_field_mic"></i></label>
                    <div class="after--forminput-control after--forminput-control-sm d-none" ref="suggestions2"></div>
                </div>
            </div>
            <div class="wrapper-date-time">
                <div>
                    <custom-date-picker type="time" v-model="transaction.time" @change="watch_date_time_picker" id="timepicker_field" :placeholder="$t('Time')" :disabled="disable_date_time_picker"></custom-date-picker>
                </div>
                <div>
                    <custom-date-picker type="date" v-model="transaction.date" @change="watch_date_time_picker" id="datepicker_field" :placeholder="$t('Date')" :disabled="disable_date_time_picker"></custom-date-picker>
                </div>
            </div>
            <div class="forminput-control">
                <textarea v-model="transaction.desc" id="description_field" ref="description_field" required rows="3" disabled></textarea>
                <label for="description_field">{{ $t('Description') }} <i class="ti-microphone blink-animation d-none" ref="description_field_mic"></i></label>
            </div>
            <button type="submit" ref="submit_btn" disabled class="btn">{{ $t('SAVE') }}</button><br>
        </form>
    </div>

    <div class="loading-progress" :style="{'width': `${percent_loading_page}%`}"></div>

    <div class="msg-section">
        <p class="success fade-out" v-if="msg.success"><i class="ti-thumb-up"></i> {{ msg.success }}</p>
        <p class="error fade-out" v-if="msg.error"><i class="ti-thumb-down"></i> {{ msg.error }}</p>
        <p class="info fade-out" v-if="msg.info"><i class="ti-info-alt"></i> {{ msg.info }}</p>
    </div>
</template>

<script>
import axios from '../plugins/axios';

export default {
    name: 'SaveVoiceTransaction',

    data: () => ({
        disable_date_time_picker: true,
        show_surement: true,
        transaction: {
            bank_name: '',
            type: '',
            price: '',
            time: '',
            date: '',
            desc: '',
        },
        banks: [],
        voiceList: {
            bank_name_real_en: '/audio/en/bank_name_real.mp3',
            bank_name_real_fa: '/audio/en/bank_name_real.mp3',
            bank_name_again_en: '/audio/en/bank_name_again.mp3',
            bank_name_again_fa: '/audio/en/bank_name_again.mp3',

            price_real_en: '/audio/en/price_real.mp3',
            price_real_fa: '/audio/en/price_real.mp3',
            price_again_en: '/audio/en/price_again.mp3',
            price_again_fa: '/audio/en/price_again.mp3',

            type_transaction_real_en: '/audio/en/type_transaction_real.mp3',
            type_transaction_real_fa: '/audio/en/type_transaction_real.mp3',
            type_transaction_again_en: '/audio/en/type_transaction_again.mp3',
            type_transaction_again_fa: '/audio/en/type_transaction_again.mp3',

            date_time_real_en: '/audio/en/date_time_real.mp3',
            date_time_real_fa: '/audio/en/date_time_real.mp3',

            description_real_en: '/audio/en/description_real.mp3',
            description_real_fa: '/audio/en/description_real.mp3',
            description_again_en: '/audio/en/description_again.mp3',
            description_again_fa: '/audio/en/description_again.mp3',
        },
        lang_voice_assistant: '',
        percent_loading_page: 0,
        msg: { success: '', error: '', info: '' },
    }),

    created() { 
        if(this.$i18n.locale == 'fa') {
            this.lang_voice_assistant = 'fa-IR';
        } else if (this.$i18n.locale == 'en') {
            this.lang_voice_assistant = 'en-US';
        }
        this.get_banks();
    },

    methods: {

        fire_progressive() {
            this.show_surement = false;
            this.progressive_get_bank_name('real');
        },
 
        async get_banks() {
            let a_token = JSON.parse(localStorage.getItem('BOOKKEEPER_AT'));
            await axios.get(`/${this.$i18n.locale}/api/v1/card-management/`, {
                headers: {
                    'Authorization': `Bearer ${a_token}`,
                }
            })
            .then((result) => {
                if(result.status === 200) {
                    this.banks = result.data.data;
                }
            })
            .catch((err) => {
                this.$router.push('/' + this.$i18n.locale + '/sign-in');
            });
        },

        async save_transaction() {
            this.percent_loading_page = 0;
            this.msg = {success: '', error: '', info: '' };
            let a_token = JSON.parse(localStorage.getItem('BOOKKEEPER_AT'));
            let formdata = new FormData();
            formdata.append('card', this.transaction.bank_name);
            formdata.append('price', this.transaction.price);
            if(this.transaction.type == 'withdrawal' || this.transaction.type == 'برداشت') {
                formdata.append('in_out', 'withdrawal');
            }
            else if(this.transaction.type == 'deposit' || this.transaction.type == 'واریز') {
                formdata.append('in_out', 'deposit');
            }
            formdata.append('time', this.transaction.time);
            formdata.append('date', this.transaction.date);
            formdata.append('description', this.transaction.desc);
            await axios.post(`/${this.$i18n.locale}/api/v1/transaction-management/`, formdata, {
                headers: {
                    'Authorization': `Bearer ${a_token}`,
                    'Content-Type': 'application/json',
                },
                onUploadProgress: function( progressEvent ) {
                    this.percent_loading_page = parseInt( Math.round( ( progressEvent.loaded / progressEvent.total ) * 100 ) );
                }.bind(this)
            })
            .then((result) => {
                if(result.status === 200) {
                    this.msg.success = this.$t('Your Transaction saved Successfully');
                    setTimeout(() => {
                        this.transaction = {
                            bank_name: '',
                            type: '',
                            price: '',
                            time: '',
                            date: '',
                            desc: '',
                        };
                        this.$refs.bank_name_field.setAttribute('disabled', '');
                        this.$refs.price_field.setAttribute('disabled', '');
                        this.$refs.type_transaction_field.setAttribute('disabled', '');
                        this.disable_date_time_picker = true;
                        this.show_surement = true;
                        this.$refs.description_field.setAttribute('disabled', '');
                        this.$refs.submit_btn.setAttribute('disabled', '');
                        this.$router.push('/' + this.$i18n.locale + '/save-voice-transaction')
                    }, 1500);
                }
            })
            .catch((err) => {
                this.msg ={ success: '', error: '', info: '' };
                this.msg.error = this.$t('There is a Problem in Your Form');
            });
        },

        fixNumbers(str) {
            let persianNumbers = [/۰/g, /۱/g, /۲/g, /۳/g, /۴/g, /۵/g, /۶/g, /۷/g, /۸/g, /۹/g]
            if(typeof str === 'string') {
                for(let i=0; i < 10; i++)
                    str = str.replace(persianNumbers[i], i);
            }
            return str;
        },

        progressive_get_bank_name(audio_type) {
            
            if (audio_type == 'real') {
                let audio = new Audio(this.voiceList[`bank_name_real_${this.$i18n.locale}`]);
                audio.play();
            } else if (audio_type == 'again') {
                let audio = new Audio(this.voiceList[`bank_name_again_${this.$i18n.locale}`]);
                audio.play();
            }

            let banksname = [];
            this.banks.map((item) => {
                banksname.push(item.name);
            });

            this.$refs.suggestions1.classList.remove('d-none');
            this.$refs.suggestions1.innerHTML = `<span style="color: #bfbfbf">${this.$t('Your Choices:')}</span><br> ${banksname.join('<br>')}`;

            setTimeout(() => {

                window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                const recognition = new SpeechRecognition();
                let transcript;
                let its_ok = false;
                
                // set configs
                recognition.continuous = false;
                recognition.lang = this.lang_voice_assistant;
                recognition.interimResults = true;
                recognition.maxAlternatives = 1;

                this.$refs.bank_name_field_mic.classList.remove('d-none');
                recognition.start(); // get voice from client

                recognition.onresult = function(e) { // set results in dom
                    transcript = Array.from(e.results).map(result => result[0]).map(result => result.transcript).join('');
                }
                recognition.onerror= function(event) { // an error occurred
                    recognition.stop();
                }
                recognition.onnomatch = function(event) { // not found results
                    recognition.stop();
                }
                recognition.onspeechend = function(event) { // end of get tunes
                    recognition.stop();
                }

                setTimeout(() => {
                    this.$refs.bank_name_field_mic.classList.add('d-none');
                    this.$refs.bank_name_field.removeAttribute('disabled');
                    this.$refs.bank_name_field.focus();

                    this.transaction.bank_name = transcript;

                    this.banks.map((item) => {
                        if(item.name == transcript)
                            its_ok = true
                        if(item.name.includes(transcript)){
                            its_ok = true
                            this.transaction.bank_name = item.name;
                        }
                    });
                    if (its_ok == true){
                        this.progressive_get_price('real');
                        this.$refs.suggestions1.classList.add('d-none');
                    } else {
                        this.$refs.bank_name_field.setAttribute('disabled', '');
                        this.transaction.bank_name = '';
                        this.progressive_get_bank_name('again');
                    }
                }, 4000);

            }, 3000);
        },

        progressive_get_price(audio_type) {
            
            if (audio_type == 'real') {
                let audio = new Audio(this.voiceList[`price_real_${this.$i18n.locale}`]);
                audio.play();
            } else if (audio_type == 'again') {
                let audio = new Audio(this.voiceList[`price_again_${this.$i18n.locale}`]);
                audio.play();
            }

            setTimeout(() => {

                window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                const recognition = new SpeechRecognition();
                let transcript;
                let its_ok = false;
                
                // set configs
                recognition.continuous = false;
                recognition.lang = this.lang_voice_assistant;
                recognition.interimResults = true;
                recognition.maxAlternatives = 1;

                this.$refs.price_field_mic.classList.remove('d-none');
                recognition.start(); // get voice from client

                recognition.onresult = function(e) { // set results in dom
                    transcript = Array.from(e.results).map(result => result[0]).map(result => result.transcript).join('');
                }
                recognition.onerror= function(event) { // an error occurred
                    recognition.stop();
                }
                recognition.onnomatch = function(event) { // not found results
                    recognition.stop();
                }
                recognition.onspeechend = function(event) { // end of get tunes
                    recognition.stop();
                }

                setTimeout(() => {
                    this.$refs.price_field_mic.classList.add('d-none');
                    this.$refs.price_field.removeAttribute('disabled');
                    this.$refs.price_field.focus();

                    this.transaction.price = this.fixNumbers(transcript);

                    if(this.transaction.price > 0){
                        its_ok = true;
                    }

                    if (its_ok == true){
                        this.progressive_get_type_transaction('real');
                    } else {
                        this.$refs.price_field.setAttribute('disabled', '');
                        this.transaction.price = '';
                        this.progressive_get_price('again');
                    }
                }, 4000);

            }, 3000);
        },

        progressive_get_type_transaction(audio_type) {
            
            if (audio_type == 'real') {
                let audio = new Audio(this.voiceList[`type_transaction_real_${this.$i18n.locale}`]);
                audio.play();
            } else if (audio_type == 'again') {
                let audio = new Audio(this.voiceList[`type_transaction_again_${this.$i18n.locale}`]);
                audio.play();
            }

            this.$refs.suggestions2.classList.remove('d-none');
            this.$refs.suggestions2.innerHTML = `<span style="color: #bfbfbf">${this.$t('Your Choices:')}</span><br> ${this.$t('Deposit')}<br>${this.$t('WithDrawal')}`;

            setTimeout(() => {

                window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                const recognition = new SpeechRecognition();
                let transcript;
                let its_ok = false;
                
                // set configs
                recognition.continuous = false;
                recognition.lang = this.lang_voice_assistant;
                recognition.interimResults = true;
                recognition.maxAlternatives = 1;

                this.$refs.transaction_type_field_mic.classList.remove('d-none');
                recognition.start(); // get voice from client

                recognition.onresult = function(e) { // set results in dom
                    transcript = Array.from(e.results).map(result => result[0]).map(result => result.transcript).join('');
                }
                recognition.onerror= function(event) { // an error occurred
                    recognition.stop();
                }
                recognition.onnomatch = function(event) { // not found results
                    recognition.stop();
                }
                recognition.onspeechend = function(event) { // end of get tunes
                    recognition.stop();
                }

                setTimeout(() => {
                    this.$refs.transaction_type_field_mic.classList.add('d-none');
                    this.$refs.type_transaction_field.removeAttribute('disabled');
                    this.$refs.type_transaction_field.focus();

                    this.transaction.type = transcript;

                    let words = ['deposit', 'withdrawal', 'واریز', 'برداشت'];
                    words.map((item) => {
                        if(this.transaction.type == item) {
                            its_ok = true;
                        }
                    });

                    if (its_ok == true){
                        this.progressive_get_date_time('real');
                        this.$refs.suggestions2.classList.add('d-none');
                    } else {
                        this.$refs.type_transaction_field.setAttribute('disabled', '');
                        this.transaction.type = '';
                        this.progressive_get_type_transaction('again');
                    }
                }, 4000);

            }, 3000);
        },

        progressive_get_date_time() {

            let audio = new Audio(this.voiceList[`date_time_real_${this.$i18n.locale}`]);
            audio.play();

            setTimeout(() => {
                this.disable_date_time_picker = false;
            }, 3000);
        },

        watch_date_time_picker(e){
            if(this.transaction.date != '' && this.transaction.time != '') {
                this.progressive_get_description('real');
            }
        },

        progressive_get_description(audio_type) {
            
            if (audio_type == 'real') {
                let audio = new Audio(this.voiceList[`description_real_${this.$i18n.locale}`]);
                audio.play();
            } else if (audio_type == 'again') {
                let audio = new Audio(this.voiceList[`description_again_${this.$i18n.locale}`]);
                audio.play();
            }

            setTimeout(() => {

                window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                const recognition = new SpeechRecognition();
                
                // set configs
                recognition.continuous = false;
                recognition.lang = this.lang_voice_assistant;
                recognition.interimResults = true;
                recognition.maxAlternatives = 1;

                this.$refs.description_field_mic.classList.remove('d-none');
                this.$refs.description_field.removeAttribute('disabled');
                this.$refs.description_field.focus();
                
                recognition.start(); // get voice from client

                let my_this = this;
                recognition.onresult = function(e) { // set results in dom
                    const transcript = Array.from(e.results).map(result => result[0]).map(result => result.transcript).join('');
                    my_this.transaction.desc = transcript;
                }
                recognition.onerror= function(event) { // an error occurred
                    my_this.$refs.description_field_mic.classList.add('d-none');
                    recognition.stop();
                }
                recognition.onnomatch = function(event) { // not found results
                    my_this.$refs.description_field_mic.classList.add('d-none');
                    recognition.stop();
                }
                recognition.onspeechend = function(event) { // end of get tunes
                    my_this.$refs.description_field_mic.classList.add('d-none');
                    setTimeout(() => {
                        my_this.$refs.submit_btn.removeAttribute('disabled');
                        my_this.save_transaction(); // click submit btn
                    }, 2000)
                    recognition.stop();
                }

            }, 3000);
        },
    },

    async mounted() {
        // check user
        let r_token = JSON.parse(localStorage.getItem('BOOKKEEPER_RT'));
        if(r_token) {
            let formdata = new FormData();
            formdata.append('refresh', r_token)
            await axios.post(`/${this.$i18n.locale}/api/v1/get-token/refresh-token/`, formdata, {
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then((result) => {
                localStorage.setItem('BOOKKEEPER_AT', JSON.stringify(result.data.access));
                this.$store.dispatch('getUserData', {at: result.data.access, lang: this.$i18n.locale});
            })
            .catch((err) => {
                this.$router.push('/' + this.$i18n.locale + '/sign-in');
            })
        } else {
            this.$router.push('/' + this.$i18n.locale + '/sign-in');
        }
    }
}
</script>

<style scoped>
.opacity-wrapper .after--forminput-control {
    position: absolute;
    top: 37%;
    right: 25%;
    padding: 10px 15px;
    border-radius: 7px;
    background-color: #0c0e0d;
    width: 140px;
    z-index: 1000;
    font-size: 10pt;
    transition: all 0.3s linear;
}
.opacity-wrapper .after--forminput-control::before {
    content: '';
    position: absolute;
    top: 0;
    right: -18px;
    background-color: #0c0e0d;
    clip-path: polygon(0 6px, 20px 0, 0 20px);
    height: 20px;
    width: 20px;
    z-index: 1000;
    font-size: 10pt;
}
.opacity-wrapper-ltr .after--forminput-control {
    position: absolute;
    top: 37%;
    left: 30%;
    padding: 10px 15px;
    border-radius: 7px;
    background-color: #0c0e0d;
    width: 140px;
    z-index: 1000;
    font-size: 10pt;
    transition: all 0.3s linear;
}
.opacity-wrapper-ltr .after--forminput-control::before {
    content: '';
    position: absolute;
    top: 0;
    left: -16px;
    background-color: #0c0e0d;
    clip-path: polygon(0 0, 20px 6px, 20px 20px);
    height: 20px;
    width: 20px;
    z-index: 1000;
    font-size: 10pt;
}
.after--forminput-control-sm {
    width: 100px !important;
}
.opacity-wrapper input#price_field { width: 97% !important; margin-right: 1px !important; }
.opacity-wrapper select#type_transaction_field { width: 97% !important; margin-left: 0 !important; float: left; }
.opacity-wrapper-ltr #bank_name_field { margin-left: 0 !important; }
button[type="submit"]:hover { color: white; background-color:#0000008e !important; transform: translateY(-1px); }
.opacity-wrapper { width: 40% !important; min-height: 415px !important; }
.vpd-controls, .vpd-day-text {color: #aaa !important;}
.wrapper-surement {
    position: absolute;
    inset: 0;
    background-color: rgba(0,0,0,0.87);
    z-index: 100;
    padding: 2rem;
    text-align: center;
    display: flex;
    align-items: center;
    border-radius: 15px;
    justify-content: center;
    flex-direction: column;
    transition: all 0.3s ease;
}
.wrapper-surement p {
    padding-bottom: 20px;
}
.wrapper-surement button {
    padding: 14px 15px;
    border-radius: 50%;
    background: linear-gradient(rgb(77, 77, 77), rgb(31, 31, 31));
    cursor: url(../assets/img/cursor-link.png),auto;
    transform: rotateZ(-30deg);
    position: relative;
    transition: all 0.3s ease;
}
.wrapper-surement button:hover {
    transform: scale(1.02) rotateZ(-30deg);
}
.wrapper-surement button::before {
    content: '';
    position: absolute;
    border-radius: 50%;
    inset: 0;
    background-color: rgba(255, 255, 255, 0.1);
    animation: faderBtn 1.5s infinite linear;
}
@keyframes faderBtn {
    0% {
        transform: scale(1);
        opacity: 1;
    }
    75% {
        transform: scale(1.4);
        opacity: 0.2;
    }
    100% {
        transform: scale(1.4);
        opacity: 0;
    }
}
.wrapper-surement button i {
    font-size: 30pt;
    cursor: url(../assets/img/cursor-link.png),auto;
    color: white;
}
.wrapper-date-time { display: flex; margin-bottom: 30px; } .wrapper-date-time div { flex: 1; } .wrapper-date-time div:nth-child(1) { flex: 1; margin: 0 0 0 5px; } .wrapper-date-time div:nth-child(2) { flex: 1; margin: 0 5px 0 0; }
.opacity-wrapper-ltr .wrapper-date-time div:nth-child(1) { flex: 1; } .opacity-wrapper-ltr .wrapper-date-time div:nth-child(2) { flex: 1; margin: 0 0 0 5px !important; }
.opacity-wrapper-ltr .forminput-control{position:relative}.opacity-wrapper-ltr .forminput-control label{position:absolute;top:0;left:0;padding:10px 0;font-size:15px;color:#fff;transition:.5s}.opacity-wrapper-ltr .forminput-control #current_stock_field,.opacity-wrapper-ltr .forminput-control #expire_field{margin-left:5px}.opacity-wrapper-ltr .forminput-control label[for='date_field'],.opacity-wrapper-ltr .forminput-control label[for='time_field']{display:none}.opacity-wrapper-ltr .forminput-control input:focus ~ label,.opacity-wrapper-ltr .forminput-control input:valid ~ label{top:-20px;right:0px;font-size:11px}.opacity-wrapper-ltr button[type="submit"]{float:right !important}.opacity-wrapper h4{margin-bottom:1.5rem}.opacity-wrapper .wrapper-twofield{display:flex;flex-wrap:wrap}.opacity-wrapper .wrapper-twofield .forminput-control{flex:1}.opacity-wrapper .forminput-control{position:relative}.opacity-wrapper .forminput-control input{width:100%;padding:11px 3px 3px 3px;font-size:16px;color:#eaeaea;margin-bottom:20px;border:none;border-bottom:1px solid #fff;background:transparent}.opacity-wrapper .forminput-control textarea{padding:11px 3px 3px 3px;font-size:16px;color:#eaeaea;margin-bottom:10px;border:none;border-bottom:1px solid #fff;background:transparent;width:100% !important}.opacity-wrapper .forminput-control select{padding:6px 0;font-size:11pt;color:#fff;margin:0 0 20px 5px;border:none;border-bottom:1px solid #fff;background:#2424244f;width:100% !important}.opacity-wrapper .forminput-control label{position:absolute;top:0;right:0;padding:10px 0;font-size:15px;color:#fff;transition:.5s}.opacity-wrapper .forminput-control label[for='time_field'],.opacity-wrapper .forminput-control label[for='date_field']{position:absolute;top:0;right:29px;padding:8px 0;font-size:15px;color:#fff;transition:.5s}.opacity-wrapper .forminput-control input:focus ~ label,.opacity-wrapper .forminput-control input:valid ~ label,.opacity-wrapper .forminput-control textarea:focus ~ label,.opacity-wrapper .forminput-control textarea:valid ~ label{top:-20px;right:0;font-size:11px}.opacity-wrapper button[type="submit"]{color:rgb(238, 238, 238);background-color:#0000006e;padding:0.3rem 1rem;border-radius:5px;transition: all 0.3s ease;float:left}@media screen and (max-width: 900px){.container .page-wrapper .article .wrapper-body .opacity-wrapper{width:90% !important}}
</style>