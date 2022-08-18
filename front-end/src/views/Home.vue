<template>
    <div class="opacity-wrapper" :class="{'opacity-wrapper-ltr': $i18n.locale == 'en'}">
        <h4><i class="ti-home"></i> {{ $t('Home') }}</h4>

        <ul class="wrapper-links">
            <li><router-link :to="{ name: 'SaveTransaction' }"><i class="ti-marker-alt"></i>{{ $t('Transaction Registration') }}</router-link></li>
            <li><router-link :to="{ name: 'LastTransactions' }"><i class="ti-pulse"></i>{{ $t('Latest Transactions') }}</router-link></li>
            <li><router-link :to="{ name: 'SaveCard' }"><i class="ti-save"></i>{{ $t('Card Registration') }}</router-link></li>
            <li><router-link :to="{ name: 'PrintAccount' }"><i class="ti-files"></i>{{ $t('Print Transactions') }}</router-link></li>
            <li><router-link :to="{ name: 'ShowChart' }"><i class="ti-stats-up"></i>{{ $t('Show Charts') }}</router-link></li>
            <li><router-link :to="{ name: 'ChnageInfo' }"><i class="ti-user"></i>{{ $t('Change Info') }}</router-link></li>
            <li><router-link :to="{ name: 'Setting' }"><i class="ti-image"></i>{{ $t('Backstage Settings') }}</router-link></li>
        </ul>
    </div>
</template>

<script>
import axios from '../plugins/axios';

export default {
    name: 'Home',

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
    max-height: 384px !important;
    width: 35% !important;
}
.opacity-wrapper h4{margin-bottom:1rem}.opacity-wrapper ul.wrapper-links{list-style-type:none}.opacity-wrapper ul.wrapper-links li{padding:8px 18px}.opacity-wrapper ul.wrapper-links li a{color:white;transition:all 0.3s ease;font-size:12pt}.opacity-wrapper ul.wrapper-links li a i{padding:0 4px;transition:all 0.3s ease;font-size:12pt;color:gray}.opacity-wrapper ul.wrapper-links li:hover a{padding-right:5px}.opacity-wrapper ul.wrapper-links li:hover i{font-size:15pt;color:white}@media screen and (max-width: 750px){.container .page-wrapper .article .wrapper-body .opacity-wrapper{width:90% !important}}
</style>