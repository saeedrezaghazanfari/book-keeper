<template>
    <div class="container">
        <div class="page-wrapper">

            <!-- header page -->
            <header class="header">
                <!-- three circles -->
                <div class="header--points">
                    <div class="header--point header--point__1"></div>
                    <div class="header--point header--point__2"></div>
                    <div class="header--point header--point__3"></div>
                </div>

                <!-- title page -->
                <div class="header--title">
                    <i class="ti-money"></i>
                    <span>{{ $t('Book Keeper') }}</span>
                </div>
                
            </header>

            <!-- navbar -->
            <nav class="navbar">
                <div class="navbar--username">
                    <img v-if="$store.state.user.profile" :src="`${$store.state.backend}/media/${$store.state.user.profile}`" class="ml-1-2" :alt="$store.state.user.username">
                    <img v-else-if="!$store.state.user.profile && $store.state.user.username" src="@/assets/img/wolf.png" class="ml-1-2">
                    <span v-if="$store.state.user.first_name">{{ $store.state.user.first_name }} {{ $store.state.user.last_name }}</span>
                    <i v-if="$store.state.user.first_name" @click="log_out_user" class="ti-power-off mx-1-2 cur-poi" style="font-size: 10px;"></i>
                </div>
                <div class="navbar--searchbar">
                    <div class="input-wrapper"> 
                        <form @submit.prevent="search_transaction">
                            <i @click="get_voice_to_search" ref="icon_get_voice_ref" class="ti-microphone link"></i>
                            <input type="text" class="link" ref="input_search_txt" @input="control_input" v-model="search_text" :placeholder="$t('Search for Transactions')">
                            <i class="ti-close spinner-hover link d-none" @click="reset_searchbar" ref="close_ref"></i>
                        </form>
                    </div>
                </div>
                <div class="navbar--navigator">
                    <button @click="$router.push('/' + this.$i18n.locale + '/')"><i :class="paths_to_active_home() ? 't-black' : ''" class="ti-home"></i></button>
                    <button @click="reload_page()"><i class="ti-reload"></i></button>
                    <button @click="$router.go(1)"><i class="ti-arrow-right"></i></button>
                    <button @click="$router.go(-1)"><i class="ti-arrow-left"></i></button>
                </div>
            </nav>

            <!-- body -->
            <article class="article">
                <div class="wrapper-body" :class="$store.state.bg_class">

                    <!-- show component -->
                    <router-view v-slot="{Component}">
                        <transition name="fade">
                            <component :is="Component" :key="$route.path"></component>
                        </transition>
                    </router-view>

                </div>
                <div class="lang-section">
                    <language-switcher v-slot="{ links }" active-class="router-link-exact-active">
                        <router-link :to="link.url" v-for="link in links" :key="link.langIndex" :class="link.activeClass">
                            <span :class="$i18n.locale != link.langIndex ? '' : 'disabled'">{{ link.langName }}</span>
                        </router-link>
                    </language-switcher>
                </div>
                
                <div 
                    v-show="repeatAchilleVoice"
                    class="audio_section" 
                    :class="$route.path == `/${this.$i18n.locale}/save-voice-transaction` ? 'audio_section--active' : ''" 
                    :title="$route.path != `/${this.$i18n.locale}/save-voice-transaction` ? this.$t('If you want to save the transaction with voice, click the button') : this.$t('I hope you were Satisfied')"
                >
                    <button @click="clicked_microphone">
                        <i v-if="$route.path != `/${this.$i18n.locale}/save-voice-transaction`" class="ti-microphone"></i>
                        <i v-else class="ti-comments-smiley"></i>
                    </button>
                </div>

            </article>

        </div>
    </div>
    <div class="web--version">
        <p :title="v_title">
            <span>V</span><span>{{v_version}}</span>
        </p>
    </div>
    <div class="web--links">
        <ul>
            <li>
                <a href="https://github.com/saeedrezaghazanfari" class="hover-light" target="_blank">
                    <i class="ti-github"></i>
                </a>
            </li>
            <li>
                <a href="https://instagram.com/saeedreza_wu" class="hover-pink" target="_blank">
                    <i class="ti-instagram"></i>
                </a>
            </li>
            <li>
                <a href="https://www.linkedin.com/in/%D8%B3%D8%B9%DB%8C%D8%AF%D8%B1%D8%B6%D8%A7-%D8%BA%D8%B6%D9%86%D9%81%D8%B1%DB%8C-7b2944220/" class="hover-lblue" target="_blank">
                    <i class="ti-linkedin"></i>
                </a>
            </li>
            <li>
                <a href="mailto:saeedreza.gh.1397@gmail.com" class="hover-red" target="_blank">
                    <i class="ti-email"></i>
                </a>
            </li>
        </ul>
    </div>
</template>

<script>
import axios from './plugins/axios';

