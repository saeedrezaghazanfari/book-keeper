<template>
    <div class="opacity-wrapper" :class="{'opacity-wrapper-ltr': $i18n.locale == 'en'}">
        <h4><i class="ti-pulse"></i> {{ $t('Search Transactions') }} (' {{$store.state.search_query }} ')</h4>

        <div ref="transactions_div" class="list-transactions">
            <div class="transaction-info" v-for="(transaction, index) in transactions" :key="index">
                <div class="two-field">
                    <p>{{ transaction.price }} <i class="ti-money font-8-pt"></i></p>
                    <p>{{ $t(transaction.in_out) }} <i class="font-8-pt" :class="transaction.type == 'deposit' ? 'ti-angle-double-down text-green' : 'ti-angle-double-up text-red'"></i></p>
                </div>
                <div class="two-field">
                    <p>{{ transaction.time }} <i class="ti-time font-8-pt"></i></p>
                    <p>{{ transaction.date }} <i class="ti-calendar font-8-pt"></i></p>
                </div>
                <i class="ti-info link" :class="transaction.type == 'deposit' ? 'link-green' : 'link-red'" @click="show_desc(`desc_${index}`)"></i>
                <p class="more-info d-none mx-1-2" :id="'desc_'+index">{{ transaction.description }}</p>
            </div>
        </div>
        <p v-if="transactions == ''" class="not-found">{{ $t('No Matching Transactions Were Found with Your Search Term') }}</p>
    </div>
</template>

<script>
import axios from '../plugins/axios';

export default {
    name: 'SearchTransaction',

    data() {
        return {
            transactions: [],
            banks: [],
        }
    },

    created() {
        this.get_banks();
        this.get_transactions();
    },

    methods: {
        show_desc(itemId) {
            let item = document.getElementById(itemId);
            if (item.classList.contains('d-none')) item.classList.remove('d-none');
            else item.classList.add('d-none');
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

        async get_transactions() {
            let a_token = JSON.parse(localStorage.getItem('BOOKKEEPER_AT'));
            await axios.get(`/${this.$i18n.locale}/api/v1/transaction-management/?type=search&query=${this.$route.params.query}`, {
                headers: {
                    'Authorization': `Bearer ${a_token}`,
                }
            })
            .then((result) => {
                if(result.status === 200) {
                    this.transactions = result.data.data;
                }
            })
            .catch((err) => {
                this.$router.push('/' + this.$i18n.locale + '/sign-in');
            });            
        },
    }
}
</script>

<style scoped>
.not-found{color: red; font-size: 10pt; text-align: center;}.font-8-pt{font-size: 8pt}.link-green{border-color: #00ff00 !important;}.link-red{border-color: red !important;}.text-green{color: #00ff00 !important;}.text-red{color: red !important;}.opacity-wrapper h4{margin-bottom:1rem}.opacity-wrapper ul.wrapper-links{list-style-type:none}.opacity-wrapper ul.wrapper-links li{padding:8px 18px}.opacity-wrapper ul.wrapper-links li a{color:white;transition:all 0.3s ease;font-size:12pt}.opacity-wrapper ul.wrapper-links li a i{padding:0 4px;transition:all 0.3s ease;font-size:12pt;color:gray}.opacity-wrapper ul.wrapper-links li:hover a{padding-right:5px}.opacity-wrapper ul.wrapper-links li:hover i{font-size:15pt;color:white}.opacity-wrapper select{width:40px;padding:6px 0;font-size:11pt;color:#fff;border:none;background:#2424244f}.opacity-wrapper .list-transactions .transaction-info{padding:0.5rem;border-radius:5px;background-color:#2424244f;font-size:11pt;border:1px dashed gray;margin-bottom:5px;position:relative}.opacity-wrapper .list-transactions .transaction-info .two-field{display:flex;margin-bottom:8px}.opacity-wrapper .list-transactions .transaction-info .two-field p{flex:1;text-align:center}.opacity-wrapper .list-transactions .transaction-info .two-field p i{color:#a3a3a3;padding:0 5px}.opacity-wrapper .list-transactions .transaction-info i.ti-info{position:absolute;bottom:10px;right:-10px;background-color:#24242475;border:1px dashed gray;padding:5px 6px;border-radius:5px}.opacity-wrapper .list-transactions .transaction-info p.more-info{text-align:justify;color:#bbb;word-break:break-all}@media screen and (max-width: 900px){.container .page-wrapper .article .wrapper-body .opacity-wrapper{width:90% !important}}
</style>