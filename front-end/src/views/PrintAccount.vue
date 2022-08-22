<template>
    <div class="opacity-wrapper" :class="{'opacity-wrapper-ltr': $i18n.locale == 'en'}">
        <h4><i class="ti-files"></i> {{ $t('Print Transactions') }}</h4>

        <ul class="wrapper-links">
            <li v-for="(bank, index) in banks" :key="index">
                <a :href="`http://127.0.0.1:8000/${$i18n.locale}/api/v1/print-account/?bank-name=${bank.name}&un=${$store.state.user.username}`">
                    <i :class="$i18n.locale == 'fa' ? 'ti-hand-point-left' : 'ti-hand-point-right'"></i> {{ bank.name }}
                </a>
            </li>
        </ul>
    </div>
</template>

<script>
import axios from '../plugins/axios';

export default {
    name: 'PrintAccount',

    data: () => ({
        banks: '',
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
.opacity-wrapper h4{margin-bottom:1rem}.opacity-wrapper ul.wrapper-links{list-style-type:none}.opacity-wrapper ul.wrapper-links li{padding:8px 18px}.opacity-wrapper ul.wrapper-links li a{color:white;transition:all 0.3s ease;font-size:12pt}.opacity-wrapper ul.wrapper-links li a i{padding:0 4px;transition:all 0.3s ease;font-size:12pt;color:gray}.opacity-wrapper ul.wrapper-links li:hover a{padding-right:5px}.opacity-wrapper ul.wrapper-links li:hover i{font-size:15pt;color:white}@media screen and (max-width: 750px){.container .page-wrapper .article .wrapper-body .opacity-wrapper{width:90% !important}}
</style>