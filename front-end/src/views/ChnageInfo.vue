<template>
    <div class="opacity-wrapper" :class="{'opacity-wrapper-ltr': $i18n.locale == 'en'}">
        <h4><i class="ti-user"></i> {{ $t('Change Info') }}</h4>

        <form novalidate @submit.prevent="save_info" enctype="multipart/form-data">
            <div class="forminput-control">
                <input type="text" v-model="fname" id="fname_field" required>
                <label for="fname_field">{{ $t('First Name') }}</label>
            </div>
            <div class="forminput-control">
                <input type="text" v-model="lname" id="lname_field" required>
                <label for="lname_field">{{ $t('Last Name') }}</label>
            </div>
            <div class="forminput-control">
                <input type="file" id="profile_field" ref="profile_field" @change="submit_profile" required>
                <div class="forminput-file">
                    <div><label for="profile_field" id="profile_field_label">{{ $t('Profile') }}</label></div>
                    <button type="button" ref="btn_uploaded"><i class="ti-upload"></i></button>
                    <img src="" ref="img_uploaded" class="d-none">
                </div>
            </div>

            <div class="progress-nav-bar">
                <div class="progress-bar" ref="progress_bar_ref" :style="{'width': `${uploadPercentage}%`}"></div>
            </div>
            
            <button type="submit" class="btn">{{ $t('SAVE') }}</button><br>
        </form>

    </div>
    <div class="msg-section">
        <p class="success fade-out" v-if="msg.success"><i class="ti-thumb-up"></i> {{ msg.success }}</p>
        <p class="error fade-out" v-if="msg.error"><i class="ti-thumb-down"></i> {{ msg.error }}</p>
        <p class="info fade-out" v-if="msg.info"><i class="ti-info-alt"></i> {{ msg.info }}</p>
    </div>
</template>

<script>
import axios from '../plugins/axios';

