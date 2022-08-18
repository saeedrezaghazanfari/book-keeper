<template>
    <div class="opacity-wrapper" :class="{'opacity-wrapper-ltr': $i18n.locale == 'en'}">
        <h4><i class="ti-marker-alt"></i> {{ $t('Transaction Registration') }}</h4>
        <form novalidate @submit.prevent="save_transaction">
            <div class="forminput-control">
                <select v-model="transaction.bank_name" type="text" id="bank_name_field" required>
                    <option value="Bank Name">{{ $t('Bank Name') }}</option>
                    <option :value="bank.name" v-for="bank in banks" :key="bank">{{ bank.name }}</option>
                </select>
            </div>
            <div class="wrapper-twofield">
                <div class="forminput-control">
                    <input v-model="transaction.price" type="number" id="price_field" required class="text-center">
                    <label for="price_field">{{ $t('Price') }}</label>
                </div>
                <div class="forminput-control">
                    <select v-model="transaction.type" type="text" id="type_transaction_field" required>
                        <option value="Transaction Type">{{ $t('Transaction Type') }}</option>
                        <option value="deposit">{{ $t('Deposit') }}</option>
                        <option value="withdrawal">{{ $t('WithDrawal') }}</option>
                    </select>
                </div>
            </div>
            <div class="wrapper-date-time">
                <div>
                    <custom-date-picker type="time" v-model="transaction.time" :placeholder="$t('Time')"></custom-date-picker>
                </div>
                <div>
                    <custom-date-picker type="date" v-model="transaction.date" :placeholder="$t('Date')"></custom-date-picker>
                </div>
            </div>
            <div class="forminput-control">
                <textarea v-model="transaction.desc" type="text" id="description_field" required rows="3"></textarea>
                <label for="description_field">{{ $t('Description') }}</label>
            </div>
            <button type="submit" v-if="transaction.type != 'Transaction Type' && transaction.bank_name != 'Bank Name' && transaction.price != '' && transaction.time != '' && transaction.date != '' && transaction.desc != ''" class="btn">{{ $t('SAVE') }}</button><br>
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
    name: 'SaveTransaction',

    data: () => ({
        transaction: {
            bank_name: 'Bank Name',
            type: 'Transaction Type',
            price: '',
            time: '',
            date: '',
            desc: '',
        },
        banks: [],
        percent_loading_page: 0,
        msg: { success: '', error: '', info: '' },
    }),

    created() { this.get_banks(); },

    methods: {

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
            formdata.append('in_out', this.transaction.type);
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
                            bank_name: 'Bank Name',
                            type: 'Transaction Type',
                            price: '',
                            time: '',
                            date: '',
                            desc: '',
                        };
                        this.$router.push('/' + this.$i18n.locale + '/save-transaction')
                    }, 1500);
                }
            })
            .catch((err) => {
                this.msg ={ success: '', error: '', info: '' };
                this.msg.error = this.$t('There is a Problem in Your Form');
            });
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
.opacity-wrapper input#price_field { width: 97% !important; margin-right: 1px !important; }
.opacity-wrapper select#type_transaction_field { width: 97% !important; margin-left: 0 !important; float: left; }
.opacity-wrapper-ltr #bank_name_field { margin-left: 0 !important; }
button[type="submit"]:hover { color: white; background-color:#0000008e !important; transform: translateY(-1px); }
.opacity-wrapper { width: 40% !important; min-height: 415px !important; }
.vpd-controls, .vpd-day-text {color: #aaa !important;}
.wrapper-date-time { display: flex; margin-bottom: 30px; } .wrapper-date-time div { flex: 1; } .wrapper-date-time div:nth-child(1) { flex: 1; margin: 0 0 0 5px; } .wrapper-date-time div:nth-child(2) { flex: 1; margin: 0 5px 0 0; }
.opacity-wrapper-ltr .wrapper-date-time div:nth-child(1) { flex: 1; } .opacity-wrapper-ltr .wrapper-date-time div:nth-child(2) { flex: 1; margin: 0 0 0 5px !important; }
.opacity-wrapper-ltr .forminput-control{position:relative}.opacity-wrapper-ltr .forminput-control label{position:absolute;top:0;left:0;padding:10px 0;font-size:15px;color:#fff;transition:.5s}.opacity-wrapper-ltr .forminput-control #current_stock_field,.opacity-wrapper-ltr .forminput-control #expire_field{margin-left:5px}.opacity-wrapper-ltr .forminput-control label[for='date_field'],.opacity-wrapper-ltr .forminput-control label[for='time_field']{display:none}.opacity-wrapper-ltr .forminput-control input:focus ~ label,.opacity-wrapper-ltr .forminput-control input:valid ~ label{top:-20px;right:0px;font-size:11px}.opacity-wrapper-ltr button[type="submit"]{float:right !important}.opacity-wrapper h4{margin-bottom:1.5rem}.opacity-wrapper .wrapper-twofield{display:flex;flex-wrap:wrap}.opacity-wrapper .wrapper-twofield .forminput-control{flex:1}.opacity-wrapper .forminput-control{position:relative}.opacity-wrapper .forminput-control input{width:100%;padding:11px 3px 3px 3px;font-size:16px;color:#eaeaea;margin-bottom:20px;border:none;border-bottom:1px solid #fff;background:transparent}.opacity-wrapper .forminput-control textarea{padding:11px 3px 3px 3px;font-size:16px;color:#eaeaea;margin-bottom:10px;border:none;border-bottom:1px solid #fff;background:transparent;width:100% !important}.opacity-wrapper .forminput-control select{padding:6px 0;font-size:11pt;color:#fff;margin:0 0 20px 5px;border:none;border-bottom:1px solid #fff;background:#2424244f;width:100% !important}.opacity-wrapper .forminput-control label{position:absolute;top:0;right:0;padding:10px 0;font-size:15px;color:#fff;transition:.5s}.opacity-wrapper .forminput-control label[for='time_field'],.opacity-wrapper .forminput-control label[for='date_field']{position:absolute;top:0;right:29px;padding:8px 0;font-size:15px;color:#fff;transition:.5s}.opacity-wrapper .forminput-control input:focus ~ label,.opacity-wrapper .forminput-control input:valid ~ label,.opacity-wrapper .forminput-control textarea:focus ~ label,.opacity-wrapper .forminput-control textarea:valid ~ label{top:-20px;right:0;font-size:11px}.opacity-wrapper button[type="submit"]{color:rgb(238, 238, 238);background-color:#0000006e;padding:0.3rem 1rem;border-radius:5px;transition: all 0.3s ease;float:left}@media screen and (max-width: 900px){.container .page-wrapper .article .wrapper-body .opacity-wrapper{width:90% !important}}
</style>