<template>
    <div class="opacity-wrapper" :class="{'opacity-wrapper-ltr': $i18n.locale == 'en'}">
        <h4><i class="ti-direction-alt"></i> {{ $t('Login to BookKeeper') }}</h4>

        <form novalidate @submit.prevent="user_login">
            <div class="forminput-control">
                <input type="text" v-model="username" id="username_field" ref="username_field" required>
                <label for="username_field">{{ $t('UserName') }}</label>
            </div>
            
            <div class="forminput-control forminput-controlpw">
                <input type="password" v-model="password" id="password_number" ref="password_number" required>
                <label for="password_number">{{ $t('PassWord') }}</label>
                <a role="button" class="show-password" @click="show_password">
                    <i class="ti-eye" ref="eyeinput"></i>
                </a>
            </div>
            <button type="submit" class="btn">{{ $t('Login') }}</button>
            <button type="button" class="btn">{{ $t('Login as a Guest') }}</button>
        </form>
    </div>
    <div class="msg-section">
        <p class="success fade-out" v-if="msg.success"><i class="ti-thumb-up"></i> {{ msg.success }}</p>
        <p class="error fade-out" v-if="msg.error"><i class="ti-thumb-down"></i> {{ msg.error }}</p>
        <p class="info fade-out" v-if="msg.info"><i class="ti-info-alt"></i> {{ msg.info }}</p>
    </div>
</template>

<script>
import axios from '../plugins/axios'

export default {
    name: 'SignIn',

    data: () => ({
        username: '',
        password: '',

        msg: { success: '', error: '', info: '' }
    }),

    methods: {
        show_password() {
            if (this.$refs.password_number.type == 'text') {
                this.$refs.password_number.type = 'password';
                this.$refs.eyeinput.classList.add('is_show');
            } else {
                this.$refs.password_number.type = 'text';
                this.$refs.eyeinput.classList.remove('is_show');
            }
        },

        async user_login() {
            let formdata = new FormData();
            formdata.append('username', this.username);
            formdata.append('password', this.password);
            await axios.post(`/${this.$i18n.locale}/api/v1/get-token/`, formdata, {
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then((result) => {
                localStorage.setItem('BOOKKEEPER_RT', JSON.stringify(result.data.refresh));
                localStorage.setItem('BOOKKEEPER_AT', JSON.stringify(result.data.access));
                this.$store.dispatch('getUserData', {at: result.data.access, lang: this.$i18n.locale});
                this.$router.push('/' + this.$i18n.locale + '/');
            })
            .catch((err) => {
                if(err.response.status === 401) {
                    this.msg.error = this.$t('Your UserName or PassWord is Wrong. Try Again!')
                }
            })
        },
    },

    async mounted() {
        // check token
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
                this.$router.push('/' + this.$i18n.locale + '/');
            })
            .catch((err) => {
                this.$router.push('/' + this.$i18n.locale + '/sign-in')
            })
        } else {
            this.$router.push('/' + this.$i18n.locale + '/sign-in')
        }
    }
}
</script>

<style scoped>
button[type="button"] { background-color: #ff000070 !important; margin-right: 3px; }
.opacity-wrapper-ltr{direction:ltr !important}.opacity-wrapper-ltr .forminput-control{position:relative}.opacity-wrapper-ltr .forminput-control label{position:absolute;top:0;left:0;padding:10px 0;font-size:15px;color:#fff;transition:.5s}.opacity-wrapper-ltr .forminput-control #current_stock_field,.opacity-wrapper-ltr .forminput-control #expire_field{margin-left:5px}.opacity-wrapper-ltr .forminput-control label[for='expire_field']{display:none}.opacity-wrapper-ltr .forminput-control input:focus ~ label,.opacity-wrapper-ltr .forminput-control input:valid ~ label{top:-20px;right:0px;font-size:11px}.opacity-wrapper-ltr button[type="submit"], button[type="button"]{float:right !important}.opacity-wrapper h4{margin-bottom:1.5rem}.opacity-wrapper .wrapper-twofield{display:flex;flex-wrap:wrap}.opacity-wrapper .wrapper-twofield .forminput-control{flex:1}.opacity-wrapper .forminput-control{position:relative}.opacity-wrapper .forminput-control input{width:100%;padding:5px 0;font-size:18px;color:#fff;margin-bottom:20px;border:none;border-bottom:1px solid #fff;background:transparent}.opacity-wrapper .forminput-control label{position:absolute;top:0;right:0;padding:10px 0;font-size:15px;color:#fff;transition:.5s}.opacity-wrapper .forminput-control #cvv2_field{padding:6px}.opacity-wrapper .forminput-control #current_stock_field,.opacity-wrapper .forminput-control #expire_field{margin-right:5px}.opacity-wrapper .forminput-control label[for='expire_field']{position:absolute;top:0;right:33px;padding:8px 0;font-size:15px;color:#fff;transition:.5s}.opacity-wrapper .forminput-control input:focus ~ label,.opacity-wrapper .forminput-control input:valid ~ label{top:-20px;right:0px;font-size:11px}.opacity-wrapper .forminput-controlpw input{width:85% !important}.opacity-wrapper .forminput-controlpw a.show-password{padding:5px 12px;font-size:18px;color:#fff;margin-bottom:20px;border:none;border-bottom:1px solid #fff;background:transparent;font-weight:0}.opacity-wrapper .forminput-controlpw a.show-password i.is_show{font-weight:900 !important}.opacity-wrapper button[type="submit"], button[type="button"]{color:white;background-color:#0000006e;padding:0.3rem 1rem;border-radius:5px;float:left}@media screen and (max-width: 900px){.container .page-wrapper .article .wrapper-body .opacity-wrapper{width:90% !important}}
</style>