export default {
    name: 'ChangeInfo',

    data () {
        return {
            fname: this.$store.state.user.first_name,
            lname: this.$store.state.user.last_name,
            profile: '',
            result_profile: {
                profile: '',
            },
            uploadPercentage: 0,
            msg: { success: '', error: '', info: '' },
        }
    },

    methods: {

        submit_profile() {
            this.msg ={ success: '', error: '', info: '' };
            this.uploadPercentage = 0;
            this.profile = this.$refs.profile_field.files[0];

            let formdata = new FormData();
            let a_token = JSON.parse(localStorage.getItem('BOOKKEEPER_AT'));

            formdata.append('profile', this.profile);

            axios.post(`/${this.$i18n.locale}/api/v1/profile-collector/`, formdata, {
                headers: {
                    'Authorization': `Bearer ${a_token}`,
                    'Content-Type': 'multipart/form-data',
                },
                onUploadProgress: function( progressEvent ) {
                    this.uploadPercentage = parseInt( Math.round( ( progressEvent.loaded / progressEvent.total ) * 100 ) );
                }.bind(this)
            })
            .then((result) => {
                if(result.data.status === 200) {
                    this.msg ={ success: '', error: '', info: '' };
                    this.$refs.progress_bar_ref.classList.add('bg-green');
                    this.result_profile.profile = result.data.profile;
                    this.$refs.btn_uploaded.classList.add('d-none');
                    this.$refs.img_uploaded.classList.remove('d-none');
                    this.$refs.img_uploaded.setAttribute('src', `http://127.0.0.1:8000/media/${this.result_profile.profile}`);
                }
            })
            .catch((err) => {
                if(err.response) {
                    this.msg ={ success: '', error: '', info: '' };
                    this.msg.error = this.$t('There is a Problem in Your Form');
                }
            });
        },

        save_info() {
            this.msg ={ success: '', error: '', info: '' };
            let formdata = new FormData();
            let a_token = JSON.parse(localStorage.getItem('BOOKKEEPER_AT'));
            formdata.append('first_name', this.fname);
            formdata.append('last_name', this.lname);
            
            axios.post(`/${this.$i18n.locale}/api/v1/info-update/`, formdata, {
                headers: {
                    'Authorization': `Bearer ${a_token}`,
                    'Content-Type': 'application/json',
                },
            })
            .then((result) => {
                if(result.data.status === 200) {
                    this.msg ={ success: '', error: '', info: '' };
                    this.msg.success = this.$t('Your information was Updated');
                    setTimeout(() => {
                        this.$router.push('/' + this.$i18n.locale + '/')
                    }, 3000);
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
input#profile_field {display: none;}
.opacity-wrapper { max-height: 307px !important;}
.bg-green {background-color: rgb(0, 255, 0) !important;}
.progress-nav-bar {
    position: relative;
    width: 100%;
    background-color: transparent;
    height: 5px;
    margin-bottom: 10px;
    border-radius: 5px;
    transition: all 0.3s linear;
}
.progress-nav-bar .progress-bar {
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    width: 0%;
    border-radius: 5px;
    background-color: white;
    transition: all 0.3s linear;
}
.forminput-file { display: flex; margin-bottom: 10px; }
.forminput-file div {flex: auto; position: relative;}
.forminput-file button {width: 50px; border-radius: 5px; padding: 5px 0; margin-top: 8px; color: white; background-color: #0000006e; border: none; outline: none; }
.forminput-file img {width: 50px; height: 40px; border-radius: 3px; padding: 5px 0; margin-top: 4px; color: white; background-color: #0000006e; border: none; outline: none; }
label#profile_field_label { width: 95%; font-size: 16px; padding: 11px 3px 3px 3px;color:#eaeaea;margin-bottom:20px;border:none;border-bottom:1px solid #fff;background:transparent}
.opacity-wrapper-ltr{direction:ltr !important}.opacity-wrapper-ltr .forminput-control{position:relative}.opacity-wrapper-ltr .forminput-control label{position:absolute;top:0;left:0;padding:10px 0;font-size:15px;color:#fff;transition:.5s}.opacity-wrapper-ltr .forminput-control #current_stock_field,.opacity-wrapper-ltr .forminput-control #expire_field{margin-left:5px}.opacity-wrapper-ltr .forminput-control label[for='expire_field']{display:none}.opacity-wrapper-ltr .forminput-control input:focus ~ label,.opacity-wrapper-ltr .forminput-control input:valid ~ label{top:-20px;right:0px;font-size:11px}.opacity-wrapper-ltr button[type="submit"]{float:right !important}.opacity-wrapper h4{margin-bottom:1.5rem}.opacity-wrapper .forminput-control{position:relative}.opacity-wrapper .forminput-control input{width:100%;font-size: 16px; padding: 11px 3px 3px 3px;color:#eaeaea;margin-bottom:20px;border:none;border-bottom:1px solid #fff;background:transparent}.opacity-wrapper .forminput-control label{position:absolute;top:0;right:0;padding:10px 7px;font-size:15px;color:#fff;transition:.5s}.opacity-wrapper .forminput-control #cvv2_field{padding:6px}.opacity-wrapper .forminput-control #current_stock_field,.opacity-wrapper .forminput-control #expire_field{margin-right:5px; width: 97%;}.opacity-wrapper .forminput-control label[for='expire_field']{position:absolute;top:0;right:33px;padding:8px 0;font-size:15px;color:#fff;transition:.5s}.opacity-wrapper .forminput-control input:focus ~ label,.opacity-wrapper .forminput-control input:valid ~ label{top:-20px;right:0px;font-size:11px}.opacity-wrapper button[type="submit"]{color:rgb(238, 238, 238);background-color:#0000006e;padding:0.3rem 1rem;border-radius:5px;transition: all 0.3s ease;float:left}@media screen and (max-width: 900px){.container .page-wrapper .article .wrapper-body .opacity-wrapper{width:90% !important}}
</style>