export default {
    name: 'App', 
    data: () => ({
        search_text: '',
        v_title: '',
        v_version: '',
        lang_voice_assistant: '',
        repeatAchilleVoice: true,
    }),
    
    created() { 
        this.get_version(); 
    },

    methods: {

        clicked_microphone() {
            if(this.$route.path != `/${this.$i18n.locale}/save-voice-transaction` ) {
                this.$router.push('/' + this.$i18n.locale + '/save-voice-transaction');
            } else {
                this.repeatAchilleVoice = false;
                let audio = new Audio(`/audio/${this.$i18n.locale}/thankyou.mp3`);
                audio.play();

                setTimeout(() => {
                    this.repeatAchilleVoice = true;
                }, 10000)
            }
        },

        fixNumbers(str) {
            let persianNumbers = [/۰/g, /۱/g, /۲/g, /۳/g, /۴/g, /۵/g, /۶/g, /۷/g, /۸/g, /۹/g]
            if(typeof str === 'string') {
                for(let i=0; i < 10; i++)
                    str = str.replace(persianNumbers[i], i);
            }
            return str;
        },

        reload_page() {location.reload()},

        get_voice_to_search() {

            if(!this.$refs.icon_get_voice_ref.classList.contains('blink-animation')) {

                if(this.$i18n.locale == 'fa') {
                    this.lang_voice_assistant = 'fa-IR';
                } else if (this.$i18n.locale == 'en') {
                    this.lang_voice_assistant = 'en-US';
                }

                window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                const recognition = new SpeechRecognition();
                
                // set configs
                recognition.continuous = false;
                recognition.lang = this.lang_voice_assistant;
                recognition.interimResults = true;
                recognition.maxAlternatives = 1;

                this.$refs.icon_get_voice_ref.classList.add('blink-animation');
                this.$refs.input_search_txt.setAttribute('placeholder', this.$t('Please Speak to Search Transaction...'));
                
                recognition.start(); // get voice from client

                let my_this = this;
                recognition.onresult = function(e) { // set results in dom
                    const transcript = Array.from(e.results).map(result => result[0]).map(result => result.transcript).join('');
                    my_this.search_text = my_this.fixNumbers(transcript);
                }
                recognition.onerror= function(event) { // an error occurred
                    my_this.$refs.icon_get_voice_ref.classList.remove('blink-animation');
                    my_this.$refs.input_search_txt.setAttribute('placeholder', my_this.$t('Search for Transactions'));
                    recognition.stop();
                }
                recognition.onnomatch = function(event) { // not found results
                    my_this.$refs.icon_get_voice_ref.classList.remove('blink-animation');
                    my_this.$refs.input_search_txt.setAttribute('placeholder', my_this.$t('Search for Transactions'));
                    recognition.stop();
                }
                recognition.onspeechend = function(event) { // end of get tunes
                    my_this.$refs.icon_get_voice_ref.classList.remove('blink-animation');
                    my_this.$refs.input_search_txt.setAttribute('placeholder', my_this.$t('Search for Transactions'));
                    recognition.stop();
                    my_this.search_transaction();
                }
            }

        },

        paths_to_active_home() {
            let pathes = ['/fa/', '/en/'];
            if(this.$route.path == pathes[0] || this.$route.path == pathes[1]) {
                return true;
            }
            return false;
        },

        async get_version() {
            let a_token = JSON.parse(localStorage.getItem('BOOKKEEPER_AT'));
            await axios.get(`/${this.$i18n.locale}/api/v1/get-last-version/`, {
                headers: {
                    'Authorization': `Bearer ${a_token}`,
                }
            })
            .then((result) => {
                if(result.status === 200) {
                    this.v_version = result.data.version;
                    this.v_title = result.data.description;
                }
            })
            .catch((err) => {
                this.$router.push('/' + this.$i18n.locale + '/sign-in');
            });
        },
        log_out_user() {
            localStorage.removeItem('BOOKKEEPER_AT');
            localStorage.removeItem('BOOKKEEPER_RT');
            this.$store.state.user = '';
            this.$router.push('/' + this.$i18n.locale + '/sign-in');
        },
        control_input(e) {
            if(e.target.value.length > 0) { this.$refs.close_ref.classList.remove('d-none'); }
            else if(e.target.value.length < 1 ) { this.$refs.close_ref.classList.add('d-none'); }
        },
        search_transaction() {
            if (this.search_text) {
                this.$store.commit('SAVE_SEARCH_QUERY', this.search_text);
                this.$router.push(`/${this.$i18n.locale}/search-transaction/${this.search_text}`);
            }
        },
        reset_searchbar() {
            this.search_text = '';
            this.$router.push('/' + this.$i18n.locale + '/last-transactions');
        }
    }
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {transition: opacity 0.5s ease;}
.t-black { color: black !important; }
.fade-enter-from, .fade-leave-to {opacity: 0;}
.opacity-wrapper h4{margin-bottom:1rem}.opacity-wrapper ul.wrapper-links{list-style-type:none}.opacity-wrapper ul.wrapper-links li{padding:8px 18px}.opacity-wrapper ul.wrapper-links li a{color:white;transition:all 0.3s ease;font-size:12pt}.opacity-wrapper ul.wrapper-links li a i{padding:0 4px;transition:all 0.3s ease;font-size:12pt;color:gray}.opacity-wrapper ul.wrapper-links li:hover a{padding-right:5px}.opacity-wrapper ul.wrapper-links li:hover i{font-size:15pt;color:white}@media screen and (max-width: 750px){.container .page-wrapper .article .wrapper-body .opacity-wrapper{width:90% !important}}
</style>