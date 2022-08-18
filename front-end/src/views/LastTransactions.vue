<template>
    <div class="opacity-wrapper" :class="{'opacity-wrapper-ltr': $i18n.locale == 'en'}">

        <h4 ref="first_title"><i class="ti-pulse"></i> {{ $t('Latest Transactions') }}</h4>
        <h4 class="d-none" ref="sec_title"><i class="ti-menu-alt"></i> {{ $t('Show') }} <select v-model="number">
            <option :value="number" v-for="number in numbers" :key="number">{{ number }}</option>
        </select> {{ $t('Last Transactions') }}</h4>

        <ul ref="banks_div" class="wrapper-links">
            <li v-for="bank in banks" @click="get_transactions(bank.name)" :key="bank">
                <a><i :class="{'ti-hand-point-left': $i18n.locale == 'fa', 'ti-hand-point-right': $i18n.locale == 'en'}"></i> {{ bank.name }}</a>
            </li>
        </ul>

        <ul ref="reset_div" class="wrapper-lines d-none">
            <li class="mb-1-2">
                <i class="ti-server text-light"></i> <span class="text-light">{{ $t('Bank Name') }}:</span> {{ current_bank_transactions }}
            </li>
            <li class="mb-1-2">
                <i class="ti-money text-light"></i> <span class="text-light">{{ $t('Your Stock') }}:</span> {{ last_bank_stock }}
            </li>
            <li @click="reset_div" class="mb-1">
                <i class="text-light link" :class="{'ti-arrow-left': $i18n.locale == 'fa', 'ti-arrow-right': $i18n.locale == 'en'}"></i> <span class="text-light link">{{ $t('Go Back') }}</span>
            </li>
        </ul>

        <div ref="transactions_div" class="list-transactions d-none">
            <div class="transaction-info" v-for="(transaction, index) in transactions" :key="index">
                <div class="two-field">
                    <p>{{ transaction.price }} <i class="ti-money font-8-pt"></i></p>
                    <p v-if="transaction.type == 'deposit'">{{ $t(transaction.type) }} <i class="font-8-pt ti-angle-double-down text-green"></i></p>
                    <p v-else-if="transaction.type == 'withdrawal'">{{ $t(transaction.type) }} <i class="font-8-pt ti-angle-double-up text-red"></i></p>
                </div>
                <div class="two-field">
                    <p>{{ transaction.time }} <i class="ti-time font-8-pt"></i></p>
                    <p>{{ transaction.date }} <i class="ti-calendar font-8-pt"></i></p>
                </div>
                <button class="btn_show_more link mx-1-2" @click="show_desc(`desc_${index}`, `angle_icon_${index}`, `span_show_more_${index}`)">
                    <i :id="'angle_icon_'+index" class="ti-angle-double-left icon-lr-transaction"></i> <span :id="'span_show_more_'+index" class="span-lr-transaction">{{ $t('Show More') }}</span>
                </button>
                <p class="more-info d-none mx-1-2 mt-1-2" :id="'desc_'+index">{{ transaction.desc }}</p>
            </div>
        </div>

    </div>
</template>


<script>
import axios from '../plugins/axios';

