<template>
    <div class="opacity-wrapper" :class="{'opacity-wrapper-ltr': $i18n.locale == 'en'}">
        <h4><i class="ti-save"></i> {{ $t('Card Registration') }}</h4>

        <form novalidate @submit.prevent="save_card">
            <div class="wrapper-twofield">
                <div class="forminput-control">
                    <input type="text" v-model="card.bankname" id="bankname_field" required>
                    <label for="bankname_field">{{ $t('Bank Name') }}</label>
                </div>
                <div class="forminput-control">
                    <input type="number" v-model="card.current_stock" id="current_stock_field" required class="text-center">
                    <label for="current_stock_field">{{ $t('Current Stock') }}</label>
                </div>
            </div>
            <div class="forminput-control">
                <input type="number" v-model="card.cardnumber" id="cardnumber_field" required>
                <label for="cardnumber_field">{{ $t('Card Number') }}</label>
            </div>
            
            <p ref="card_ref" class="d-nne error_p_form"></p>
            <button type="submit" class="btn">{{ $t('SAVE') }}</button><br>
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
    name: 'SaveCard',

    data: () => ({
        card: {
            bankname: '',
            current_stock: '',
            cardnumber: '',
        },
        percent_loading_page: 0,
        msg: { success: '', error: '', info: '' },
    }),

    methods: {

        async save_card() {
            this.$refs.card_ref.classList.add('d-none');
            
            if (this.card.bankname == '') {
                this.$refs.card_ref.classList.remove('d-none');
                this.$refs.card_ref.innerHTML = this.$t('Your Bank Name must have a Value');
                return;
            }
            if (this.card.current_stock <= 0 || this.card.current_stock == '') {
                this.$refs.card_ref.classList.remove('d-none');
                this.$refs.card_ref.innerHTML = this.$t('Your Stock must be Greater than 0');
                return;
            }
            if (this.card.cardnumber.toString().length != 16) {
                this.$refs.card_ref.classList.remove('d-none');
                this.$refs.card_ref.innerHTML = this.$t('The Card Number must be 16 Digits');
                return;
            }

            this.percent_loading_page = 0;
            this.msg ={ success: '', error: '', info: '' };
            let formdata = new FormData();
            let a_token = JSON.parse(localStorage.getItem('BOOKKEEPER_AT'));
            formdata.append('name', this.card.bankname);
            formdata.append('stock', this.card.current_stock);
            formdata.append('card_number', this.card.cardnumber);
            await axios.post(`/${this.$i18n.locale}/api/v1/card-management/`, formdata, {
                headers: {
                    'Authorization': `Bearer ${a_token}`,
                    'Content-Type': 'application/json',
                },
                onUploadProgress: function( progressEvent ) {
                    this.percent_loading_page = parseInt( Math.round( ( progressEvent.loaded / progressEvent.total ) * 100 ) );
                }.bind(this)
            })
            .then((result) => {
                if(result.data.status === 200) {
                    this.msg ={ success: '', error: '', info: '' };
                    this.msg.success = this.$t('Your Bank Card saved Successfully');
                    setTimeout(() => {
                        this.$router.push('/' + this.$i18n.locale + '/')
                    }, 3000);

                } else if(result.data.status == 400) {

                    if(result.data.msg == 'c') {
                        this.$refs.card_ref.classList.remove('d-none');
                        this.$refs.card_ref.innerHTML = this.$t('Card Number is Duplicated');
                    }
                    else if(result.data.msg == 'n') {
                        this.$refs.card_ref.classList.remove('d-none');
                        this.$refs.card_ref.innerHTML = this.$t('Bank Name is Duplicated');
                    }
                }
            })
            .catch((err) => {
                if(err.response) {
                    this.msg ={ success: '', error: '', info: '' };
                    this.msg.error = this.$t('There is a Problem in Your Form');
                }
            });
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
input#expire_field {padding: 5px !important;}
button[type="submit"]:hover { color: white; background-color:#0000008e !important; transform: translateY(-1px); }
.opacity-wrapper-ltr{direction:ltr !important}.opacity-wrapper-ltr .forminput-control{position:relative}.opacity-wrapper-ltr .forminput-control label{position:absolute;top:0;left:0;padding:10px 0;font-size:15px;color:#fff;transition:.5s}.opacity-wrapper-ltr .forminput-control #current_stock_field,.opacity-wrapper-ltr .forminput-control #expire_field{margin-left:5px}.opacity-wrapper-ltr .forminput-control label[for='expire_field']{display:none}.opacity-wrapper-ltr .forminput-control input:focus ~ label,.opacity-wrapper-ltr .forminput-control input:valid ~ label{top:-20px;right:0px;font-size:11px}.opacity-wrapper-ltr button[type="submit"]{float:right !important}.opacity-wrapper h4{margin-bottom:1.5rem}.opacity-wrapper .wrapper-twofield{display:flex;flex-wrap:wrap}.opacity-wrapper .wrapper-twofield .forminput-control{flex:1}.opacity-wrapper .forminput-control{position:relative}.opacity-wrapper .forminput-control input{width:100%;font-size: 16px; padding: 11px 3px 3px 3px;color:#eaeaea;margin-bottom:20px;border:none;border-bottom:1px solid #fff;background:transparent}.opacity-wrapper .forminput-control label{position:absolute;top:0;right:0;padding:10px 7px;font-size:15px;color:#fff;transition:.5s}.opacity-wrapper .forminput-control #cvv2_field{padding:6px}.opacity-wrapper .forminput-control #current_stock_field,.opacity-wrapper .forminput-control #expire_field{margin-right:5px; width: 97%;}.opacity-wrapper .forminput-control label[for='expire_field']{position:absolute;top:0;right:33px;padding:8px 0;font-size:15px;color:#fff;transition:.5s}.opacity-wrapper .forminput-control input:focus ~ label,.opacity-wrapper .forminput-control input:valid ~ label{top:-20px;right:0px;font-size:11px}.opacity-wrapper button[type="submit"]{color:rgb(238, 238, 238);background-color:#0000006e;padding:0.3rem 1rem;border-radius:5px;transition: all 0.3s ease;float:left}@media screen and (max-width: 900px){.container .page-wrapper .article .wrapper-body .opacity-wrapper{width:90% !important}}
</style>