export default {
    name: 'LastTransactions',

    data() {
        return {
            transactions: [],
            numbers: [20, 30, 50],
            number: 20,
            last_bank_stock: '',
            banks: [],
        }
    },

    created() { this.get_banks(); },

    watch: {
        async number(newval, oldval) {
            this.transactions = [];
            let a_token = JSON.parse(localStorage.getItem('BOOKKEEPER_AT'));
            await axios.get(`/${this.$i18n.locale}/api/v1/transaction-management/?bank=${this.current_bank_transactions}&amount=${newval}`, {
                headers: {
                    'Authorization': `Bearer ${a_token}`,
                }
            })
            .then((result) => {
                if(result.data.status === 200) {
                    this.last_bank_stock = result.data.last_stock;
                    for(let i = 0; i < result.data.data.length; i++) {
                        this.transactions.push({
                            price: result.data.data[i].price,
                            type: result.data.data[i].in_out,
                            time: result.data.data[i].time,
                            date: result.data.data[i].date,
                            desc: result.data.data[i].description,
                        });
                    }
                }
            })
            .catch((err) => {
                this.$router.push('/' + this.$i18n.locale + '/sign-in');
            });
            this.$refs.first_title.classList.add('d-none');
            this.$refs.sec_title.classList.remove('d-none');
            this.$refs.banks_div.classList.add('d-none');
            this.$refs.transactions_div.classList.remove('d-none');
            this.$refs.reset_div.classList.remove('d-none');
        }
    },

    methods: {
        show_desc(itemId, iconId, spanId) {
            let itemel = document.getElementById(itemId);
            let iconel = document.getElementById(iconId);
            let spanel = document.getElementById(spanId);

            document.querySelectorAll('.more-info').forEach((item) => {
                if (item != itemel)
                    item.classList.add('d-none');
            });
            document.querySelectorAll('.icon-lr-transaction').forEach((item) => {
                if (item.classList.contains('ti-angle-double-down')) {
                    item.classList.remove('ti-angle-double-down');
                    item.classList.add('ti-angle-double-left');
                }
            });
            document.querySelectorAll('.span-lr-transaction').forEach((item) => {
                if(item.innerHTML == 'Show Less' || item.innerHTML == 'نمایش کمتر' ) 
                    item.innerHTML = this.$t('Show More');
            });

            if (itemel.classList.contains('d-none')) {
                itemel.classList.remove('d-none');
                iconel.classList.remove('ti-angle-double-left');
                iconel.classList.add('ti-angle-double-down');
                spanel.innerHTML = this.$t('Show Less');
            }
            else {
                itemel.classList.add('d-none');
                iconel.classList.remove('ti-angle-double-down');
                iconel.classList.add('ti-angle-double-left');
                spanel.innerHTML = this.$t('Show More');
            }
        },

        async get_banks() {
            let a_token = JSON.parse(localStorage.getItem('BOOKKEEPER_AT'));
            await axios.get(`/${this.$i18n.locale}/api/v1/card-management/`, {
                headers: {
                    'Authorization': `Bearer ${a_token}`,
                }
            })
            .then((result) => {
                if(result.data.status === 200) {
                    this.banks = result.data.data;
                }
            })
            .catch((err) => {
                this.$router.push('/' + this.$i18n.locale + '/sign-in');
            });
        },

        async get_transactions(bankname) {
            this.transactions = [];
            this.current_bank_transactions = bankname;
            let a_token = JSON.parse(localStorage.getItem('BOOKKEEPER_AT'));
            await axios.get(`/${this.$i18n.locale}/api/v1/transaction-management/?bank=${this.current_bank_transactions}&amount=${this.number}`, {
                headers: {
                    'Authorization': `Bearer ${a_token}`,
                }
            })
            .then((result) => {
                if(result.data.status === 200) {
                    this.last_bank_stock = result.data.last_stock;
                    for(let i = 0; i < result.data.data.length; i++) {
                        this.transactions.push({
                            price: result.data.data[i].price,
                            type: result.data.data[i].in_out,
                            time: result.data.data[i].time,
                            date: result.data.data[i].date,
                            desc: result.data.data[i].description,
                        });
                    }
                }
            })
            .catch((err) => {
                this.$router.push('/' + this.$i18n.locale + '/sign-in');
            });
            this.$refs.first_title.classList.add('d-none');
            this.$refs.sec_title.classList.remove('d-none');
            this.$refs.banks_div.classList.add('d-none');
            this.$refs.transactions_div.classList.remove('d-none');
            this.$refs.reset_div.classList.remove('d-none');
        },

        reset_div() {
            this.transactions = [];
            this.$refs.first_title.classList.remove('d-none');
            this.$refs.sec_title.classList.add('d-none');
            this.$refs.banks_div.classList.remove('d-none');
            this.$refs.transactions_div.classList.add('d-none');
            this.$refs.reset_div.classList.add('d-none');
        }
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
.opacity-wrapper {
    width: 40% !important;
    min-height: 415px !important;
}
.btn_show_more {
    background-color: transparent;
    font-size: 9pt;
    color: #a3a3a3;
    border: none;
    outline: none;
}
.text-light {
    color: #a3a3a3;
}
ul{list-style: none;}
.opacity-wrapper ul.wrapper-lines li{padding:0px 18px; color:white;transition:all 0.3s ease;font-size:12pt}
.opacity-wrapper ul.wrapper-lines li i{font-size: 10pt;}
.font-8-pt{font-size: 8pt}.link-green{border-color: #00ff00 !important;}.link-red{border-color: red !important;}.text-green{color: #00ff00 !important;}.text-red{color: red !important;}.opacity-wrapper h4{margin-bottom:1rem}.opacity-wrapper ul.wrapper-links{list-style-type:none}.opacity-wrapper ul.wrapper-links li{padding:8px 18px}.opacity-wrapper ul.wrapper-links li a{color:white;transition:all 0.3s ease;font-size:12pt}.opacity-wrapper ul.wrapper-links li a i{padding:0 4px;transition:all 0.3s ease;font-size:12pt;color:gray}.opacity-wrapper ul.wrapper-links li:hover a{padding-right:5px}.opacity-wrapper ul.wrapper-links li:hover i{font-size:15pt;color:white}.opacity-wrapper select{width:40px;padding:6px 0;font-size:11pt;color:#fff;border:none;background:#2424244f}.opacity-wrapper .list-transactions .transaction-info{padding: 17px 0.5rem;border-radius: 5px;background-color: #000000a6;font-size: 11pt;/* border: 1px dashed gray; */margin-bottom: 5px;position: relative;}.opacity-wrapper .list-transactions .transaction-info .two-field{display:flex;margin-bottom:8px}.opacity-wrapper .list-transactions .transaction-info .two-field p{flex:1;text-align:center}.opacity-wrapper .list-transactions .transaction-info .two-field p i{color:#a3a3a3;padding:0 5px}.opacity-wrapper .list-transactions .transaction-info p.more-info{text-align:justify;color:#bbb;word-break:break-all}@media screen and (max-width: 900px){.container .page-wrapper .article .wrapper-body .opacity-wrapper{width:90% !important}}
</style>